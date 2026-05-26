"""MCP server for n8n-chitara — full management of n8n on chitara VPS via SSH + CLI + DB."""
import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SSH_HOST = os.environ.get("CHITARA_SSH_HOST", "5.252.52.190")
SSH_USER = os.environ.get("CHITARA_SSH_USER", "root")

def _ssh_exec(cmd: str) -> dict:
    safe_cmd = cmd.replace("'", "'\\''")
    ssh = f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {SSH_USER}@{SSH_HOST} '{safe_cmd}'"
    try:
        r = subprocess.run(ssh, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": r.stdout, "stderr": r.stderr, "rc": r.returncode}
    except Exception as e:
        return {"error": str(e)}

def _n8n_cli(cmd: str) -> dict:
    """Run n8n CLI command inside the n8n container."""
    return _ssh_exec(f"docker exec n8n n8n {cmd}")

def _psql(sql: str) -> dict:
    """Run SQL against n8n database."""
    sql_escaped = sql.replace("'", "'\\''")
    return _ssh_exec(f"docker exec postgres psql -U chitara -d n8n -c '{sql_escaped}'")

def _psql_json(sql: str) -> list:
    """Run SQL and return JSON result."""
    sql_escaped = sql.replace("'", "'\\''")
    r = _ssh_exec(f"docker exec postgres psql -U chitara -d n8n -t -A -c '{sql_escaped}'")
    rows = []
    for line in r.get("stdout", "").strip().split("\n"):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except:
                rows.append(line)
    return rows

server = Server("n8n-chitara")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="n8n_chitara_list_workflows", description="List all workflows from n8n on chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="n8n_chitara_get_workflow", description="Get full workflow JSON by ID from n8n on chitara.", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="n8n_chitara_create_workflow", description="Create a new workflow on n8n chitara. Provide name and full workflow JSON.", inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "workflow_json": {"type": "string", "description": "Full workflow JSON (nodes, connections, settings)"}}, "required": ["name", "workflow_json"]}),
        Tool(name="n8n_chitara_update_workflow", description="Update an existing workflow on n8n chitara.", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}, "workflow_json": {"type": "string", "description": "Full workflow JSON (nodes, connections, settings)"}}, "required": ["workflow_id", "workflow_json"]}),
        Tool(name="n8n_chitara_delete_workflow", description="Delete a workflow on n8n chitara. Requires confirmation.", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}, "confirmed": {"type": "boolean", "default": False}}, "required": ["workflow_id"]}),
        Tool(name="n8n_chitara_activate_workflow", description="Activate a workflow on n8n chitara.", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="n8n_chitara_deactivate_workflow", description="Deactivate a workflow on n8n chitara.", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="n8n_chitara_execute_workflow", description="Execute a workflow (trigger it) on n8n chitara.", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="n8n_chitara_list_executions", description="List recent executions from n8n on chitara.", inputSchema={"type": "object", "properties": {"limit": {"type": "integer", "default": 20}, "workflow_id": {"type": "string"}}, "required": []}),
        Tool(name="n8n_chitara_get_execution", description="Get an execution by ID from n8n on chitara.", inputSchema={"type": "object", "properties": {"execution_id": {"type": "string"}}, "required": ["execution_id"]}),
        Tool(name="n8n_chitara_export_workflow", description="Export a workflow as JSON (n8n export format).", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="n8n_chitara_server_info", description="Get n8n server info and statistics from chitara.", inputSchema={"type": "object", "properties": {}, "required": []}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "n8n_chitara_list_workflows":
            sql = "SELECT json_build_object('id', w.id, 'name', w.name, 'active', w.active, 'createdAt', w.\"createdAt\", 'updatedAt', w.\"updatedAt\") FROM workflow_entity w ORDER BY w.name"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2, ensure_ascii=False)

        elif name == "n8n_chitara_get_workflow":
            sql = f"SELECT json_build_object('id', id, 'name', name, 'active', active, 'nodes', nodes, 'connections', connections, 'settings', settings, 'createdAt', \"createdAt\", 'updatedAt', \"updatedAt\") FROM workflow_entity WHERE id = '{arguments['workflow_id']}'"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2, ensure_ascii=False) if rows else "Workflow not found"

        elif name == "n8n_chitara_create_workflow":
            import uuid
            wf_id = uuid.uuid4().hex[:21]
            wf_json = arguments["workflow_json"].replace("'", "''")
            name_safe = arguments["name"].replace("'", "''")
            sql = f"INSERT INTO workflow_entity (id, name, active, nodes, connections, settings, \"createdAt\", \"updatedAt\") VALUES ('{wf_id}', '{name_safe}', false, '{wf_json}'::jsonb, '{{}}'::jsonb, '{{}}'::jsonb, NOW(), NOW())"
            r = _psql(sql)
            if r.get("rc") == 0:
                result = f"Workflow created: id={wf_id}, name={arguments['name']}"
            else:
                result = f"Error: {r.get('stderr', '')}"

        elif name == "n8n_chitara_update_workflow":
            wf_json = arguments["workflow_json"].replace("'", "''")
            sql = f"UPDATE workflow_entity SET nodes = '{wf_json}'::jsonb, \"updatedAt\" = NOW() WHERE id = '{arguments['workflow_id']}'"
            r = _psql(sql)
            result = f"Workflow {arguments['workflow_id']} updated" if r.get("rc") == 0 else f"Error: {r.get('stderr')}"

        elif name == "n8n_chitara_delete_workflow":
            if not arguments.get("confirmed"):
                result = "⚠️ Delete requires confirmed=True. Set confirmed=true to delete."
            else:
                wf_id = arguments["workflow_id"]
                _psql(f"DELETE FROM shared_workflow WHERE \"workflowId\" = '{wf_id}'")
                _psql(f"DELETE FROM execution_entity WHERE \"workflowId\" = '{wf_id}'")
                r = _psql(f"DELETE FROM workflow_entity WHERE id = '{wf_id}'")
                result = f"Workflow {wf_id} deleted" if r.get("rc") == 0 else f"Error: {r.get('stderr')}"

        elif name == "n8n_chitara_activate_workflow":
            r = _psql(f"UPDATE workflow_entity SET active = true, \"updatedAt\" = NOW() WHERE id = '{arguments['workflow_id']}'")
            result = f"Workflow {arguments['workflow_id']} activated" if r.get("rc") == 0 else f"Error: {r.get('stderr')}"

        elif name == "n8n_chitara_deactivate_workflow":
            r = _psql(f"UPDATE workflow_entity SET active = false, \"updatedAt\" = NOW() WHERE id = '{arguments['workflow_id']}'")
            result = f"Workflow {arguments['workflow_id']} deactivated" if r.get("rc") == 0 else f"Error: {r.get('stderr')}"

        elif name == "n8n_chitara_execute_workflow":
            wf_id = arguments["workflow_id"]
            # Activate workflow and let scheduler run it
            r = _psql(f"UPDATE workflow_entity SET active = true, \"updatedAt\" = NOW() WHERE id = '{wf_id}'")
            # Trigger via webhook if a production webhook URL exists
            webhooks = _psql_json(f"SELECT json_build_object('url', \"webhookPath\", 'method', \"webhookMethod\") FROM webhook_entity WHERE \"workflowId\" = '{wf_id}'")
            webhook_results = ""
            for wh in webhooks:
                try:
                    wh_data = wh if isinstance(wh, dict) else json.loads(wh)
                    path = wh_data.get("url", "")
                    method = wh_data.get("method", "GET")
                    if path:
                        if method == "GET":
                            wh_r = _ssh_exec(f"curl -s http://localhost:5678{path}")
                        else:
                            wh_r = _ssh_exec(f"curl -s -X {method} http://localhost:5678{path}")
                        webhook_results += f"\nWebhook {method} {path}: {wh_r.get('stdout', '')[:200]}"
                except:
                    pass
            result = f"Workflow {wf_id} activated. Will execute based on trigger.{webhook_results}"

        elif name == "n8n_chitara_list_executions":
            limit = arguments.get("limit", 20)
            wf_filter = f"AND e.\"workflowId\" = '{arguments['workflow_id']}'" if arguments.get("workflow_id") else ""
            sql = f"SELECT json_build_object('id', e.id, 'workflowId', e.\"workflowId\", 'status', e.status, 'startedAt', e.\"startedAt\", 'stoppedAt', e.\"stoppedAt\", 'mode', e.mode) FROM execution_entity e WHERE 1=1 {wf_filter} ORDER BY e.\"startedAt\" DESC LIMIT {limit}"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2, ensure_ascii=False)

        elif name == "n8n_chitara_get_execution":
            sql = f"SELECT json_build_object('id', id, 'workflowId', \"workflowId\", 'status', status, 'startedAt', \"startedAt\", 'stoppedAt', \"stoppedAt\", 'mode', mode, 'data', data) FROM execution_entity WHERE id = '{arguments['execution_id']}'"
            rows = _psql_json(sql)
            result = json.dumps(rows, indent=2, ensure_ascii=False) if rows else "Execution not found"

        elif name == "n8n_chitara_export_workflow":
            wf_id = arguments["workflow_id"]
            r = _n8n_cli(f"export:workflow --id {wf_id}")
            result = r.get("stdout", r.get("error", "Export failed"))

        elif name == "n8n_chitara_server_info":
            counts = _psql_json("SELECT json_build_object('total_workflows', (SELECT COUNT(*) FROM workflow_entity), 'active_workflows', (SELECT COUNT(*) FROM workflow_entity WHERE active=true), 'total_executions', (SELECT COUNT(*) FROM execution_entity), 'credentials', (SELECT COUNT(*) FROM credentials_entity))")
            result = json.dumps(counts, indent=2)

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
