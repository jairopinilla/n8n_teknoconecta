# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp[cli]>=1.0.0",
#     "httpx>=0.27.0",
# ]
# ///

import json
import os
import re
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

DOC_PATH = Path(__file__).resolve().parent.parent.parent / "documentacion" / "Pricelabs_API.md"

# ── Parse once at startup ──────────────────────────────────────────────

def parse_documentation():
    text = DOC_PATH.read_text(encoding="utf-8")
    lines = text.split("\n")

    sections = []
    cur_section = None
    buff = []

    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            if cur_section is not None:
                cur_section["content"] = "\n".join(buff).strip()
                sections.append(cur_section)
            cur_section = {"title": line[3:].strip(), "content": ""}
            buff = []
        elif cur_section is not None:
            buff.append(line)

    if cur_section is not None:
        cur_section["content"] = "\n".join(buff).strip()
        sections.append(cur_section)

    return sections


SECTIONS = parse_documentation()
FULL_TEXT = DOC_PATH.read_text(encoding="utf-8")

mcp = FastMCP("pricelabs-docs")


# ── Documentation tools ────────────────────────────────────────────────

@mcp.tool()
def list_endpoints() -> str:
    """List all Pricelabs API endpoints documented in Pricelabs_API.md"""
    out = []
    for s in SECTIONS:
        out.append(f"## {s['title']}")
    return "\n".join(out)


@mcp.tool()
def get_endpoint_detail(name: str) -> str:
    """Get full documentation for a specific Pricelabs API endpoint.

    Use the exact name shown in list_endpoints. Pass an endpoint name
    (e.g. 'GET all listings', 'POST update listings', 'POST prices for listings').
    """
    for s in SECTIONS:
        if name.lower() in s["title"].lower() or s["title"].lower() in name.lower():
            return f"## {s['title']}\n\n{s['content']}"

    matches = []
    for s in SECTIONS:
        if any(token in s["title"].lower() for token in name.lower().split()):
            matches.append(s["title"])
    if matches:
        return f"No exact match. Try one of: {', '.join(matches)}"

    return f"No endpoint found matching '{name}'"


@mcp.tool()
def search_pricelabs_docs(query: str) -> str:
    """Full-text search across the entire Pricelabs API documentation.

    Returns relevant paragraphs containing the search terms.
    Use for questions like 'how to update listing price', 'what headers are needed', etc.
    """
    lines = FULL_TEXT.split("\n")
    results = []
    for i, line in enumerate(lines):
        if query.lower() in line.lower():
            start = max(0, i - 6)
            end = min(len(lines), i + 7)
            context = "\n".join(lines[start:end])
            parent = ""
            for j in range(i, -1, -1):
                if lines[j].startswith("## ") and not lines[j].startswith("### "):
                    parent = lines[j].strip()
                    break
            results.append(f"**[{parent}]** (línea {i+1})\n```\n{context}\n```")

    if not results:
        return f"No results found for '{query}'"

    if len(results) > 12:
        results = results[:12]
        remaining = len([_ for _ in lines if query.lower() in _.lower()])
        results.append(f"\n*...y ~{remaining - 12} resultados más. Acota el query para más precisión.*")

    return "\n\n---\n\n".join(results)


# ── API call tools ─────────────────────────────────────────────────────

BASE_URL = os.environ.get("PRICELABS_API_BASE_URL", "https://api.pricelabs.co")
API_KEY = os.environ.get("PRICELABS_API_KEY", "")


def _build_headers() -> dict:
    return {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
    }


