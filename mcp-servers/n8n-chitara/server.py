"""MCP server for n8n-chitara — interacts with n8n on chitara VPS via SSH."""

import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SSH_HOST = os.environ.get("CHITARA_SSH_HOST", "5.252.52.190")
SSH_USER = os.environ.get("CHITARA_SSH_USER", "root")
N8N_API_KEY = os.environ.get("N8N_CHITARA_API_KEY", "")

def _ssh_exec(cmd: str) -> dict:
    ssh_cmd = f'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {SSH_USER}@{SSH_HOST} {cmd}'
    try:
        result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": result.stdout, "stderr": result.stderr, "rc": result.returncode}
    except Exception as e:
        return {"error": str(e)}

def api_call(method: str, path: str, body: str = "") -> dict:
    if body:
        curl = f"curl -s -X {method} http://localhost:5678/api/v1{path} -H 'X-N8N-API-KEY: {N8N_API_KEY}' -H 'Content-Type: application/json' -d '{body}'"
    else:
        curl = f"curl -s -X {method} http://localhost:5678/api/v1{path} -H 'X-N8N-API-KEY: {N8N_API_KEY}'"
    # Escape single quotes for SSH
    curl = curl.replace("'", "'\\''")
    r = _ssh_exec(f"'{curl}'")
    try:
        return json.loads(r.get("stdout", "{}"))
    except:
        return {"raw": r.get("stdout", ""), "error": r.get("stderr", "")}

server = Server("n8n-chitara")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="n8n_chitara_list_workflows", description="List all workflows from n8n on chitara VPS.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="n8n_chitara_get_workflow", description="Get a workflow by ID from n8n on chitara.", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="n8n_chitara_list_executions", description="List recent executions from n8n on chitara.", inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}, "workflow_id": {"type": "string"}}, "required": []}),
        Tool(name="n8n_chitara_get_execution", description="Get an execution by ID from n8n on chitara.", inputSchema={"type": "object", "properties": {"execution_id": {"type": "string"}}, "required": ["execution_id"]}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "n8n_chitara_list_workflows":
            data = api_call("GET", "/workflows")
        elif name == "n8n_chitara_get_workflow":
            data = api_call("GET", f"/workflows/{arguments['workflow_id']}")
        elif name == "n8n_chitara_list_executions":
            limit = arguments.get("limit", 20)
            wf = f"&workflowId={arguments['workflow_id']}" if arguments.get("workflow_id") else ""
            data = api_call("GET", f"/executions?limit={limit}{wf}")
        elif name == "n8n_chitara_get_execution":
            data = api_call("GET", f"/executions/{arguments['execution_id']}")
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        return [TextContent(type="text", text=json.dumps(data, indent=2, ensure_ascii=False)[:8000])]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]

async def main():
    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
