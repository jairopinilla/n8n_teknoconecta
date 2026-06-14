"""MCP server for topic_system — PostgreSQL management on chitara VPS via SSH.

Usage (from topic_system repo / developer machine):
  - Requires uv (pip install uv)
  - Requires SSH key at ~/.ssh/id_ed25519 authorized on VPS
  - Set env: TOPIC_SSH_HOST, TOPIC_SSH_USER, TOPIC_DB_USER, TOPIC_DB_PASS
"""

import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SSH_HOST = os.environ.get("TOPIC_SSH_HOST", "5.252.52.190")
SSH_USER = os.environ.get("TOPIC_SSH_USER", "root")
DB_USER = os.environ.get("TOPIC_DB_USER", "topic_system_app")
DB_PASS = os.environ.get("TOPIC_DB_PASS", "ws3-2Gq9ttD_ZNFjm1ZIz-o7a8G3nh4z")
DB_NAME = os.environ.get("TOPIC_DB_NAME", "topic_system")

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

server = Server("topic-system-db")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="topic_system_list_schemas",
            description="List all database schemas in topic_system.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="topic_system_list_tables",
            description="List tables in a schema from topic_system.",
            inputSchema={
                "type": "object",
                "properties": {"schema": {"type": "string", "default": "public"}},
                "required": [],
            },
        ),
        Tool(
            name="topic_system_get_table",
            description="Get table structure (columns, types, constraints) from topic_system.",
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
            name="topic_system_exec_sql",
            description="Execute any SQL statement on topic_system. Full read-write access.",
            inputSchema={
                "type": "object",
                "properties": {"sql": {"type": "string"}},
                "required": ["sql"],
            },
        ),
        Tool(
            name="topic_system_list_extensions",
            description="List all PostgreSQL extensions from topic_system.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="topic_system_list_functions",
            description="List all stored functions in a schema from topic_system.",
            inputSchema={
                "type": "object",
                "properties": {"schema": {"type": "string", "default": "public"}},
                "required": [],
            },
        ),
        Tool(
            name="topic_system_get_indexes",
            description="Get indexes for a specific table from topic_system.",
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
            name="topic_system_server_info",
            description="Get topic_system server info and DB stats.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="topic_system_list_roles",
            description="List all database roles from topic_system.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="topic_system_query",
            description="Run a read-only SQL query against topic_system via psql.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        Tool(
            name="topic_system_get_migrations",
            description="List applied migrations from topic_system (if tracking table exists).",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="topic_system_apply_migration",
            description="Apply a new migration SQL to topic_system.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Migration name (snake_case)"},
                    "sql": {"type": "string"},
                    "confirmed": {"type": "boolean", "default": False},
                },
                "required": ["name", "sql"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "topic_system_list_schemas":
            rows = _psql_json(
                "SELECT schema_name FROM information_schema.schemata "
                "WHERE schema_name NOT LIKE 'pg_%' AND schema_name NOT IN ('information_schema', 'extensions') "
                "ORDER BY schema_name"
            )
            result = json.dumps(rows, indent=2)

        elif name == "topic_system_list_tables":
            schema = arguments.get("schema", "public")
            sql = (
                f"SELECT json_build_object('schema', table_schema, 'table', table_name, 'type', table_type) "
                f"FROM information_schema.tables WHERE table_schema = '{schema}' ORDER BY table_name"
            )
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "topic_system_get_table":
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

        elif name == "topic_system_exec_sql":
            r = _psql(arguments["sql"])
            result = r.get("stdout", r.get("error", ""))

        elif name == "topic_system_list_extensions":
            rows = _psql_json(
                "SELECT json_build_object('name', extname, 'version', extversion, 'schema', nspname) "
                "FROM pg_extension JOIN pg_namespace ON pg_extension.extnamespace = pg_namespace.oid ORDER BY extname"
            )
            result = json.dumps(rows, indent=2)

        elif name == "topic_system_list_functions":
            schema = arguments.get("schema", "public")
            sql = (
                f"SELECT json_build_object('schema', n.nspname, 'name', p.proname, "
                f"'args', pg_get_function_arguments(p.oid), 'returns', pg_get_function_result(p.oid)) "
                f"FROM pg_proc p JOIN pg_namespace n ON p.pronamespace = n.oid "
                f"WHERE n.nspname = '{schema}' ORDER BY p.proname"
            )
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "topic_system_get_indexes":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            sql = (
                f"SELECT json_build_object('name', indexname, 'def', indexdef) "
                f"FROM pg_indexes WHERE schemaname = '{schema}' AND tablename = '{table}' ORDER BY indexname"
            )
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "topic_system_server_info":
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

        elif name == "topic_system_list_roles":
            rows = _psql_json(
                "SELECT json_build_object('name', rolname, 'super', rolsuper, 'login', rolcanlogin) "
                "FROM pg_roles ORDER BY rolname"
            )
            result = json.dumps(rows, indent=2)

        elif name == "topic_system_query":
            r = _psql(arguments["query"])
            result = r.get("stdout", r.get("error", ""))

        elif name == "topic_system_get_migrations":
            sql = (
                "SELECT json_build_object('name', name, 'applied_at', applied_at) "
                "FROM topic_system_migrations ORDER BY applied_at DESC"
            )
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2)

        elif name == "topic_system_apply_migration":
            if not arguments.get("confirmed", False):
                result = json.dumps({
                    "warning": "Migration NOT applied. Set confirmed=True to execute.",
                    "name": arguments["name"],
                    "preview": arguments["sql"][:500],
                }, indent=2)
            else:
                r = _psql(arguments["sql"])
                _psql(
                    "CREATE TABLE IF NOT EXISTS topic_system_migrations "
                    "(name text PRIMARY KEY, applied_at timestamptz DEFAULT now())"
                )
                _psql(
                    f"INSERT INTO topic_system_migrations (name) VALUES ('{arguments['name']}') "
                    f"ON CONFLICT (name) DO NOTHING"
                )
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
