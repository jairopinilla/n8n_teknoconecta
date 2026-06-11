"""MCP server for kioskomunicipio — PostgreSQL management on chitara VPS via SSH.

Usage (from another repo / developer machine):
  - Requires uv (pip install uv)
  - Requires SSH key at ~/.ssh/id_ed25519 authorized on VPS
  - Set env: KIOSKO_SSH_HOST, KIOSKO_SSH_USER, KIOSKO_DB_USER, KIOSKO_DB_PASS
"""

import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SSH_HOST = os.environ.get("KIOSKO_SSH_HOST", "5.252.52.190")
SSH_USER = os.environ.get("KIOSKO_SSH_USER", "root")
DB_USER = os.environ.get("KIOSKO_DB_USER", "kiosko_app")
DB_PASS = os.environ.get("KIOSKO_DB_PASS", "KioskoDB2026!")
DB_NAME = os.environ.get("KIOSKO_DB_NAME", "kioskomunicipio")

def _ssh_exec(cmd: str) -> dict:
    safe_cmd = cmd.replace("'", "'\\''")
    ssh = f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {SSH_USER}@{SSH_HOST} '{safe_cmd}'"
    try:
        r = subprocess.run(ssh, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": r.stdout, "stderr": r.stderr, "rc": r.returncode}
    except Exception as e:
        return {"error": str(e)}

def _psql(sql: str) -> dict:
    sql_escaped = sql.replace("'", "'\\''")
    return _ssh_exec(
        f"docker exec postgres psql -U {DB_USER} -d {DB_NAME} -c '{sql_escaped}'"
    )

def _psql_json(sql: str) -> list:
    sql_escaped = sql.replace("'", "'\\''")
    r = _ssh_exec(
        f"docker exec postgres psql -U {DB_USER} -d {DB_NAME} -t -A -c '{sql_escaped}'"
    )
    rows = []
    for line in r.get("stdout", "").strip().split("\n"):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except:
                rows.append(line)
    return rows

server = Server("kiosko-municipio")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="kiosko_list_schemas",
            description="List all database schemas in kioskomunicipio.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="kiosko_list_tables",
            description="List tables in a schema from kioskomunicipio.",
            inputSchema={
                "type": "object",
                "properties": {"schema": {"type": "string", "default": "public"}},
                "required": [],
            },
        ),
        Tool(
            name="kiosko_get_table",
            description="Get table structure (columns, types, constraints) from kioskomunicipio.",
            inputSchema={
                "type": "object",
                "properties": {
                    "schema": {"type": "string", "default": "public"},
                    "table": {"type": "string"},
                },
                "required": ["table"],
            },
        ),
        Tool(
            name="kiosko_exec_sql",
            description="Execute any SQL statement on kioskomunicipio. Full read-write access.",
            inputSchema={
                "type": "object",
                "properties": {"sql": {"type": "string"}},
                "required": ["sql"],
            },
        ),
        Tool(
            name="kiosko_list_extensions",
            description="List all PostgreSQL extensions from kioskomunicipio.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="kiosko_list_functions",
            description="List all stored functions in a schema from kioskomunicipio.",
            inputSchema={
                "type": "object",
                "properties": {"schema": {"type": "string", "default": "public"}},
                "required": [],
            },
        ),
        Tool(
            name="kiosko_get_indexes",
            description="Get indexes for a specific table from kioskomunicipio.",
            inputSchema={
                "type": "object",
                "properties": {
                    "schema": {"type": "string", "default": "public"},
                    "table": {"type": "string"},
                },
                "required": ["table"],
            },
        ),
        Tool(
            name="kiosko_server_info",
            description="Get kioskomunicipio server info and DB stats.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="kiosko_list_roles",
            description="List all database roles from kioskomunicipio.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "kiosko_list_schemas":
            rows = _psql_json(
                "SELECT schema_name FROM information_schema.schemata "
                "WHERE schema_name NOT LIKE 'pg_%' AND schema_name NOT IN ('information_schema', 'extensions') "
                "ORDER BY schema_name"
            )
            result = json.dumps(rows, indent=2)

        elif name == "kiosko_list_tables":
            schema = arguments.get("schema", "public")
            sql = (
                f"SELECT json_build_object('schema', table_schema, 'table', table_name, 'type', table_type) "
                f"FROM information_schema.tables WHERE table_schema = '{schema}' ORDER BY table_name"
            )
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "kiosko_get_table":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            sql = (
                f"SELECT json_build_object('column', c.column_name, 'type', c.data_type, "
                f"'nullable', c.is_nullable, 'default', c.column_default, "
                f"'pk', CASE WHEN pk.constraint_type = 'PRIMARY KEY' THEN true ELSE false END) "
                f"FROM information_schema.columns c "
                f"LEFT JOIN ("
                f"  SELECT ku.table_schema, ku.table_name, ku.column_name, tc.constraint_type "
                f"  FROM information_schema.key_column_usage ku "
                f"  JOIN information_schema.table_constraints tc "
                f"    ON ku.constraint_name = tc.constraint_name AND ku.table_schema = tc.table_schema "
                f"  WHERE tc.constraint_type = 'PRIMARY KEY'"
                f") pk ON c.table_schema = pk.table_schema AND c.table_name = pk.table_name AND c.column_name = pk.column_name "
                f"WHERE c.table_schema = '{schema}' AND c.table_name = '{table}' ORDER BY c.ordinal_position"
            )
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "kiosko_exec_sql":
            r = _psql(arguments["sql"])
            result = r.get("stdout", r.get("error", ""))

        elif name == "kiosko_list_extensions":
            rows = _psql_json(
                "SELECT json_build_object('name', extname, 'version', extversion, 'schema', nspname) "
                "FROM pg_extension JOIN pg_namespace ON pg_extension.extnamespace = pg_namespace.oid ORDER BY extname"
            )
            result = json.dumps(rows, indent=2)

        elif name == "kiosko_list_functions":
            schema = arguments.get("schema", "public")
            sql = (
                f"SELECT json_build_object('schema', n.nspname, 'name', p.proname, "
                f"'args', pg_get_function_arguments(p.oid), 'returns', pg_get_function_result(p.oid)) "
                f"FROM pg_proc p JOIN pg_namespace n ON p.pronamespace = n.oid "
                f"WHERE n.nspname = '{schema}' ORDER BY p.proname"
            )
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "kiosko_get_indexes":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            sql = (
                f"SELECT json_build_object('name', indexname, 'def', indexdef) "
                f"FROM pg_indexes WHERE schemaname = '{schema}' AND tablename = '{table}' ORDER BY indexname"
            )
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "kiosko_server_info":
            db_size = _psql_json("SELECT pg_size_pretty(pg_database_size(current_database()))")
            table_count = _psql_json(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
            )
            stats = _psql_json(
                "SELECT json_build_object('version', version(), 'connections', "
                "(SELECT COUNT(*) FROM pg_stat_activity), 'uptime', pg_postmaster_start_time())"
            )
            result = json.dumps(
                {
                    "db": DB_NAME,
                    "db_size": db_size[0] if db_size else "N/A",
                    "total_tables": table_count[0] if table_count else 0,
                    "stats": stats[0] if stats else {},
                },
                indent=2,
            )

        elif name == "kiosko_list_roles":
            rows = _psql_json(
                "SELECT json_build_object('name', rolname, 'super', rolsuper, 'login', rolcanlogin) "
                "FROM pg_roles ORDER BY rolname"
            )
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
