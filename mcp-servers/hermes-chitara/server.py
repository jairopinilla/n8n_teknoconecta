"""MCP server for Hermes Agent — unified chitara tools via docker exec (no SSH needed)."""
import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("hermes-chitara")

# ── helpers ──────────────────────────────────────────────

def _docker_exec(container: str, cmd: str, timeout: int = 30) -> dict:
    """Run a command inside a Docker container."""
    try:
        r = subprocess.run(
            ["docker", "exec", container, "sh", "-c", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return {"stdout": r.stdout.strip(), "stderr": r.stderr.strip(), "rc": r.returncode}
    except Exception as e:
        return {"error": str(e)}

def _psql(sql: str, db: str = "sandiegoapart") -> dict:
    """Run SQL against PostgreSQL."""
    return _docker_exec("postgres", f"psql -U chitara -d {db} -c '{sql}'")

def _psql_json(sql: str, db: str = "sandiegoapart") -> list:
    """Run SQL and return JSON lines."""
    r = _docker_exec("postgres", f"psql -U chitara -d {db} -t -A -c '{sql}'")
    rows = []
    for line in r.get("stdout", "").split("\n"):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except:
                rows.append(line)
    return rows

def _n8n_cli(cmd: str) -> dict:
    """Run n8n CLI command."""
    return _docker_exec("n8n", f"n8n {cmd}")

def _directus_api(method: str, path: str, body: str = "") -> dict:
    """Call Directus API with cached token."""
    email = os.environ.get("DIRECTUS_CHITARA_EMAIL", "")
    password = os.environ.get("DIRECTUS_CHITARA_PASSWORD", "")
    url = os.environ.get("DIRECTUS_CHITARA_URL", "http://localhost:8055")

    # Get token
    login = _docker_exec("hermes", f"curl -s -X POST '{url}/auth/login' -H 'Content-Type: application/json' -d '{{\"email\":\"{email}\",\"password\":\"{password}\"}}'")
    try:
        token = json.loads(login.get("stdout", "{}")).get("data", {}).get("access_token", "")
    except:
        token = ""

    auth = f"-H 'Authorization: Bearer {token}'" if token else ""
    if body:
        curl = f"curl -s -X {method} '{url}{path}' {auth} -H 'Content-Type: application/json' -d '{body}'"
    else:
        curl = f"curl -s -X {method} '{url}{path}' {auth}"

    r = _docker_exec("hermes", curl, timeout=15)
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", ""), "stderr": r.get("stderr", "")}

def _supabase_api(method: str, path: str, body: str = "") -> dict:
    """Call Supabase REST API."""
    key = os.environ.get("SUPABASE_CHITARA_SERVICE_KEY", "")
    auth = f"-H 'apikey: {key}' -H 'Authorization: Bearer {key}'"
    if body:
        curl = f"curl -s -X {method} 'http://kong:8000{path}' {auth} -H 'Content-Type: application/json' -d '{body}'"
    else:
        curl = f"curl -s -X {method} 'http://kong:8000{path}' {auth}"
    r = _docker_exec("hermes", curl, timeout=15)
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", "")}

def _stays_api(path: str) -> dict:
    """Call Stays.net API."""
    base = os.environ.get("STAYS_API_BASE_URL", "https://jairop.stays.net")
    key = os.environ.get("STAYS_API_KEY", "")
    r = _docker_exec("hermes", f"curl -s '{base}{path}' -H 'accept: application/json' -H 'Authorization: Basic {key}'", timeout=15)
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", "")}

def _pricelabs_api(path: str) -> dict:
    """Call PriceLabs API."""
    key = os.environ.get("PRICELABS_API_KEY", "")
    r = _docker_exec("hermes", f"curl -s 'https://api.pricelabs.co{path}' -H 'X-API-Key: {key}'", timeout=15)
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", "")}


# ── n8n tools ────────────────────────────────────────────

@server.list_tools()
async def list_tools():
    return [
        Tool(name="chitara_n8n_list_workflows", description="List all workflows from n8n on chitara.",
             inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="chitara_n8n_get_workflow", description="Get full workflow JSON by ID.",
             inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="chitara_n8n_list_executions", description="List recent executions from n8n.",
             inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}}, "required": []}),
        Tool(name="chitara_n8n_server_info", description="Get n8n server info and stats.",
             inputSchema={"type": "object", "properties": {}, "required": []}),

        Tool(name="chitara_directus_list_collections", description="List all collections from Directus on chitara.",
             inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="chitara_directus_get_items", description="Get items from a Directus collection.",
             inputSchema={"type": "object", "properties": {"collection": {"type": "string"}, "limit": {"type": "integer"}, "filter": {"type": "string"}}, "required": ["collection"]}),

        Tool(name="chitara_supabase_exec_sql", description="Execute raw SQL on PostgreSQL via Supabase chitara.",
             inputSchema={"type": "object", "properties": {"sql": {"type": "string"}, "db": {"type": "string"}}, "required": ["sql"]}),
        Tool(name="chitara_supabase_query", description="Run a read-only SQL query via API.",
             inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="chitara_supabase_list_tables", description="List tables in a schema.",
             inputSchema={"type": "object", "properties": {"schema": {"type": "string"}}, "required": []}),
        Tool(name="chitara_supabase_get_table", description="Get table structure (columns, types, constraints).",
             inputSchema={"type": "object", "properties": {"schema": {"type": "string"}, "table": {"type": "string"}}, "required": ["table"]}),

        Tool(name="chitara_stays_get_reservations", description="Get reservations from Stays.net for a date range.",
             inputSchema={"type": "object", "properties": {"from_date": {"type": "string"}, "to_date": {"type": "string"}, "date_type": {"type": "string"}, "listing_id": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["from_date", "to_date"]}),
        Tool(name="chitara_stays_search_listings", description="Search bookable listings in Stays.net.",
             inputSchema={"type": "object", "properties": {"from_date": {"type": "string"}, "to_date": {"type": "string"}, "guests": {"type": "integer"}}, "required": ["from_date", "to_date"]}),

        Tool(name="chitara_pricelabs_get_listings", description="Get all listings from PriceLabs.",
             inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="chitara_pricelabs_get_listing", description="Get a specific PriceLabs listing by ID.",
             inputSchema={"type": "object", "properties": {"listing_id": {"type": "string"}}, "required": ["listing_id"]}),

        Tool(name="chitara_docker_ps", description="List all running Docker containers on the VPS.",
             inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="chitara_docker_logs", description="Get recent logs from a Docker container.",
             inputSchema={"type": "object", "properties": {"container": {"type": "string"}, "tail": {"type": "integer"}}, "required": ["container"]}),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "chitara_n8n_list_workflows":
            r = _n8n_cli("list-workflows --output=json")
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_n8n_get_workflow":
            r = _n8n_cli(f"export-workflow --id={arguments['workflow_id']} --output=json")
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_n8n_list_executions":
            limit = arguments.get("limit", 20)
            sql = f"SELECT id, workflow_id, status, started_at FROM execution_entity ORDER BY started_at DESC LIMIT {limit}"
            rows = _psql_json(sql, "n8n")
            return [TextContent(type="text", text=json.dumps(rows, indent=2))]

        elif name == "chitara_n8n_server_info":
            sql = "SELECT count(*) as workflows FROM workflow_entity; SELECT count(*) as credentials FROM credentials_entity; SELECT count(*) as executions FROM execution_entity;"
            rows = _psql_json(sql, "n8n")
            return [TextContent(type="text", text=json.dumps(rows, indent=2))]

        elif name == "chitara_directus_list_collections":
            r = _directus_api("GET", "/collections")
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_directus_get_items":
            collection = arguments["collection"]
            limit = arguments.get("limit", 20)
            filter_str = arguments.get("filter", "")
            path = f"/items/{collection}?limit={limit}"
            if filter_str:
                path += f"&filter={filter_str}"
            r = _directus_api("GET", path)
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_supabase_exec_sql":
            db = arguments.get("db", "sandiegoapart")
            r = _psql(arguments["sql"], db)
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_supabase_query":
            r = _supabase_api("GET", f"/rest/v1/{arguments['query']}")
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_supabase_list_tables":
            schema = arguments.get("schema", "public")
            sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema='{schema}' ORDER BY table_name"
            r = _psql(sql)
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_supabase_get_table":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            sql = f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_schema='{schema}' AND table_name='{table}' ORDER BY ordinal_position"
            r = _psql(sql)
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_stays_get_reservations":
            from_date = arguments["from_date"]
            to_date = arguments["to_date"]
            date_type = arguments.get("date_type", "arrival")
            listing = arguments.get("listing_id", "")
            limit = arguments.get("limit", 20)
            path = f"/external/v1/booking/reservations?from={from_date}&to={to_date}&dateType={date_type}&limit={limit}"
            if listing:
                path += f"&listing_id={listing}"
            r = _stays_api(path)
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_stays_search_listings":
            from_date = arguments["from_date"]
            to_date = arguments["to_date"]
            guests = arguments.get("guests", 1)
            base = os.environ.get("STAYS_API_BASE_URL", "https://jairop.stays.net")
            key = os.environ.get("STAYS_API_KEY", "")
            body = json.dumps({"from_date": from_date, "to_date": to_date, "guests": guests, "rooms": 1})
            curl = f"curl -s -X POST '{base}/external/v1/booking/search-listings' -H 'accept: application/json' -H 'Authorization: Basic {key}' -H 'Content-Type: application/json' -d '{body}'"
            r = _docker_exec("hermes", curl, timeout=15)
            try:
                data = json.loads(r.get("stdout", "{}"))
            except:
                data = {"raw": r.get("stdout", "")}
            return [TextContent(type="text", text=json.dumps(data, indent=2))]

        elif name == "chitara_pricelabs_get_listings":
            r = _pricelabs_api("/v1/listings")
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_pricelabs_get_listing":
            r = _pricelabs_api(f"/v1/listings/{arguments['listing_id']}")
            return [TextContent(type="text", text=json.dumps(r, indent=2))]

        elif name == "chitara_docker_ps":
            r = subprocess.run(["docker", "ps", "--format", "{{.Names}} {{.Status}}"], capture_output=True, text=True, timeout=10)
            return [TextContent(type="text", text=r.stdout)]

        elif name == "chitara_docker_logs":
            container = arguments["container"]
            tail = arguments.get("tail", 50)
            r = subprocess.run(["docker", "logs", container, f"--tail={tail}"], capture_output=True, text=True, timeout=10)
            return [TextContent(type="text", text=r.stdout[:5000])]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
