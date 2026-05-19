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
def stays_api_call(method: str, path: str, query_params: str = "{}", body: str = "{}", confirmed: bool = False) -> str:
    """Make authenticated request to Stays.net API. READ-WRITE for POST/PUT/PATCH.

    GET requests execute immediately.
    POST, PUT, PATCH require explicit user confirmation. Pass confirmed=True after user approval.
    DELETE is permanently blocked.

    Args:
        method: HTTP method (GET, POST, PUT, PATCH)
        path: API path, e.g. '/external/v1/booking/reservations'
        query_params: JSON string of query parameters (for GET)
        body: JSON body as string for POST/PUT/PATCH
        confirmed: Must be True for non-GET operations.

    Returns JSON response as formatted string, or confirmation prompt.
    """
    if not API_KEY:
        return "Error: STAYS_API_KEY not configured in environment"

    method = method.upper()

    if method == "DELETE":
        return "Error: DELETE is permanently blocked for safety."

    if method not in ("GET", "POST", "PUT", "PATCH"):
        return f"Error: Unsupported method '{method}'. Only GET, POST, PUT, PATCH allowed."

    if method != "GET" and not confirmed:
        return (
            f"⚠️ CONFIRMACIÓN REQUERIDA ⚠️\n"
            f"Se detectó una operación de escritura en Stays.net.\n\n"
            f"Método: {method}\n"
            f"Ruta: {path}\n"
            f"Query params: {query_params}\n"
            f"Body: {body}\n\n"
            f"¿Deseas aplicar este cambio? Si es así, vuelve a llamar esta herramienta con confirmed=True."
        )

    url = f"{BASE_URL}{path}"
    headers = _build_headers()

    try:
        with httpx.Client(timeout=30) as client:
            if method == "GET":
                params = json.loads(query_params) if query_params else {}
                resp = client.get(url, headers=headers, params=params)
            else:
                resp = client.request(
                    method, url, headers=headers, content=body.encode("utf-8")
                )

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


# ── Write wrappers ─────────────────────────────────────────────────────

@mcp.tool()
def stays_checkout_initiate(stays_id: str, client_email: str, client_name: str, client_surname: str,
                            persons: int = 1, confirmed: bool = False) -> str:
    """Initiate a checkout/booking process on Stays.net.

    Creates a booking possibility and returns a redirect URL for the guest.
    Requires explicit confirmation (confirmed=True) to execute.

    Args:
        stays_id: Stays apartment identifier (e.g. '999-999-999')
        client_email: Guest email address
        client_name: Guest first name
        client_surname: Guest last name
        persons: Total number of guests (default 1)
        confirmed: Must be True to execute.
    """
    if not API_KEY:
        return "Error: STAYS_API_KEY not configured in environment"

    if not confirmed:
        return (
            "⚠️ CONFIRMACIÓN REQUERIDA ⚠️\n"
            f"Se va a iniciar un checkout en Stays para la propiedad {stays_id}.\n\n"
            f"Huésped: {client_name} {client_surname} ({client_email})\n"
            f"Personas: {persons}\n\n"
            "¿Deseas aplicar este cambio? Vuelve a llamar con confirmed=True."
        )

    payload = json.dumps({
        "stays_id": stays_id,
        "persons": persons,
        "client": {
            "email": client_email,
            "name": client_name,
            "surname": client_surname
        }
    }, ensure_ascii=False)

    url = f"{BASE_URL}/external/checkout/initiate"
    headers = _build_headers()

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, headers=headers, content=payload.encode("utf-8"))
        if resp.status_code >= 400:
            return f"HTTP {resp.status_code}\nURL: {url}\nResponse: {resp.text[:2000]}"
        try:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            return resp.text[:4000]
    except httpx.RequestError as e:
        return f"Request failed: {type(e).__name__}: {e}"