@mcp.tool()
def pricelabs_api_call(method: str, path: str, body: str = "{}") -> str:
    """Make authenticated HTTP request to Pricelabs API.

    Authenticates automatically with X-API-Key header.

    Args:
        method: HTTP method (GET, POST)
        path: API path, e.g. '/v1/listings', '/v1/listings/123', '/v1/fetch_prices'
        body: JSON string of request body for POST, e.g. '{"listing":{"id":"abc","pms":"xyz"}}'

    Returns JSON response as formatted string, or error details.
    """
    if not API_KEY:
        return "Error: PRICELABS_API_KEY not configured in environment"

    url = f"{BASE_URL}{path}"
    headers = _build_headers()

    try:
        data = json.loads(body) if body else None
    except json.JSONDecodeError:
        return f"Error: invalid JSON in body: {body}"

    try:
        with httpx.Client(timeout=30) as client:
            method_upper = method.upper()
            if method_upper == "GET":
                resp = client.get(url, headers=headers)
            elif method_upper == "POST":
                resp = client.post(url, headers=headers, json=data)
            else:
                return f"Unsupported HTTP method: {method}. Use GET or POST."

        if resp.status_code >= 400:
            return f"HTTP {resp.status_code}\nURL: {url}\nResponse: {resp.text[:2000]}"

        try:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            return resp.text[:4000] if resp.text else "(empty response)"

    except httpx.RequestError as e:
        return f"Request failed: {type(e).__name__}: {e}"


@mcp.tool()
def pricelabs_get_listings() -> str:
    """Get all listings from your Pricelabs account.

    Calls GET /v1/listings.
    """
    if not API_KEY:
        return "Error: PRICELABS_API_KEY not configured in environment"

    url = f"{BASE_URL}/v1/listings"
    headers = _build_headers()

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(url, headers=headers)
        if resp.status_code >= 400:
            return f"HTTP {resp.status_code}\nURL: {url}\nResponse: {resp.text[:2000]}"
        try:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            return resp.text[:4000]
    except httpx.RequestError as e:
        return f"Request failed: {type(e).__name__}: {e}"


@mcp.tool()
def pricelabs_get_listing(listing_id: str) -> str:
    """Get a specific Pricelabs listing by ID.

    Calls GET /v1/listings/{listing_id}.

    Args:
        listing_id: The Pricelabs listing ID (e.g. '123456')
    """
    if not API_KEY:
        return "Error: PRICELABS_API_KEY not configured in environment"

    url = f"{BASE_URL}/v1/listings/{listing_id}"
    headers = _build_headers()

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(url, headers=headers)
        if resp.status_code >= 400:
            return f"HTTP {resp.status_code}\nURL: {url}\nResponse: {resp.text[:2000]}"
        try:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            return resp.text[:4000]
    except httpx.RequestError as e:
        return f"Request failed: {type(e).__name__}: {e}"


@mcp.tool()
def pricelabs_update_listings(body: str) -> str:
    """Update listing parameters in Pricelabs (base_price, min_price, max_price).

    Calls POST /v1/listings.

    Args:
        body: JSON string with listings array. Example:
            '{"listings": [{"id": "123456", "base_price": 1100, "min_price": 200, "max_price": 1600}]}'
    """
    if not API_KEY:
        return "Error: PRICELABS_API_KEY not configured in environment"

    return pricelabs_api_call("POST", "/v1/listings", body)


@mcp.tool()
def pricelabs_fetch_prices(body: str) -> str:
    """Fetch current prices for listings from Pricelabs.

    Calls POST /v1/fetch_prices.

    Args:
        body: JSON string with listing info. Example:
            '{"listing": {"id": "abc", "pms": "xyz"}}'
    """
    if not API_KEY:
        return "Error: PRICELABS_API_KEY not configured in environment"

    return pricelabs_api_call("POST", "/v1/fetch_prices", body)


@mcp.tool()
def pricelabs_push_prices(body: str) -> str:
    """Push prices to listings via Pricelabs.

    Calls POST /v1/push_prices.

    Args:
        body: JSON string with listing info. Example:
            '{"listing": "1234", "pms": "abc"}'
    """
    if not API_KEY:
        return "Error: PRICELABS_API_KEY not configured in environment"

    return pricelabs_api_call("POST", "/v1/push_prices", body)


if __name__ == "__main__":
    mcp.run()
