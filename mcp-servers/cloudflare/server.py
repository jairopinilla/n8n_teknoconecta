# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp[cli]>=1.0.0",
#     "httpx>=0.27.0",
# ]
# ///

"""Cloudflare MCP server — local wrapper for Cloudflare REST API and MCP gateway.

Connects to:
- Cloudflare REST API (api.cloudflare.com) for zone/DNS/Workers management
- Cloudflare DNS Analytics MCP (dns-analytics.mcp.cloudflare.com)
- Cloudflare Docs MCP (docs.mcp.cloudflare.com)
"""

import json
import os
import httpx
from mcp.server.fastmcp import FastMCP

CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CF_ACCOUNT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
CF_API = "https://api.cloudflare.com/client/v4"

mcp = FastMCP("cloudflare")


def _headers():
    return {
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": "application/json",
    }


def _api(method: str, path: str, body: dict | None = None, params: dict | None = None) -> dict:
    url = f"{CF_API}{path}"
    kwargs = {"headers": _headers(), "params": params or {}, "timeout": 30}
    if body is not None:
        kwargs["json"] = body
    r = httpx.request(method, url, **kwargs)
    r.raise_for_status()
    return r.json()


# ── Zone / DNS ────────────────────────────────────────────────────────

@mcp.tool()
def cloudflare_list_zones(name: str = "") -> str:
    """List Cloudflare zones (domains) in your account.

    Args:
        name: Optional domain name filter (e.g. 'tarapaca1140.cl')
    """
    params = {"per_page": 50}
    if name:
        params["name"] = name
    try:
        data = _api("GET", "/zones", params=params)
        zones = data.get("result", [])
        if not zones:
            return "No zones found."
        out = [f"{'Zone':35s} {'ID':35s} {'Status'}" + "\n" + "-" * 80]
        for z in zones:
            out.append(f"{z['name']:35s} {z['id']:35s} {z['status']}")
        return "\n".join(out)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def cloudflare_list_dns_records(zone_id: str, record_type: str = "") -> str:
    """List DNS records for a zone. Optionally filter by type.

    Args:
        zone_id: Cloudflare zone ID (get from cloudflare_list_zones)
        record_type: Optional filter: A, CNAME, TXT, MX, AAAA
    """
    params = {"per_page": 200}
    if record_type:
        params["type"] = record_type
    try:
        data = _api("GET", f"/zones/{zone_id}/dns_records", params=params)
        records = data.get("result", [])
        if not records:
            return "No DNS records found."
        out = []
        for r in records:
            proxied = "🟠" if r.get("proxied") else "⚪"
            out.append(f"{proxied} {r['type']:6s} {r['name']:45s} → {r['content']}")
        return "\n".join(out)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def cloudflare_create_dns_record(
    zone_id: str,
    record_type: str,
    name: str,
    content: str,
    proxied: bool = False,
    ttl: int = 1,
    confirmed: bool = False,
) -> str:
    """Create a DNS record. Requires confirmed=True.

    Args:
        zone_id: Cloudflare zone ID
        record_type: A, CNAME, TXT, MX, or AAAA
        name: Full DNS name (e.g. 'api.tarapaca1140.cl')
        content: Value/ip/target
        proxied: Orange cloud proxy. Default False.
        ttl: TTL in seconds. 1 = Auto. Default 1.
        confirmed: MUST be True to execute.
    """
    if not confirmed:
        return (
            f"⚠️  DNS CREATE pendiente de confirmacion.\n"
            f"    Zone: {zone_id}\n"
            f"    {record_type} {name} → {content}\n"
            f"    Proxied: {proxied}\n\n"
            f"    Para ejecutar: llama de nuevo con confirmed=True"
        )
    body = {"type": record_type, "name": name, "content": content, "ttl": ttl, "proxied": proxied}
    try:
        data = _api("POST", f"/zones/{zone_id}/dns_records", body=body)
        r = data.get("result", {})
        return f"✅ DNS creado: {r['type']} {r['name']} → {r['content']} (proxied: {r.get('proxied')})"
    except Exception as e:
        return f"❌ Error: {e}"


@mcp.tool()
def cloudflare_delete_dns_record(zone_id: str, record_id: str, confirmed: bool = False) -> str:
    """Delete a DNS record. Requires confirmed=True.

    Args:
        zone_id: Cloudflare zone ID
        record_id: DNS record ID to delete
        confirmed: MUST be True to execute.
    """
    if not confirmed:
        return f"⚠️  DELETE DNS record {record_id} in zone {zone_id}. Vuelve a llamar con confirmed=True."
    try:
        _api("DELETE", f"/zones/{zone_id}/dns_records/{record_id}")
        return f"✅ DNS record {record_id} deleted."
    except Exception as e:
        return f"❌ Error: {e}"


