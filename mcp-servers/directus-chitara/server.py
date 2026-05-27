"""MCP server for directus-chitara — full CRUD management of Directus on chitara VPS via SSH."""

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
    safe_cmd = cmd.replace("'", "'\\''")
    ssh = f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {SSH_USER}@{SSH_HOST} '{safe_cmd}'"
    try:
        r = subprocess.run(ssh, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": r.stdout, "stderr": r.stderr, "rc": r.returncode}
    except Exception as e:
        return {"error": str(e)}

def _get_token() -> str:
    global TOKEN_CACHE
    if TOKEN_CACHE:
        return TOKEN_CACHE
    body = json.dumps({"email": DIRECTUS_EMAIL, "password": DIRECTUS_PASSWORD})
    data_json = body.replace("'", "'\\''")
    r = _ssh_exec(f"curl -s -X POST http://localhost:8055/auth/login -H 'Content-Type: application/json' -d '{data_json}'")
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
        curl = f"curl -s -X {method} 'http://localhost:8055{path}' {auth} -H 'Content-Type: application/json' -d '{b}'"
    else:
        curl = f"curl -s -X {method} 'http://localhost:8055{path}' {auth}"
    r = _ssh_exec(curl)
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", ""), "error": r.get("stderr", "")}

server = Server("directus-chitara")

@server.list_tools()
async def list_tools():
    return [
        # Collections
        Tool(name="directus_chitara_list_collections", description="List all collections from Directus on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="directus_chitara_get_collection", description="Get collection details by name from Directus on chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}}, "required": ["collection"]}),
        Tool(name="directus_chitara_create_collection", description="Create a new collection on Directus chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "meta": {"type": "string", "description": "JSON string: {singleton, note, icon, color, translations, etc.}"}, "fields": {"type": "string", "description": "JSON string: array of field definitions"}}, "required": ["collection"]}),
        Tool(name="directus_chitara_update_collection", description="Update a collection on Directus chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "meta": {"type": "string", "description": "JSON string with meta fields to update"}}, "required": ["collection"]}),
        Tool(name="directus_chitara_delete_collection", description="Delete a collection from Directus chitara. Requires confirmed=True.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "confirmed": {"type": "boolean", "default": False}}, "required": ["collection"]}),

        # Items
        Tool(name="directus_chitara_get_items", description="Get items from a Directus collection on chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "limit": {"type": "integer", "default": 20}, "fields": {"type": "string"}, "filter": {"type": "string", "description": "JSON string: filter rules"}}, "required": ["collection"]}),
        Tool(name="directus_chitara_get_item", description="Get a single item by ID from Directus on chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "item_id": {"type": "string"}}, "required": ["collection", "item_id"]}),
        Tool(name="directus_chitara_create_item", description="Create a new item in a Directus collection on chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "data": {"type": "string", "description": "JSON string: item data"}}, "required": ["collection", "data"]}),
        Tool(name="directus_chitara_update_item", description="Update an item in a Directus collection on chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "item_id": {"type": "string"}, "data": {"type": "string", "description": "JSON string: fields to update"}}, "required": ["collection", "item_id", "data"]}),
        Tool(name="directus_chitara_delete_item", description="Delete an item from a Directus collection. Requires confirmed=True.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "item_id": {"type": "string"}, "confirmed": {"type": "boolean", "default": False}}, "required": ["collection", "item_id"]}),

        # Fields
        Tool(name="directus_chitara_list_fields", description="List all fields of a collection on Directus chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}}, "required": ["collection"]}),
        Tool(name="directus_chitara_create_field", description="Add a new field to a collection on Directus chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "field_data": {"type": "string", "description": "JSON string: {field, type, meta, schema}"}}, "required": ["collection", "field_data"]}),
        Tool(name="directus_chitara_update_field", description="Update a field on Directus chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "field": {"type": "string"}, "field_data": {"type": "string", "description": "JSON string: {meta} with updated field metadata"}}, "required": ["collection", "field"]}),
        Tool(name="directus_chitara_delete_field", description="Delete a field from a collection. Requires confirmed=True.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "field": {"type": "string"}, "confirmed": {"type": "boolean", "default": False}}, "required": ["collection", "field"]}),

        # Files
        Tool(name="directus_chitara_list_files", description="List files from Directus on chitara.", inputSchema={"type": "object", "properties": {"limit": {"type": "integer", "default": 50}}, "required": []}),
        Tool(name="directus_chitara_get_file", description="Get file details by ID from Directus on chitara.", inputSchema={"type": "object", "properties": {"file_id": {"type": "string"}}, "required": ["file_id"]}),
        Tool(name="directus_chitara_update_file", description="Update file metadata on Directus chitara.", inputSchema={"type": "object", "properties": {"file_id": {"type": "string"}, "data": {"type": "string", "description": "JSON string: {title, description, tags, folder}"}}, "required": ["file_id", "data"]}),
        Tool(name="directus_chitara_delete_file", description="Delete a file from Directus chitara. Requires confirmed=True.", inputSchema={"type": "object", "properties": {"file_id": {"type": "string"}, "confirmed": {"type": "boolean", "default": False}}, "required": ["file_id"]}),

        # Flows
        Tool(name="directus_chitara_list_flows", description="List all automation flows from Directus on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="directus_chitara_get_flow", description="Get flow details by ID from Directus on chitara.", inputSchema={"type": "object", "properties": {"flow_id": {"type": "string"}}, "required": ["flow_id"]}),

        # Relations
        Tool(name="directus_chitara_list_relations", description="List all relations from Directus on chitara.", inputSchema={"type": "object", "properties": {"collection": {"type": "string"}}, "required": []}),
        Tool(name="directus_chitara_create_relation", description="Create a relation between collections on Directus chitara.", inputSchema={"type": "object", "properties": {"data": {"type": "string", "description": "JSON string: {collection, field, related_collection, schema, meta}"}}, "required": ["data"]}),

        # Server
        Tool(name="directus_chitara_server_info", description="Get Directus server info and stats on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "directus_chitara_list_collections":
            data = api_call("GET", "/collections?limit=-1")
            names = [{"collection": c.get("collection"), "singleton": (c.get("meta") or {}).get("singleton", False)} for c in data.get("data") or []]
            result = json.dumps({"collections": names, "total": len(names)}, indent=2)

        elif name == "directus_chitara_get_collection":
            data = api_call("GET", f"/collections/{arguments['collection']}")
            result = json.dumps(data, indent=2, ensure_ascii=False)

        elif name == "directus_chitara_create_collection":
            coll = arguments["collection"]
            body = {"collection": coll, "schema": {}, "meta": {}}
            if arguments.get("meta"):
                body["meta"] = json.loads(arguments["meta"])
            if arguments.get("fields"):
                body["fields"] = json.loads(arguments["fields"])
            data = api_call("POST", "/collections", json.dumps(body))
            result = json.dumps(data, indent=2)

        elif name == "directus_chitara_update_collection":
            body = {}
            if arguments.get("meta"):
                body["meta"] = json.loads(arguments["meta"])
            data = api_call("PATCH", f"/collections/{arguments['collection']}", json.dumps(body))
            result = json.dumps(data, indent=2)

        elif name == "directus_chitara_delete_collection":
            if not arguments.get("confirmed"):
                result = "⚠️ Delete requires confirmed=True"
            else:
                data = api_call("DELETE", f"/collections/{arguments['collection']}")
                result = json.dumps(data, indent=2)

        elif name == "directus_chitara_get_items":
            coll = arguments["collection"]
            limit = arguments.get("limit", 20)
            qs = f"?limit={limit}"
            if arguments.get("fields"):
                qs += f"&fields={arguments['fields']}"
            if arguments.get("filter"):
                qs += f"&filter={arguments['filter']}"
            data = api_call("GET", f"/items/{coll}{qs}")
            result = json.dumps(data, indent=2, ensure_ascii=False)

        elif name == "directus_chitara_get_item":
            data = api_call("GET", f"/items/{arguments['collection']}/{arguments['item_id']}")
            result = json.dumps(data, indent=2, ensure_ascii=False)

        elif name == "directus_chitara_create_item":
            data = api_call("POST", f"/items/{arguments['collection']}", arguments["data"])
            result = json.dumps(data, indent=2)

        elif name == "directus_chitara_update_item":
            data = api_call("PATCH", f"/items/{arguments['collection']}/{arguments['item_id']}", arguments["data"])
            result = json.dumps(data, indent=2)

        elif name == "directus_chitara_delete_item":
            if not arguments.get("confirmed"):
                result = "⚠️ Delete requires confirmed=True"
            else:
                data = api_call("DELETE", f"/items/{arguments['collection']}/{arguments['item_id']}")
                result = json.dumps(data, indent=2)

        elif name == "directus_chitara_list_fields":
            data = api_call("GET", f"/fields/{arguments['collection']}")
            fields = []
            for f in data.get("data", []):
                fields.append({"field": f.get("field"), "type": f.get("type"), "required": (f.get("meta") or {}).get("required", False)})
            result = json.dumps({"fields": fields, "total": len(fields)}, indent=2)

        elif name == "directus_chitara_create_field":
            body = json.loads(arguments["field_data"])
            data = api_call("POST", f"/fields/{arguments['collection']}", json.dumps(body))
            result = json.dumps(data, indent=2)

        elif name == "directus_chitara_update_field":
            body = json.loads(arguments["field_data"]) if arguments.get("field_data") else {}
            data = api_call("PATCH", f"/fields/{arguments['collection']}/{arguments['field']}", json.dumps(body))
            result = json.dumps(data, indent=2)

        elif name == "directus_chitara_delete_field":
            if not arguments.get("confirmed"):
                result = "⚠️ Delete requires confirmed=True"
            else:
                data = api_call("DELETE", f"/fields/{arguments['collection']}/{arguments['field']}")
                result = json.dumps(data, indent=2)

        elif name == "directus_chitara_list_files":
            limit = arguments.get("limit", 50)
            data = api_call("GET", f"/files?limit={limit}&sort=-uploaded_on")
            files = []
            for f in data.get("data", []):
                files.append({"id": f.get("id"), "title": f.get("title"), "type": f.get("type"), "filesize": f.get("filesize"), "storage": f.get("storage")})
            result = json.dumps({"files": files, "total": len(files)}, indent=2)

        elif name == "directus_chitara_get_file":
            data = api_call("GET", f"/files/{arguments['file_id']}")
            result = json.dumps(data, indent=2, ensure_ascii=False)

        elif name == "directus_chitara_update_file":
            data = api_call("PATCH", f"/files/{arguments['file_id']}", arguments["data"])
            result = json.dumps(data, indent=2)

        elif name == "directus_chitara_delete_file":
            if not arguments.get("confirmed"):
                result = "⚠️ Delete requires confirmed=True"
            else:
                data = api_call("DELETE", f"/files/{arguments['file_id']}")
                result = json.dumps(data, indent=2)

        elif name == "directus_chitara_list_flows":
            data = api_call("GET", "/flows?limit=-1")
            flows = []
            for f in data.get("data", []):
                flows.append({"id": f.get("id"), "name": f.get("name"), "trigger": f.get("trigger"), "status": f.get("status")})
            result = json.dumps({"flows": flows, "total": len(flows)}, indent=2)

        elif name == "directus_chitara_get_flow":
            data = api_call("GET", f"/flows/{arguments['flow_id']}")
            result = json.dumps(data, indent=2, ensure_ascii=False)

        elif name == "directus_chitara_list_relations":
            path = "/relations"
            if arguments.get("collection"):
                path += f"?filter[collection][_eq]={arguments['collection']}"
            data = api_call("GET", path)
            rels = []
            for r in data.get("data", []):
                rels.append({"collection": r.get("collection"), "field": r.get("field"), "related": r.get("related_collection")})
            result = json.dumps({"relations": rels, "total": len(rels)}, indent=2)

        elif name == "directus_chitara_create_relation":
            body = json.loads(arguments["data"])
            data = api_call("POST", "/relations", json.dumps(body))
            result = json.dumps(data, indent=2)

        elif name == "directus_chitara_server_info":
            info = api_call("GET", "/server/info")
            collections = api_call("GET", "/collections?limit=0&meta[total_count]=*")
            files = api_call("GET", "/files?limit=0&meta[total_count]=*")
            result = json.dumps({
                "server": info.get("data", {}),
                "total_collections": (collections.get("meta") or {}).get("total_count", 0),
                "total_files": (files.get("meta") or {}).get("total_count", 0),
            }, indent=2)

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
