"""MCP server for supabase-chitara — interacts with Supabase on chitara VPS via SSH."""

import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SSH_HOST = os.environ.get("CHITARA_SSH_HOST", "5.252.52.190")
SSH_USER = os.environ.get("CHITARA_SSH_USER", "root")
SERVICE_KEY = os.environ.get("SUPABASE_CHITARA_SERVICE_KEY", "")

def _ssh_exec(cmd: str) -> dict:
    ssh_cmd = f'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {SSH_USER}@{SSH_HOST} {cmd}'
    try:
        result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": result.stdout, "stderr": result.stderr, "rc": result.returncode}
    except Exception as e:
        return {"error": str(e)}

def api_call(method: str, path: str, body: str = "") -> dict:
    auth = f"-H 'apikey: {SERVICE_KEY}' -H 'Authorization: Bearer {SERVICE_KEY}'"
    if body:
        b = body.replace("'", "'\\''")
        curl = f"curl -s -X {method} http://localhost:8080{path} {auth} -H 'Content-Type: application/json' -d '{b}'"
    else:
        curl = f"curl -s -X {method} http://localhost:8080{path} {auth}"
    r = _ssh_exec(f"'{curl}'")
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", ""), "error": r.get("stderr", "")}

server = Server("supabase-chitara")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="supabase_chitara_list_schemas", description="List all database schemas from Supabase on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="supabase_chitara_list_tables", description="List tables in a schema from Supabase on chitara.", inputSchema={"type": "object", "properties": {"schema": {"type": "string"}}, "required": []}),
        Tool(name="supabase_chitara_get_table", description="Get table structure (columns, types) from Supabase on chitara.", inputSchema={"type": "object", "properties": {"schema": {"type": "string"}, "table": {"type": "string"}}, "required": ["table"]}),
        Tool(name="supabase_chitara_query", description="Run a read-only SQL query against Supabase on chitara.", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="supabase_chitara_exec_sql", description="Execute SQL (any statement) directly on PostgreSQL via SSH.", inputSchema={"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "supabase_chitara_list_schemas":
            data = api_call("GET", "/schemas")
            result = json.dumps(data, indent=2)
        elif name == "supabase_chitara_list_tables":
            schema = arguments.get("schema", "public")
            data = api_call("GET", f"/tables?schema={schema}")
            result = json.dumps(data, indent=2)
        elif name == "supabase_chitara_get_table":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            data = api_call("GET", f"/columns?schema={schema}&table={table}")
            result = json.dumps(data, indent=2)
        elif name == "supabase_chitara_query":
            data = api_call("POST", "/query", json.dumps({"query": arguments["query"]}))
            result = json.dumps(data, indent=2, ensure_ascii=False)
        elif name == "supabase_chitara_exec_sql":
            sql = arguments["sql"].replace("'", "'\\''")
            r = _ssh_exec(f"docker exec postgres psql -U chitara -d sandiegoapart -c '{sql}'")
            result = r.get("stdout", r.get("error", ""))
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
