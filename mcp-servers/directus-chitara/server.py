"""MCP server for directus-chitara — interacts with Directus on chitara VPS via SSH."""

import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SSH_HOST = os.environ.get("CHITARA_SSH_HOST", "5.252.52.190")
SSH_USER = os.environ.get("CHITARA_SSH_USER", "root")
DIRECTUS_EMAIL = os.environ.get("DIRECTUS_CHITARA_EMAIL", "")
DIRECTUS_PASSWORD = os.environ.get("DIRECTUS_CHITARA_PASSWORD", "")

TOKEN_CACHE = None

def _ssh_exec(cmd: str) -> dict:
    ssh_cmd = f'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {SSH_USER}@{SSH_HOST} {cmd}'
    try:
        result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": result.stdout, "stderr": result.stderr, "rc": result.returncode}
    except Exception as e:
        return {"error": str(e)}

def _get_token() -> str:
    global TOKEN_CACHE
    if TOKEN_CACHE:
        return TOKEN_CACHE
    body = json.dumps({"email": DIRECTUS_EMAIL, "password": DIRECTUS_PASSWORD}).replace("'", "'\\''")
    r = _ssh_exec(f"curl -s -X POST http://localhost:8055/auth/login -H 'Content-Type: application/json' -d '{body}'")
    try:
        data = json.loads(r.get("stdout", "{}"))
        TOKEN_CACHE = data.get("data", {}).get("access_token", "")
        return TOKEN_CACHE
    except:
        return ""

def api_call(method: str, path: str, body: str = "") -> dict:
    token = _get_token()
    auth = f"-H 'Authorization: Bearer {token}'" if token else ""
    if body:
        b = body.replace("'", "'\\''")
        curl = f"curl -s -X {method} http://localhost:8055{path} {auth} -H 'Content-Type: application/json' -d '{b}'"
    else:
        curl = f"curl -s -X {method} http://localhost:8055{path} {auth}"
    r = _ssh_exec(f"'{curl}'")
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", ""), "error": r.get("stderr", "")}

server = Server("directus-chitara")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="directus_chitara_list_collections", description="List all collections from Directus on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="directus_chitara_get_items", description="Get items from a Directus collection on chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "limit": {"type": "integer"}, "fields": {"type": "string"}}, "required": ["collection"]}),
        Tool(name="directus_chitara_get_item", description="Get a single item by ID from Directus on chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "item_id": {"type": "string"}}, "required": ["collection", "item_id"]}),
        Tool(name="directus_chitara_list_files", description="List files from Directus on chitara.", inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}}, "required": []}),
        Tool(name="directus_chitara_server_info", description="Get Directus server info on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "directus_chitara_list_collections":
            data = api_call("GET", "/collections?limit=-1")
            names = [c["collection"] for c in data.get("data", [])]
            result = json.dumps({"collections": names, "total": len(names)}, indent=2)
        elif name == "directus_chitara_get_items":
            coll = arguments["collection"]
            limit = arguments.get("limit", 20)
            qs = f"?limit={limit}"
            if arguments.get("fields"):
                qs += f"&fields={arguments['fields']}"
            data = api_call("GET", f"/items/{coll}{qs}")
            result = json.dumps(data, indent=2, ensure_ascii=False)
        elif name == "directus_chitara_get_item":
            data = api_call("GET", f"/items/{arguments['collection']}/{arguments['item_id']}")
            result = json.dumps(data, indent=2, ensure_ascii=False)
        elif name == "directus_chitara_list_files":
            limit = arguments.get("limit", 50)
            data = api_call("GET", f"/files?limit={limit}&sort=-uploaded_on")
            result = json.dumps(data, indent=2, ensure_ascii=False)
        elif name == "directus_chitara_server_info":
            data = api_call("GET", "/server/info")
            result = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        return [TextContent(type="text", text=result[:8000])]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]

async def main():
    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
