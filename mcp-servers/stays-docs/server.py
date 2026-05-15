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

DOC_PATH = Path(__file__).resolve().parent.parent.parent / "documentacion" / "APIStaysDoc.md"

# ── Parse once at startup ──────────────────────────────────────────────

def parse_documentation():
    text = DOC_PATH.read_text(encoding="utf-8")
    lines = text.split("\n")

    sections = []
    cur_section = None
    cur_sub = None
    buf = []

    for line in lines:
        if line.startswith("## "):
            if cur_section is not None:
                if cur_sub is not None:
                    cur_sub["content"] = "\n".join(buf).strip()
                sections.append(cur_section)
            cur_section = {"title": line[3:].strip(), "subsections": []}
            cur_sub = None
            buf = []
        elif line.startswith("### "):
            if cur_sub is not None and cur_section is not None:
                cur_sub["content"] = "\n".join(buf).strip()
                cur_section["subsections"].append(cur_sub)
            cur_sub = {"title": line[4:].strip(), "content": ""}
            buf = []
        elif cur_sub is not None:
            buf.append(line)

    if cur_sub is not None and cur_section is not None:
        cur_sub["content"] = "\n".join(buf).strip()
        cur_section["subsections"].append(cur_sub)
    if cur_section is not None:
        sections.append(cur_section)

    return sections


SECTIONS = parse_documentation()
FULL_TEXT = DOC_PATH.read_text(encoding="utf-8")

mcp = FastMCP("stays-docs")


# ── Tools ──────────────────────────────────────────────────────────────

@mcp.tool()
def list_endpoints() -> str:
    """List all Stays.net API sections and endpoints documented in APIStaysDoc.md"""
    out = []
    for s in SECTIONS:
        out.append(f"## {s['title']}")
        for sub in s["subsections"]:
            out.append(f"    • {sub['title']}")
    return "\n".join(out)


@mcp.tool()
def get_endpoint_detail(name: str) -> str:
    """Get full documentation for a specific Stays.net API section or endpoint.

    Use the exact name shown in list_endpoints. Pass a section title
    (e.g. 'Booking Checkout API') or an endpoint name (e.g. 'Initiate checkout process').
    """
    for s in SECTIONS:
        if name.lower() in s["title"].lower() or s["title"].lower() in name.lower():
            lines = [f"## {s['title']}\n"]
            for sub in s["subsections"]:
                lines.append(f"### {sub['title']}\n{sub['content']}\n")
            return "\n".join(lines)
        for sub in s["subsections"]:
            if name.lower() in sub["title"].lower() or sub["title"].lower() in name.lower():
                return f"### {sub['title']}\n\n{sub['content']}"

    # Fuzzy fallback
    matches = []
    for s in SECTIONS:
        if any(token in s["title"].lower() for token in name.lower().split()):
            matches.append(s["title"])
        for sub in s["subsections"]:
            if any(token in sub["title"].lower() for token in name.lower().split()):
                matches.append(sub["title"])
    if matches:
        return f"No exact match. Try one of: {', '.join(matches)}"

    return f"No endpoint found matching '{name}'"


@mcp.tool()
def search_stays_docs(query: str) -> str:
    """Full-text search across the entire Stays.net API documentation.

    Returns relevant paragraphs containing the search terms.
    Use for questions like 'how to authenticate', 'payment endpoint', 'promo code body parameters', etc.
    """
    lines = FULL_TEXT.split("\n")
    results = []
    for i, line in enumerate(lines):
        if query.lower() in line.lower():
            start = max(0, i - 6)
            end = min(len(lines), i + 7)
            context = "\n".join(lines[start:end])
            # Find parent section heading
            parent = ""
            for j in range(i, -1, -1):
                if lines[j].startswith("## ") or lines[j].startswith("### "):
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


# ── API Tools ────────────────────────────────────────────────────────

BASE_URL = os.environ.get("STAYS_API_BASE_URL", "https://jairop.stays.net")
API_KEY = os.environ.get("STAYS_API_KEY", "")


def _build_headers() -> dict:
    return {
        "Authorization": f"Basic {API_KEY}",
        "Content-Type": "application/json",
    }


@mcp.tool()
def stays_api_call(method: str, path: str, query_params: str = "{}", body: str = "{}") -> str:
    """Make authenticated HTTP request to Stays.net API (jairop.stays.net).

    Authenticates automatically with Basic Auth using the configured API key.

    Args:
        method: HTTP method (GET, POST, PATCH, DELETE)
        path: API path, e.g. '/external/v1/booking/reservations', '/v1/bookings/reservations/123/payments'
        query_params: JSON string of query parameters, e.g. '{"from":"2026-01-01","to":"2026-03-30","dateType":"arrival"}'
        body: JSON string of request body for POST/PATCH, e.g. '{"stays_id":"999-999-999","persons":2}'

    Returns JSON response as formatted string, or error details.
    """
    if not API_KEY:
        return "Error: STAYS_API_KEY not configured in environment"

    url = f"{BASE_URL}{path}"
    headers = _build_headers()

    try:
        params = json.loads(query_params) if query_params else {}
    except json.JSONDecodeError:
        return f"Error: invalid JSON in query_params: {query_params}"

    try:
        data = json.loads(body) if body else None
    except json.JSONDecodeError:
        return f"Error: invalid JSON in body: {body}"

    try:
        with httpx.Client(timeout=30) as client:
            method_upper = method.upper()
            if method_upper == "GET":
                resp = client.get(url, headers=headers, params=params)
            elif method_upper == "POST":
                resp = client.post(url, headers=headers, params=params, json=data)
            elif method_upper == "PATCH":
                resp = client.patch(url, headers=headers, params=params, json=data)
            elif method_upper == "DELETE":
                resp = client.delete(url, headers=headers, params=params, json=data)
            else:
                return f"Unsupported HTTP method: {method}. Use GET, POST, PATCH, or DELETE."

        if resp.status_code >= 400:
            return f"HTTP {resp.status_code}\nURL: {url}\nResponse: {resp.text[:2000]}"

        try:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            content_type = resp.headers.get("content-type", "")
            if "xlsx" in content_type or "spreadsheet" in content_type:
                return f"Binary response ({content_type}), {len(resp.content)} bytes received"
            return resp.text[:4000]

    except httpx.RequestError as e:
        return f"Request failed: {type(e).__name__}: {e}"


@mcp.tool()
def stays_get_reservations(from_date: str, to_date: str, date_type: str = "arrival",
                           listing_id: str = "", limit: int = 20, offset: int = 0) -> str:
    """Get reservations from Stays.net for a date range.

    Convenience wrapper around the /external/v1/booking/reservations endpoint.

    Args:
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        date_type: Date filter type. One of: arrival, departure, creation, modification, include
        listing_id: Optional listing identifier to filter
        limit: Max records to return (default 20, max 20)
        offset: Records to skip for pagination (default 0)
    """
    params = {"from": from_date, "to": to_date, "dateType": date_type, "limit": limit}
    if listing_id:
        params["listingId"] = listing_id
    if offset:
        # The API uses 'limit' as offset sometimes, careful with param names
        pass

    if not API_KEY:
        return "Error: STAYS_API_KEY not configured in environment"

    url = f"{BASE_URL}/external/v1/booking/reservations"
    headers = _build_headers()

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(url, headers=headers, params=params)
        if resp.status_code >= 400:
            return f"HTTP {resp.status_code}\nURL: {url}\nResponse: {resp.text[:2000]}"
        try:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            return resp.text[:4000]
    except httpx.RequestError as e:
        return f"Request failed: {type(e).__name__}: {e}"


if __name__ == "__main__":
    mcp.run()
