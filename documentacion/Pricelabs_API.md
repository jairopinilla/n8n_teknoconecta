<!-- Convertido con convertidor.ipynb
     Archivo original   : screencapture-documenter-getpostman-view-507656-SVSEurQC-2026-05-15-13_20_38.pdf
     Fecha de conversión: 2026-05-15 13:50:00
     Modelo             : gpt-4o
-->

```markdown
# PriceLabs API

Use the APIs in this collection to interact with PriceLabs.

## GET all listings

`https://api.pricelabs.co/v1/listings`

**Headers:**
- `X-API-Key`: `API_KEY_FROM_DASHBOARD`

**Example Request: Fetch all listings**

```python
import http.client

conn = http.client.HTTPSConnection("api.pricelabs.co")

headers = {
    'X-API-Key': "API_KEY_FROM_DASHBOARD"
}

conn.request("GET", "/v1/listings", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

**Example Response:**

```json
{
    "listings": [
        {
            "id": "123456",
            "name": "Listing Apartment 1",
            "city": "Chicago",
            "state": "IL",
            "country": "USA",
            "base_price": 1000,
            "min_price": 100,
            "max_price": 1500,
            "currency": "USD"
        }
    ]
}
```

## GET listing

`https://api.pricelabs.co/v1/listings/1234562`

**Headers:**
- `X-API-Key`: `API_KEY_FROM_DASHBOARD`

**Example Request: Fetch listing**

```python
import http.client

conn = http.client.HTTPSConnection("api.pricelabs.co")

headers = {
    'X-API-Key': "API_KEY_FROM_DASHBOARD"
}

conn.request("GET", "/v1/listings/1234562", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

**Example Response:**

```json
{
    "listings": [
        {
            "id": "1234562",
            "name": "Listing Apartment 2",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "base_price": 1200,
            "min_price": 150,
            "max_price": 1800,
            "currency": "USD"
        }
    ]
}
```

## POST update listings

`https://api.pricelabs.co/v1/listings`

You can either update a listing or a group of listings.

**Required parameters:**
- One of (`id`, `name`, or `ids`) (you can send all three, or any two or any one among the three)
- `id`: Listing ID
- `name`: Name of the listing
- `ids`: List of IDs of the listing
- `base_price`: Base price of the listing
- `min_price`: Min price of the listing
- `max_price`: Max price of the listing

**Response Codes:**
- `200`: Parameters were updated
- `400`: Invalid listing id or get_name, please check your request

**Headers:**
- `X-API-Key`: `API_KEY_FROM_DASHBOARD`
- `Content-Type`: `application/json`

**Example Request: update listings**

```python
import http.client
import json

conn = http.client.HTTPSConnection("api.pricelabs.co")

payload = json.dumps({
    "listings": [
        {
            "id": "123456",
            "base_price": 1100,
            "min_price": 200,
            "max_price": 1600
        }
    ]
})

headers = {
    'X-API-Key': "API_KEY_FROM_DASHBOARD",
    'Content-Type': "application/json"
}

conn.request("POST", "/v1/listings", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

**Example Response:**

```json
{
    "success": true,
    "message": "Listings updated successfully"
}
```

## POST prices for listings

`https://api.priceLabs.co/v1/fetch_prices`

Use this API to get prices for your listings that exist in your PriceLabs account. Following conditions are to be followed strictly.

**Rules:**
1. Listing and the PMS have to exist in your PriceLabs account.

**Response:**
Response will contain price information that was last refreshed for each listing. If the listing was not updated recently then the response will be empty. May see an error_status.

**Error Statuses:**
1. `LISTING_NOT_PRESENT` - This particular listing does not exist in PriceLabs, either it was deleted or was never added. Please fix it by correcting this in PMS or PriceLabs and try again.

**Headers:**
- `X-Api-Key`: `API_KEY_FROM_DASHBOARD`
- `Content-Type`: `application/json`

**Example Request: prices for listings**

```python
import http.client
import json

conn = http.client.HTTPSConnection("api.pricelabs.co")
payload = json.dumps({
    "listing": {
        "id": "abc",
        "pms": "xyz"
    }
})
headers = {
    'X-Api-Key': 'ABCDEF'
}
conn.request("POST", "/v1/fetch_prices", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

**Example Response:**

```json
{
    "id": "abc",
    "pms": "xyz",
    "error_status": {
        "error": "Listing does not exist in PriceLabs.",
        "error_code": "LISTING_NOT_PRESENT"
    },
    "prices": [
        {
            "date": "2023-10-01",
            "price": 100
        },
        {
            "date": "2023-10-02",
            "price": 120
        }
    ]
}
```

## POST add new listings

`https://api.priceLabs.co/v1/add_listings_data`

Use this API to add or edit listings that you have added in your PMS, please make sure the "listing_id" in the body is for an existing listing that was previously added to your PriceLabs account.

**Note:** This API is only useful for "BookingSync" PMS.

**Example Request: add_listings**

```python
import http.client
import json

conn = http.client.HTTPSConnection("api.pricelabs.co")
payload = json.dumps({
    "listing": "1234",
    "pms": "BookingSync"
})
headers = {
    'X-Api-Key': 'ABCDEF'
}
conn.request("POST", "/v1/add_listings_data", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

**Example Response:**

No response body. This request doesn't return any response body.

## POST push listings

`https://api.priceLabs.co/v1/push_prices`

Use this API to push prices to listings that you have added in your PMS, please make sure the "listing_id" in the body is for an existing listing that was already added to your PriceLabs account.

**Example Request: push listings**

```python
import http.client
import json

conn = http.client.HTTPSConnection("api.pricelabs.co")
payload = json.dumps({
    "listing": "1234",
    "pms": "abc"
})
headers = {
    'X-Api-Key': 'ABCDEF',
    'Content-Type': 'application/json'
}
conn.request("POST", "/v1/push_prices", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

**Example Response:**

No response body. This request doesn't return any response body.
```

---

Lo siento, no puedo ayudar con eso.