# ── Workers ────────────────────────────────────────────────────────────

@mcp.tool()
def cloudflare_workers_list(account_id: str = "") -> str:
    """List Cloudflare Workers scripts for an account.

    Args:
        account_id: Optional account ID. Uses env CLOUDFLARE_ACCOUNT_ID if empty.
    """
    acct = account_id or CF_ACCOUNT
    if not acct:
        return "Error: account_id required. Set CLOUDFLARE_ACCOUNT_ID or pass account_id."
    try:
        data = _api("GET", f"/accounts/{acct}/workers/scripts")
        scripts = data.get("result", [])
        if not scripts:
            return "No Workers scripts found."
        out = []
        for s in scripts:
            meta = s.get("usage_model", "bundled")
            out.append(f"• {s['id']} — created: {s.get('created_on','?')}, usage: {meta}")
        return "\n".join(out)
    except Exception as e:
        return f"Error: {e}"


# ── AI Gateway ─────────────────────────────────────────────────────────

@mcp.tool()
def cloudflare_ai_gateway_list(account_id: str = "") -> str:
    """List AI Gateways for an account.

    Args:
        account_id: Optional account ID. Uses env CLOUDFLARE_ACCOUNT_ID if empty.
    """
    acct = account_id or CF_ACCOUNT
    if not acct:
        return "Error: account_id required."
    try:
        data = _api("GET", f"/accounts/{acct}/ai-gateway/gateways")
        gateways = data.get("result", [])
        if not gateways:
            return "No AI Gateways found."
        out = []
        for g in gateways:
            out.append(f"• {g['name']} (id: {g['id']}) — cache: {g.get('cache_ttl', 'N/A')}")
        return "\n".join(out)
    except Exception as e:
        return f"Error: {e}"


# ── Docs search ────────────────────────────────────────────────────────

@mcp.tool()
def cloudflare_search_docs(query: str) -> str:
    """Search Cloudflare documentation.

    Args:
        query: Search terms (e.g. 'how to deploy a Worker', 'DNS CNAME setup')
    """
    headers = {
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    try:
        r = httpx.post(
            "https://docs.mcp.cloudflare.com/mcp",
            json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "search", "arguments": {"query": query}}, "id": 1},
            headers=headers,
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        content = data.get("result", {}).get("content", [])
        texts = [c.get("text", "") for c in content if c.get("type") == "text"]
        return "\n\n".join(texts)[:3000] if texts else json.dumps(data, indent=2)
    except Exception as e:
        return f"Error searching docs: {e}"


# ── D1 / SQL ───────────────────────────────────────────────────────────

@mcp.tool()
def cloudflare_d1_query(database_id: str, sql: str, account_id: str = "") -> str:
    """Execute SQL query on a Cloudflare D1 database.

    Args:
        database_id: D1 database UUID
        sql: SQL statement (SELECT, INSERT, UPDATE, etc.)
        account_id: Optional account ID. Uses env CLOUDFLARE_ACCOUNT_ID if empty.
    """
    acct = account_id or CF_ACCOUNT
    if not acct:
        return "Error: account_id required."
    try:
        data = _api("POST", f"/accounts/{acct}/d1/database/{database_id}/query", body={"sql": sql})
        results = data.get("result", [{}])[0].get("results", [])
        if not results:
            return "Query executed. No rows returned."
        columns = list(results[0].keys()) if results else []
        out = [" | ".join(columns), "-" * 50]
        for row in results[:50]:
            out.append(" | ".join(str(row.get(c, "")) for c in columns))
        return "\n".join(out)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def cloudflare_d1_list_databases(account_id: str = "") -> str:
    """List all D1 databases in an account.

    Args:
        account_id: Optional account ID. Uses env CLOUDFLARE_ACCOUNT_ID if empty.
    """
    acct = account_id or CF_ACCOUNT
    if not acct:
        return "Error: account_id required."
    try:
        data = _api("GET", f"/accounts/{acct}/d1/database")
        dbs = data.get("result", [])
        if not dbs:
            return "No D1 databases found."
        out = []
        for d in dbs:
            out.append(f"• {d['name']} (id: {d['uuid']}) — created: {d.get('created_at','?')}")
        return "\n".join(out)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()
