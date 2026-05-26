"""MCP server for supabase-chitara — full management of Supabase on chitara VPS via SSH."""

import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SSH_HOST = os.environ.get("CHITARA_SSH_HOST", "5.252.52.190")
SSH_USER = os.environ.get("CHITARA_SSH_USER", "root")
SERVICE_KEY = os.environ.get("SUPABASE_CHITARA_SERVICE_KEY", "")
DB_NAME = os.environ.get("SUPABASE_CHITARA_DB", "sandiegoapart")

def _ssh_exec(cmd: str) -> dict:
    safe_cmd = cmd.replace("'", "'\\''")
    ssh = f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {SSH_USER}@{SSH_HOST} '{safe_cmd}'"
    try:
        r = subprocess.run(ssh, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": r.stdout, "stderr": r.stderr, "rc": r.returncode}
    except Exception as e:
        return {"error": str(e)}

def api_call(method: str, path: str, body: str = "") -> dict:
    auth = f"-H 'apikey: {SERVICE_KEY}' -H 'Authorization: Bearer {SERVICE_KEY}'"
    if body:
        b = body.replace("'", "'\\''")
        curl = f"curl -s -X {method} 'http://localhost:8080{path}' {auth} -H 'Content-Type: application/json' -d '{b}'"
    else:
        curl = f"curl -s -X {method} 'http://localhost:8080{path}' {auth}"
    r = _ssh_exec(curl)
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", ""), "error": r.get("stderr", "")}

def _psql(sql: str, db: str = None) -> dict:
    database = db or DB_NAME
    sql_escaped = sql.replace("'", "'\\''")
    return _ssh_exec(f"docker exec postgres psql -U chitara -d {database} -c '{sql_escaped}'")

def _psql_json(sql: str, db: str = None) -> list:
    database = db or DB_NAME
    sql_escaped = sql.replace("'", "'\\''")
    r = _ssh_exec(f"docker exec postgres psql -U chitara -d {database} -t -A -c '{sql_escaped}'")
    rows = []
    for line in r.get("stdout", "").strip().split("\n"):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except:
                rows.append(line)
    return rows

server = Server("supabase-chitara")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="supabase_chitara_list_schemas", description="List all database schemas from Supabase on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="supabase_chitara_list_tables", description="List tables in a schema from Supabase on chitara.", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}}, "required": []}),
        Tool(name="supabase_chitara_get_table", description="Get table structure (columns, types, constraints) from Supabase on chitara.", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}, "table": {"type": "string"}}, "required": ["table"]}),
        Tool(name="supabase_chitara_query", description="Run a read-only SQL query against Supabase on chitara via API.", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="supabase_chitara_exec_sql", description="Execute any SQL statement directly on PostgreSQL via SSH. Full read-write access.", inputSchema={"type": "object", "properties": {"sql": {"type": "string"}, "db": {"type": "string", "description": "Database name (default: sandiegoapart)"}}, "required": ["sql"]}),
        Tool(name="supabase_chitara_get_migrations", description="List all applied migrations from Supabase on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="supabase_chitara_apply_migration", description="Apply a new migration SQL to Supabase on chitara.", inputSchema={"type": "object", "properties": {"name": {"type": "string", "description": "Migration name (snake_case)"}, "sql": {"type": "string"}, "confirmed": {"type": "boolean", "default": False}}, "required": ["name", "sql"]}),
        Tool(name="supabase_chitara_list_extensions", description="List all PostgreSQL extensions from Supabase on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="supabase_chitara_list_functions", description="List all stored functions in a schema from Supabase on chitara.", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}}, "required": []}),
        Tool(name="supabase_chitara_get_indexes", description="Get indexes for a specific table from Supabase on chitara.", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}, "table": {"type": "string"}}, "required": ["table"]}),
        Tool(name="supabase_chitara_get_policies", description="Get RLS policies for a table from Supabase on chitara.", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}, "table": {"type": "string"}}, "required": ["table"]}),
        Tool(name="supabase_chitara_server_info", description="Get Supabase server info and DB stats from chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="supabase_chitara_list_roles", description="List all database roles from Supabase on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "supabase_chitara_list_schemas":
            rows = _psql_json("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT LIKE 'pg_%' AND schema_name NOT IN ('information_schema', 'extensions') ORDER BY schema_name")
            result = json.dumps(rows, indent=2)

        elif name == "supabase_chitara_list_tables":
            schema = arguments.get("schema", "public")
            sql = f"SELECT json_build_object('schema', table_schema, 'table', table_name, 'type', table_type) FROM information_schema.tables WHERE table_schema = '{schema}' ORDER BY table_name"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "supabase_chitara_get_table":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            sql = f"SELECT json_build_object('column', c.column_name, 'type', c.data_type, 'nullable', c.is_nullable, 'default', c.column_default, 'pk', CASE WHEN pk.constraint_type = 'PRIMARY KEY' THEN true ELSE false END) FROM information_schema.columns c LEFT JOIN (SELECT ku.table_schema, ku.table_name, ku.column_name, tc.constraint_type FROM information_schema.key_column_usage ku JOIN information_schema.table_constraints tc ON ku.constraint_name = tc.constraint_name AND ku.table_schema = tc.table_schema WHERE tc.constraint_type = 'PRIMARY KEY') pk ON c.table_schema = pk.table_schema AND c.table_name = pk.table_name AND c.column_name = pk.column_name WHERE c.table_schema = '{schema}' AND c.table_name = '{table}' ORDER BY c.ordinal_position"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "supabase_chitara_query":
            data = api_call("POST", "/query", json.dumps({"query": arguments["query"]}))
            result = json.dumps(data, indent=2, ensure_ascii=False)

        elif name == "supabase_chitara_exec_sql":
            db = arguments.get("db", DB_NAME)
            r = _psql(arguments["sql"], db)
            result = r.get("stdout", r.get("error", ""))

        elif name == "supabase_chitara_get_migrations":
            rows = _psql_json("SELECT json_build_object('version', version, 'name', name) FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 50")
            result = json.dumps(rows, indent=2) if rows else "No migrations table found"

        elif name == "supabase_chitara_apply_migration":
            if not arguments.get("confirmed"):
                result = "⚠️ Migration requires confirmed=True"
            else:
                r = _psql(arguments["sql"])
                result = f"Migration '{arguments['name']}' applied.\n{r.get('stdout', '')}"

        elif name == "supabase_chitara_list_extensions":
            rows = _psql_json("SELECT json_build_object('name', extname, 'version', extversion, 'schema', nspname) FROM pg_extension JOIN pg_namespace ON pg_extension.extnamespace = pg_namespace.oid ORDER BY extname")
            result = json.dumps(rows, indent=2)

        elif name == "supabase_chitara_list_functions":
            schema = arguments.get("schema", "public")
            sql = f"SELECT json_build_object('schema', n.nspname, 'name', p.proname, 'args', pg_get_function_arguments(p.oid), 'returns', pg_get_function_result(p.oid)) FROM pg_proc p JOIN pg_namespace n ON p.pronamespace = n.oid WHERE n.nspname = '{schema}' ORDER BY p.proname"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "supabase_chitara_get_indexes":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            sql = f"SELECT json_build_object('name', indexname, 'def', indexdef) FROM pg_indexes WHERE schemaname = '{schema}' AND tablename = '{table}' ORDER BY indexname"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "supabase_chitara_get_policies":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            sql = f"SELECT json_build_object('name', polname, 'cmd', cmd, 'permissive', permissive, 'qual', qual) FROM pg_policy p JOIN pg_class c ON p.polrelid = c.oid JOIN pg_namespace n ON c.relnamespace = n.oid WHERE n.nspname = '{schema}' AND c.relname = '{table}'"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2) if rows else "No RLS policies found"

        elif name == "supabase_chitara_server_info":
            db_size = _psql_json("SELECT pg_size_pretty(pg_database_size(current_database()))")
            table_count = _psql_json("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
            stats = _psql_json("SELECT json_build_object('version', version(), 'connections', (SELECT COUNT(*) FROM pg_stat_activity), 'uptime', pg_postmaster_start_time())")
            result = json.dumps({
                "db_size": db_size[0] if db_size else "N/A",
                "total_tables": table_count[0] if table_count else 0,
                "stats": stats[0] if stats else {}
            }, indent=2)

        elif name == "supabase_chitara_list_roles":
            rows = _psql_json("SELECT json_build_object('name', rolname, 'super', rolsuper, 'login', rolcanlogin) FROM pg_roles ORDER BY rolname")
            result = json.dumps(rows, indent=2)

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