@mcp.tool()
def stays_create_promo_code(name: str, discount_type: str, discount_value: float,
                            status: str = "active", max_uses: int = None,
                            max_uses_per_guest: int = None, confirmed: bool = False) -> str:
    """Create a promo code in Stays.net.

    Requires explicit confirmation (confirmed=True) to execute.

    Args:
        name: Promo code name
        discount_type: "fixed" or "percent"
        discount_value: Discount amount (fixed amount or percentage)
        status: "active" or "inactive" (default active)
        max_uses: How many times the promo code can be used
        max_uses_per_guest: How many times per guest
        confirmed: Must be True to execute.
    """
    if not API_KEY:
        return "Error: STAYS_API_KEY not configured in environment"

    if not confirmed:
        return (
            "⚠️ CONFIRMACIÓN REQUERIDA ⚠️\n"
            f"Se va a crear un promo code en Stays: '{name}'.\n\n"
            f"Tipo: {discount_type}, Valor: {discount_value}, Estado: {status}\n\n"
            "¿Deseas aplicar este cambio? Vuelve a llamar con confirmed=True."
        )

    payload = {
        "name": name,
        "type": discount_type,
        "status": status,
    }
    if discount_type == "percent":
        payload["is_discount"] = discount_value
    else:
        payload["multicurrency"] = {"USD": discount_value}  # Adjust as needed
    if max_uses is not None:
        payload["maxUsesCount"] = max_uses
    if max_uses_per_guest is not None:
        payload["maxUsesCountPerGuest"] = max_uses_per_guest

    payload_str = json.dumps(payload, ensure_ascii=False)
    url = f"{BASE_URL}/external/promocodes/create-promo-code"
    headers = _build_headers()

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, headers=headers, content=payload_str.encode("utf-8"))
        if resp.status_code >= 400:
            return f"HTTP {resp.status_code}\nURL: {url}\nResponse: {resp.text[:2000]}"
        try:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            return resp.text[:4000]
    except httpx.RequestError as e:
        return f"Request failed: {type(e).__name__}: {e}"


@mcp.tool()
def stays_search_listings(from_date: str, to_date: str, guests: int = 1,
                          rooms: int = 1, cities: list = None,
                          properties: list = None, confirmed: bool = False) -> str:
    """Search bookable listings in Stays.net for a certain period.

    This is a POST endpoint. Requires explicit confirmation (confirmed=True) to execute.

    Args:
        from_date: Booking start date (YYYY-MM-DD)
        to_date: Booking end date (YYYY-MM-DD)
        guests: Number of guests (default 1)
        rooms: Number of rooms (default 1)
        cities: Array of city names
        properties: Array of property identifiers
        confirmed: Must be True to execute.
    """
    if not API_KEY:
        return "Error: STAYS_API_KEY not configured in environment"

    if not confirmed:
        return (
            "⚠️ CONFIRMACIÓN REQUERIDA ⚠️\n"
            f"Se va a buscar listings en Stays del {from_date} al {to_date}.\n\n"
            "¿Deseas aplicar este cambio? Vuelve a llamar con confirmed=True."
        )

    payload = {
        "from": from_date,
        "to": to_date,
        "guests": guests,
        "rooms": rooms,
    }
    if cities:
        payload["cities"] = cities
    if properties:
        payload["properties"] = properties

    payload_str = json.dumps(payload, ensure_ascii=False)
    url = f"{BASE_URL}/external/v1/booking/search-listings"
    headers = _build_headers()

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, headers=headers, content=payload_str.encode("utf-8"))
        if resp.status_code >= 400:
            return f"HTTP {resp.status_code}\nURL: {url}\nResponse: {resp.text[:2000]}"
        try:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            return resp.text[:4000]
    except httpx.RequestError as e:
        return f"Request failed: {type(e).__name__}: {e}"


@mcp.tool()
def stays_add_payment(reservation_id: str, amount: float, currency: str = "USD",
                      payment_method: str = "credit_card", confirmed: bool = False) -> str:
    """Add a payment to a reservation in Stays.net.

    Requires explicit confirmation (confirmed=True) to execute.

    Args:
        reservation_id: Reservation identifier
        amount: Payment amount
        currency: Currency code (default USD)
        payment_method: Payment method
        confirmed: Must be True to execute.
    """
    if not API_KEY:
        return "Error: STAYS_API_KEY not configured in environment"

    if not confirmed:
        return (
            "⚠️ CONFIRMACIÓN REQUERIDA ⚠️\n"
            f"Se va a agregar un pago de {amount} {currency} a la reserva {reservation_id}.\n\n"
            "¿Deseas aplicar este cambio? Vuelve a llamar con confirmed=True."
        )

    payload = json.dumps({
        "amount": amount,
        "currency": currency,
        "paymentMethod": payment_method
    }, ensure_ascii=False)

    url = f"{BASE_URL}/v1/bookings/reservations/{reservation_id}/payments"
    headers = _build_headers()

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, headers=headers, content=payload.encode("utf-8"))
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
