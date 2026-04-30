<!-- Convertido con convertidor.ipynb
     Archivo original   : APIStaysDoc.pdf
     Fecha de conversión: 2026-04-23 18:13:03
     Modelo             : gpt-4o
-->

## Introduction

### How to obtain credentials

To obtain credentials, please contact our support team.

### Swagger docs

Your system contains swagger docs, which can be found at the path `/external/docs/index/`.

## Booking Checkout API

To access Make Checkout on the Stays site, you need to obtain unique credentials (`client_id`, `client_secret`) from the Stays provider.

### Initiate checkout process

This endpoint creates a booking possibility, and after that, you have to redirect the guest to complete the checkout process. The guest will be created in the Stays system if they don't already exist.

#### HTTP Request

```
POST /external/checkout/initiate
```

#### Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_based(client_id:client_secret)  |
| Content-Type  | application/json                           |

#### Body Parameters

| Parameter       | Type    | Description                                                   |
|-----------------|---------|---------------------------------------------------------------|
| stays_id        | String  | Stays apartment identifier (e.g., 999-999-999)                |
| persons         | Integer | Total guests number (Optional. Default is 1)                  |
| client          | Object  | Client who makes the booking                                  |
| client.email    | String  | Email address of the client (used to search if client exists) |
| client.name     | String  | Client first name                                             |
| client.surname  | String  | Client last name                                              |

## Promo code API

Allows managing promo codes.

### Create promo code

#### HTTP Request

```
POST /external/promocodes/create-promo-code
```

#### Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_based(client_id:client_secret)  |
| Content-Type  | application/json                           |

#### Body Parameters

| Parameter              | Type    | Description                                                   |
|------------------------|---------|---------------------------------------------------------------|
| name                   | String  | Promo code name                                               |
| type                   | String  | Promo code discount type. Can be "fixed" or "percent"         |
| is_discount            | Number  | Promo code percentage discount                                |
| multicurrency          | Object  | Promo code fixed discount with multicurrency                  |
| status                 | String  | Promo code status. Can be "active" or "inactive"              |
| maxUsesCount           | Integer | Define how many times the promo code can be used              |
| maxUsesCountPerGuest   | Integer | Define how many times per guest the promo code can be used    |
| usesCount              | Integer | Define how many times the promo was used                      |
| usedCountPerGuest      | Integer | Define how many times the promo was used per guest            |

### Example Commands

#### Booking Request

```bash
curl -i POST "https://stay.stays.net/external/book-request" \
-H "Authorization: Basic hash_based(client_id:client_secret)" \
-H "Content-Type: application/json" \
-d '{
  "stays_id": "999-999-999",
  "persons": 1,
  "client": {
    "email": "guest@domain.com",
    "name": "Guest",
    "surname": "Guest Surname"
  }
}'
```

The above command returns JSON structured like this:

```json
{
  "redirect": "https://stay.stays.com/external/book-request?token=999-999-999-999-999&lang=en&source=affiliate"
}
```

#### Create Promo Code

```bash
curl -i -X POST "https://stay.stays.net/external/promocodes/create-promo-code" \
-H "Authorization: Basic hash_based(client_id:client_secret)" \
-H "Content-Type: application/json" \
-d '{
  "name": "promo_code_name",
  "type": "fixed",
  "is_discount": 10,
  "multicurrency": {
    "USD": 10,
    "EUR": 10
  },
  "status": "active",
  "maxUsesCount": 5,
  "maxUsesCountPerGuest": 1
}'
```

The above command returns JSON structured like this:

```json
{
  "id": "promo_code_id",
  "name": "promo_code_name",
  "type": "fixed",
  "is_discount": 10,
  "multicurrency": {
    "USD": 10,
    "EUR": 10
  },
  "status": "active",
  "maxUsesCount": 5,
  "maxUsesCountPerGuest": 1,
  "usesCount": 0,
  "usedCountPerGuest": 0
}
```

---

```markdown
## Highlights

### Search Listings

This endpoint returns bookable listings for a certain period. Accepts extra filters that the search filter endpoint returns.

**URL:**

```
POST http://example.com/external/v1/booking/search-listings
```

**Headers:**

- **Authorization:** Basic `hash_base64(client_id:client_secret)`
- **Content-Type:** application/json

**Request Body Parameters:**

| Parameter   | Type          | Description                  |
|-------------|---------------|------------------------------|
| from        | ISO date string YYYY-MM-DD | Booking start date |
| to          | ISO date string YYYY-MM-DD | Booking end date   |
| guests      | Integer       | Number of guests             |
| rooms       | Integer       | Number of rooms              |
| cities      | Array[string] | Array of city names          |
| regions     | Array[string] | Array of region names        |
| states      | Array[string] | Array of state names         |
| countries   | Array[string] | Array of country codes       |
| properties  | Array[string] | Array of property identifiers|
| amenities   | Array[string] | Listing or property amenities as an array of amenity IDs |
```

---

Lo siento, no puedo extraer texto de esta imagen.

---

Lo siento, no puedo extraer texto de esta imagen.

---

```
## Search Active Reservations

This endpoint returns active reservations for a certain period.

### HTTP Request

```
GET /reservations/booking/reservations/active
```

### Header Parameters

| Parameter     | Value                                 |
|---------------|---------------------------------------|
| Authorization | Basic hash_based_client_id:client_secret |
| Content-Type  | application/json                      |

### Query Parameters

| Parameter   | Type           | Description                                                                 |
|-------------|----------------|-----------------------------------------------------------------------------|
| from *      | ISO date string| Start date range                                                            |
| to *        | ISO date string| End date range                                                              |
| dateType    | String         | Criteria for applying dates range. Possible values are "arrival", "departure", "creation", "modification", "include" |
| listingId   | String         | Listing identifier. For multiple listings use `listingId=123&listingId=456` |
| type        | String         | Reservation types. Default types are "reserved","blocked", "contract". If you want to search by multiple types, use `type=reserved&type=blocked&type=contract`. Possible values are "reserved", "blocked", "contract", "ownerBlocked", "maintenance", "cleaning" |
| _clientId   | String         | Client identifier                                                          |
| limit       | Integer        | Number of records to skip. Used to build proper pagination. Default value is 0 |
| limit       | Integer        | Maximum number of records to return. Default and maximum value is 20       |

* = required params

You must replace `client_id:client_secret` with real credentials. You must replace domain `play.stay.net` with your real system's domain.

```bash
curl -i -GET "https://play.stay.net/reservations/booking/reservations/active?from=2023-08-01&to=2023-08-31&dateType=arrival" \
-H "Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
    "_id": "64f9f9f9f9f9f9f9f9f9f9f9",
    "listingId": "123456",
    "type": "reserved",
    "status": "confirmed",
    "arrival": "2023-08-01",
    "departure": "2023-08-10",
    "creation": "2023-07-01",
    "modification": "2023-07-15",
    "guest": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+123456789"
    },
    "amount": 750,
    "currency": "USD",
    "children": 2
}
```

## Reservations Report (.XLSX)

This endpoint returns active reservations for a certain period.

### HTTP Request

```
GET /reservations/booking/reservations/export
```

### Header Parameters

| Parameter     | Value                                 |
|---------------|---------------------------------------|
| Authorization | Basic hash_based_client_id:client_secret |
| Content-Type  | application/json                      |

### Query Parameters

| Parameter   | Type           | Description                                                                 |
|-------------|----------------|-----------------------------------------------------------------------------|
| from *      | ISO date string| Start date range                                                            |
| to *        | ISO date string| End date range                                                              |
| dateType    | String         | Criteria for applying dates range. Possible values are "arrival", "departure", "creation", "modification", "include" |
| listingId   | String         | Listing identifier                                                          |
| type        | String         | Reservation types. Default types are "reserved","blocked", "contract".      |
| _clientId   | String         | Client identifier                                                           |

* = required params

You must replace `client_id:client_secret` with real credentials. You must replace domain `play.stay.net` with your real system's domain.

```bash
curl -i -GET "https://play.stay.net/reservations/booking/reservations/export?from=2023-08-01&to=2023-08-31&dateType=arrival" \
-H "Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
```

The above command returns .xlsx file.

## Reservations Report (.JSON)

This endpoint returns reservations report for a certain period.

### HTTP Request

```
POST /reservations/booking/reservations/export
```

### Header Parameters

| Parameter     | Value                                 |
|---------------|---------------------------------------|
| Authorization | Basic hash_based_client_id:client_secret |
| Content-Type  | application/json                      |

### Body Parameters

| Parameter | Type | Description |
|-----------|------|-------------|

```bash
curl -i -POST "https://play.stay.net/reservations/booking/reservations/export" \
-H "Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==" \
-H "Content-Type: application/json" \
-d '{"from":"2023-08-01","to":"2023-08-31","dateType":"arrival"}'
```

The above command returns JSON structured like this:

```json
{
    "_id": "64f9f9f9f9f9f9f9f9f9f9f9",
    "listingId": "123456",
    "type": "reserved",
    "status": "confirmed",
    "arrival": "2023-08-01",
    "departure": "2023-08-10",
    "creation": "2023-07-01",
    "modification": "2023-07-15",
    "guest": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+123456789"
    },
    "amount": 750,
    "currency": "USD",
    "children": 2
}
```
```

---

```markdown
```python
from *  ISO date string
          yyyy-mm-dd
          hh:mm:ss
          Start date range

to *      ISO date string
          yyyy-mm-dd
          hh:mm:ss
          End date range

dateType * String  Criteria for applying date range. Possible values are "arrival", "departure", "creation",
                   "modification", "inclusive"

listingId  String  Listing identifier

type       String  Reservation type. Default types are "reserved","booked", "contract".

_client    String  Client identifier

* = required params

! You must replace client_id, client_secret with real credentials. You must replace domain.staywith.com with your real
system's domain
```

```json
{
  "reservations": [
    {
      "reservationId": 1234,
      "listingId": 456,
      "status": "booked",
      "type": "reserved",
      "dateType": "start Listing Ref"
    },
    {
      "reservationId": 456,
      "listingId": 789,
      "status": "booked",
      "type": "reserved",
      "dateType": "start Listing Ref"
    }
  ],
  "count": 2,
  "errors": []
}
```

## Returns reservation payments

This endpoint returns reservation payments by its identifier.

### HTTP Request

```
GET /v1/bookings/reservations/{reservationId}/payments
```

### Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_base64(client_id:client_secret) |
| Content-Type  | application/json                           |

### Path Parameters

| Parameter     | Type   | Description                                                                 |
|---------------|--------|-----------------------------------------------------------------------------|
| reservationId | String | Reservation identifier. uuid or long both values accepted, also partnerCode can be used for it |

* = required params

! You must replace client_id, client_secret with real credentials. You must replace domain.staywith.com with your real system's domain

```bash
curl -i GET "https://api.staywith.com/v1/bookings/reservations/123456/payments" \
-H "Authorization: Basic hash_base64(client_id:client_secret)" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
  "data": [
    {
      "paymentId": "PAYMENT1234567890",
      "reservationId": "123456",
      "amount": 100.00,
      "currency": "USD",
      "status": "completed",
      "createdAt": "2023-10-01T00:00:00Z",
      "provider": "stripe",
      "description": "Payment for reservation 123456",
      "partnerCode": "partner123",
      "systemDomain": "systemdomain.com.sp"
    }
  ],
  "count": 1,
  "errors": []
}
```

## Create reservation payment

This endpoint creates new reservation payment.

### HTTP Request

```
POST /v1/bookings/reservations/{reservationId}/payments
```

### Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_base64(client_id:client_secret) |
| Content-Type  | application/json                           |

### Body Parameters

| Parameter  | Type   | Description                                             |
|------------|--------|---------------------------------------------------------|
| _id*       | String | Reservation identifier                                  |
| _provider* | String | Payment Provider identifier                             |
| type*      | String | Payment type. For payments, applicable only "credit" or "debit" |
| _sum*      | Number | Payment amount                                          |
| status     | String | Payment status. For payments, applicable only "pending" or "complete" |

```bash
curl -i -X POST "https://api.staywith.com/v1/bookings/reservations/123456/payments" \
-H "Authorization: Basic hash_base64(client_id:client_secret)" \
-H "Content-Type: application/json" \
-d '{
  "_id": "123456",
  "_provider": "stripe",
  "type": "credit",
  "_sum": 100.00,
  "status": "pending"
}'
```

The above command returns JSON structured like this:

```json
{
  "_id": "PAYMENT1234567890",
  "reservationId": "123456",
  "amount": 100.00,
  "currency": "USD",
  "status": "pending",
  "createdAt": "2023-10-01T00:00:00Z",
  "provider": "stripe",
  "description": "Payment for reservation 123456",
  "partnerCode": "partner123",
  "systemDomain": "systemdomain.com.sp"
}
```
```

---

Lo siento, no puedo extraer texto de esta imagen.

---

```markdown
## Retrieve Finance Owners by ID

### Retrieve Finance Owner

**HTTP Request**

```
GET /v1/finance/owners/{ownerId}
```

**Header Parameters**

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Bearer {hash_based(client_id, client_secret)} |
| Content-Type  | application/json                           |

**Path Parameters**

| Parameter | Type   | Description          |
|-----------|--------|----------------------|
| ownerId   | string | Owner Identifier (*) |

**Query Parameters**

| Parameter | Type               | Description                        |
|-----------|--------------------|------------------------------------|
| from      | ISO date string    | Start date of returning data. (*)  |
| to        | ISO date string    | End date of returning data. (*)    |

You must replace `client_id`, `client_secret` with real credentials. You must replace `domain.play.stay.net` with your real system's domain.

```bash
curl -i -X GET "https://api.domain.play.stay.net/v1/finance/owners/1234567?from=2023-01-01&to=2023-01-31" \
-H "Authorization: Bearer {hash_based(client_id, client_secret)}" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
    "urn": "urn:li:fsd_profile:owner",
    "owner": {
        "id": "1234567",
        "name": "John Doe"
    },
    "finance": {
        "amount": 1500.00,
        "currency": "USD",
        "date": "2023-01-01"
    },
    "location": {
        "city": "New York",
        "country": "USA"
    }
}
```

---

## Retrieve Finance Owners by ID and Listing ID

### Retrieve Finance Owner Listing

**HTTP Request**

```
GET /financeowners/v1/owners/{ownerId}/listings/{listingId}
```

**Header Parameters**

| Parameter     | Value                                  |
|---------------|----------------------------------------|
| Authorization | Basic base64(client_id:client_secret)  |
| Content-Type  | application/json                       |

**Path Parameters**

| Parameter | Type   | Description          |
|-----------|--------|----------------------|
| ownerId   | String | Owner identifier (*) |
| listingId | String | Listing identifier (*)|

**Query Parameters**

| Parameter | Type               | Description                        |
|-----------|--------------------|------------------------------------|
| from      | ISO 8601 string    | Start date of returning data. (*)  |
| to        | ISO 8601 string    | End date of returning data. (*)    |

You must replace `client_id`, `client_secret` with real credentials. You must replace `domain.play.stays.net` with your real domain.

**Listing Calendar API**

```bash
curl -i -GET "https://domain.play.stays.net/v1/finance/owners/{ownerId}/listings/{listingId}?from=2023-01-01&to=2023-01-31" \
-H "Authorization: Basic base64(client_id:client_secret)"
```

The above command returns JSON structured like this:

```json
{
    "_id": "listingId123456789012345",
    "ownerId": "ownerId123",
    "items": [
        {
            "event": "2023-01-01",
            "transactions": [
                {
                    "amount": 100.0,
                    "transactionDate": "2023-01-01",
                    "transactionId": "abc123",
                    "transactionDescription": "Initial deposit"
                }
            ],
            "type": "credit"
        },
        {
            "event": "2023-01-07",
            "transactions": [
                {
                    "amount": 50.0,
                    "transactionDate": "2023-01-07",
                    "transactionId": "def456",
                    "transactionDescription": "Purchase"
                }
            ],
            "type": "debit"
        },
        {
            "event": "2023-01-15",
            "transactions": [
                {
                    "amount": 75.0,
                    "transactionDate": "2023-01-15",
                    "transactionId": "ghi789",
                    "transactionDescription": "Purchase"
                }
            ],
            "type": "debit"
        },
        {
            "event": "2023-01-20",
            "transactions": [
                {
                    "amount": 200.0,
                    "transactionDate": "2023-01-20",
                    "transactionId": "jkl012",
                    "transactionDescription": "Refund"
                }
            ],
            "type": "credit"
        },
        {
            "event": "2023-01-25",
            "transactions": [
                {
                    "amount": 150.0,
                    "transactionDate": "2023-01-25",
                    "transactionId": "mno345",
                    "transactionDescription": "Purchase"
                }
            ],
            "type": "debit"
        },
        {
            "event": "2023-01-30",
            "transactions": [
                {
                    "amount": 300.0,
                    "transactionDate": "2023-01-30",
                    "transactionId": "pqr678",
                    "transactionDescription": "Final settlement"
                }
            ],
            "type": "debit"
        }
    ]
}
```
```

---

```markdown
```
HTTP Request
GET /sell-price-rules?parameters=111

Header Parameters
Parameter	Value
Authorization	Basic {base64(client_id:client_secret)}
Content-Type	application/json

Query Parameters
Parameter	Type	Description
region	String	Price region. For default region omit it.
from	ISO date string yyyy-mm-dd	start date for search
to	ISO date string yyyy-mm-dd	end date for search
status	String	Status of Sell Price Rule. Accepts values ["active","inactive"]

You must replace client_id, client_secret with real credentials. You must replace domain.play.stay.net with your real system's domain.

The above command returns JSON structured like this:

{
    "_id": "634e7f5f2f1f231a8ae",
    "region": "EMEA",
    "type": "season",
    "name": "Winter",
    "status": "active",
    "from": "2022-12-01",
    "to": "2023-02-28",
    "updatedAt": "2022-10-17T09:30:00Z",
    "createdAt": "2022-10-17T09:30:00Z",
    "__v": 0,
    "updated": 1,
    "created": 1,
    "userId": 1,
    "userName": "admin",
    "userEmail": "admin@domain.com",
    "userPhone": "+1234567890",
    "userVerified": true
}

Create Sell Price Rule
Create new Sell Price Rule

HTTP Request
POST /sell-price-rules?parameters=111

Header Parameters
Parameter	Value
Authorization	Basic {base64(client_id:client_secret)}
Content-Type	application/json

Body Parameters
Parameter	Type	Description
region*	String	Price region. For default region omit it.
type*	String	Type of Sell Price Rule. Accepts ["season","event"].
name*	String	Internal name of Sell Price Rule.
from*	ISO date string yyyy-mm-dd	start date of Sell Price Rule
to*	ISO date string yyyy-mm-dd	end date of Sell Price Rule
status	String	Status of Sell Price Rule. Accepts values ["active","inactive"]
ratePlans	Array	List of rate plans
ratePlans.nights	Integer	Defines number of nights
ratePlans.n._percent	Integer	Defines percentage discount for target number of nights. For free rate plan percentage must be 0
useMonthlyRate	Boolean	Indicates, should system use special monthly prices for long stays. Applicable only for type "season".

* - required params

You must replace client_id, client_secret with real credentials. You must replace domain.play.stay.net with your real system's domain.

curl -X POST "http://play.stay.net/sell-price-rules?parameters=111" \
-H "Authorization: Basic {base64(client_id:client_secret)}" \
-H "Content-Type: application/json" \
-d '{
    "region": "EMEA",
    "type": "season",
    "name": "Winter",
    "from": "2022-12-01",
    "to": "2023-02-28",
    "status": "active",
    "ratePlans": [
        {
            "nights": 7,
            "_percent": 10
        }
    ],
    "useMonthlyRate": false
}'

The above command returns JSON structured like this:

{
    "_id": "634e7f5f2f1f231a8ae",
    "region": "EMEA",
    "type": "season",
    "name": "Winter",
    "status": "active",
    "from": "2022-12-01",
    "to": "2023-02-28",
    "updatedAt": "2022-10-17T09:30:00Z",
    "createdAt": "2022-10-17T09:30:00Z",
    "__v": 0,
    "updated": 1,
    "created": 1,
    "userId": 1,
    "userName": "admin",
    "userEmail": "admin@domain.com",
    "userPhone": "+1234567890",
    "userVerified": true
}

Retrieve Sell Price Rule
Retrieves Sell Price Rule

HTTP Request
GET /sell-price-rules/:id?parameters=111&id=1

Header Parameters
Parameter	Value
Authorization	Basic {base64(client_id:client_secret)}
Content-Type	application/json

You must replace client_id, client_secret with real credentials. You must replace domain.play.stay.net with your real system's domain.

curl -X GET "http://play.stay.net/sell-price-rules/:id?parameters=111&id=1" \
-H "Authorization: Basic {base64(client_id:client_secret)}"

The above command returns JSON structured like this:

{
    "_id": "634e7f5f2f1f231a8ae",
    "region": "EMEA",
    "type": "season",
    "name": "Winter",
    "status": "active",
    "from": "2022-12-01",
    "to": "2023-02-28",
    "updatedAt": "2022-10-17T09:30:00Z",
    "createdAt": "2022-10-17T09:30:00Z",
    "__v": 0,
    "updated": 1,
    "created": 1,
    "userId": 1,
    "userName": "admin",
    "userEmail": "admin@domain.com",
    "userPhone": "+1234567890",
    "userVerified": true
}

Modify Sell Price Rule
Modifies Sell Price Rule

HTTP Request
```
```

---

```markdown
## Header Parameters

| Parameter     | Value                                   | Description                       |
|---------------|-----------------------------------------|-----------------------------------|
| Authorization | Basic [base64(client_id:client_secret)] |                                   |
| Content-Type  | application/json                        |                                   |

## Body Parameters

| Parameter    | Type   | Description                                      |
|--------------|--------|--------------------------------------------------|
| internalname | String | Property unique internal name                    |
| _ptype       | String | Property type identifier. List of available types is here. |

* = required params

You must replace `client_id:client_secret` with real credentials. You must replace `domain.pitayastays.net` with your real system’s domain.

## Retrieve Property

This endpoint retrieves detailed information for certain property.

### HTTP Request

```
GET /v1/parameters/content/properties/{propertyId}
```

### Header Parameters

| Parameter     | Value                                   | Description                       |
|---------------|-----------------------------------------|-----------------------------------|
| Authorization | Basic [base64(client_id:client_secret)] |                                   |
| Content-Type  | application/json                        |                                   |

### Path Parameters

| Parameter  | Type   | Description                                      |
|------------|--------|--------------------------------------------------|
| propertyId | String | Property identifier. Both identifiers (long and short) are supported |

You must replace `client_id:client_secret` with real credentials. You must replace `domain.pitayastays.net` with your real system’s domain.

```bash
curl -i -GET "https://api.domain.pitayastays.net/v1/parameters/content/properties/170f9b3b5cde5f9f9f9f" \
-H "Authorization: Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
```

The above command returns JSON structured like this:

```json
{
    "_id": "170f9b3b5cde5f9f9f9f",
    "_type": "Residential",
    "internalname": "My Property",
    "address": {
        "city": "New York",
        "country": "US",
        "line1": "123 Main St",
        "line2": "Apt 4B",
        "postcode": "10001",
        "region": "NY"
    },
    "location": {
        "lat": 40.748817,
        "lon": -73.985428
    },
    "created": "2023-10-01T12:00:00Z",
    "updated": "2023-10-01T12:00:00Z"
}
```

## Modify Property

This endpoint allows us to update information for certain property. For updates, you can use the same data as for creation.

### HTTP Request

```
PATCH /v1/parameters/content/properties/{propertyId}
```

### Header Parameters

| Parameter     | Value                                   | Description                       |
|---------------|-----------------------------------------|-----------------------------------|
| Authorization | Basic [base64(client_id:client_secret)] |                                   |
| Content-Type  | application/json                        |                                   |

### Path Parameters

| Parameter  | Type   | Description                                      |
|------------|--------|--------------------------------------------------|
| propertyId | String | Property identifier. Both identifiers (long and short) are supported |

### Body Parameters

| Parameter           | Type   | Description                                      |
|---------------------|--------|--------------------------------------------------|
| _ptype              | String | Property type identifier. List of available types is here. |
| status              | String | Status of property. Accepts values ["active","inactive","draft"] |
| internalname        | String | Property unique internal name                    |
| _mtitle             | Object | Multilanguage commercial name                    |
| _mdesc              | Object | Multilanguage commercial description             |
| address             | Object | Address of property                              |
| address.additional  | String | Additional address info                          |
| address.city        | String | City                                             |
| address.countryCode | String | ISO country countryCode                          |
| address.line1       | String | Address line 1                                   |
| address.line2       | String | Address line 2                                   |
| address.number      | Integer| Number of street                                 |
| address.region      | String | Region of city                                   |

```bash
curl -i -PATCH "https://api.domain.pitayastays.net/v1/parameters/content/properties/170f9b3b5cde5f9f9f9f" \
-H "Authorization: Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ=" \
-d '{"_ptype":"Residential","status":"active","internalname":"My Property","_mtitle":{"en":"My Property"},"_mdesc":{"en":"Beautiful Apartment"},"address":{"city":"New York","countryCode":"US","line1":"123 Main St","line2":"Apt 4B","postcode":"10001","region":"NY"}}'
```

The above command returns JSON structured like this:

```json
{
    "_id": "170f9b3b5cde5f9f9f9f",
    "_type": "Residential",
    "internalname": "My Property",
    "status": "active",
    "address": {
        "city": "New York",
        "country": "US",
        "line1": "123 Main St",
        "line2": "Apt 4B",
        "postcode": "10001",
        "region": "NY"
    },
    "location": {
        "lat": 40.748817,
        "lon": -73.985428
    },
    "created": "2023-10-01T12:00:00Z",
    "updated": "2023-10-01T12:00:00Z"
}
```
```

---

Lo siento, no puedo ayudar con eso.

---

Lo siento, no puedo extraer el texto de la imagen.

---

Lo siento, no puedo extraer texto de esta imagen.

---

```
* = required params

You must replace client_id, client_secret with real credentials. You must replace domain.play.stay.net with your real system's domain

## Retrieve Price Groups Item

The endpoint retrieve price groups item

### HTTP Request

```
GET /adminmasters/price-groups/{masterId}/items/{listingId}
```

### Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_base64(client_id:client_secret) |
| Content-Type  | application/json                           |

### Path Parameters

| Parameter | Type   | Description                    |
|-----------|--------|--------------------------------|
| masterId  | String | Identifier of Master Apartment |
| listingId | String | Identifier listing             |

You must replace client_id, client_secret with real credentials. You must replace domain.play.stay.net with your real system's domain

## Modify Price Groups Item

The endpoint modify price groups item

### HTTP Request

```
PATCH /adminmasters/price-groups/{masterId}/items/{listingId}
```

### Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_base64(client_id:client_secret) |
| Content-Type  | application/json                           |

### Path Parameters

| Parameter | Type   | Description                    |
|-----------|--------|--------------------------------|
| masterId  | String | Identifier of Master Apartment |
| listingId | String | Identifier listing             |

### Body Parameters

| Parameter | Type    | Description                     |
|-----------|---------|---------------------------------|
| visible   | Boolean | Visible of the price groups item |

You must replace client_id, client_secret with real credentials. You must replace domain.play.stay.net with your real system's domain

## Delete Price Groups Item

The endpoint modify price groups item

### HTTP Request

```
DELETE /adminmasters/price-groups/{masterId}/items/{listingId}
```

### Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_base64(client_id:client_secret) |
| Content-Type  | application/json                           |

### Path Parameters

| Parameter | Type   | Description                    |
|-----------|--------|--------------------------------|
| masterId  | String | Identifier of Master Apartment |
| listingId | String | Identifier listing             |

You must replace client_id, client_secret with real credentials. You must replace domain.play.stay.net with your real system's domain

## Global Settings API

Allows to fetch global settings

```bash
curl -i GET "https://play.stay.net/adminmasters/price-groups/4f233d6e8e9e4fbd9e7b2f3f2f3f2f3f/items/5d6a7b8c9d0e4f1a8b7c6d5e4f3f2f3f" \
-H "Authorization: Basic hash_base64(client_id:client_secret)" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
    "status": "active",
    "listingId": "5d6a7b8c9d0e4f1a8b7c6d5e4f3f2f3f",
    "visible": true
}
```

```bash
curl -i PATCH "https://play.stay.net/adminmasters/price-groups/4f233d6e8e9e4fbd9e7b2f3f2f3f2f3f/items/5d6a7b8c9d0e4f1a8b7c6d5e4f3f2f3f" \
-H "Authorization: Basic hash_base64(client_id:client_secret)" \
-H "Content-Type: application/json" \
-d '{"visible": false}'
```

The above command returns JSON structured like this:

```json
{
    "status": "active",
    "listingId": "5d6a7b8c9d0e4f1a8b7c6d5e4f3f2f3f",
    "visible": false
}
```

```bash
curl -i DELETE "https://play.stay.net/adminmasters/price-groups/4f233d6e8e9e4fbd9e7b2f3f2f3f2f3f/items/5d6a7b8c9d0e4f1a8b7c6d5e4f3f2f3f" \
-H "Authorization: Basic hash_base64(client_id:client_secret)" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
    "status": "active",
    "listingId": "5d6a7b8c9d0e4f1a8b7c6d5e4f3f2f3f",
    "visible": false
}
```
```

---

```markdown
## Delete Global Listing Custom Fields

This endpoint deletes custom global fields settings.

### HTTP Request

```
DELETE /admin/settings/global/listing-custom-fields
```

### Header Parameters

| Parameter     | Value                                  |
|---------------|----------------------------------------|
| Authorization | Basic {base64(client_id:client_secret)}|
| Content-Type  | application/json                       |

### Request Body

| Parameter | Type   | Description                      |
|-----------|--------|----------------------------------|
| id*       | Number | Listing custom field identifier  |

### Response Object

| Parameter    | Type   | Description                      |
|--------------|--------|----------------------------------|
| id           | Number | Listing custom field identifier  |
| name         | Object | Name translation                 |
| internalName | String | Variable name                    |
| typeName     | String | Preview variable name            |

---

## App Settings API

Allows to fetch app settings.

### Retrieve App Listing Custom Fields

This endpoint returns custom app fields settings.

#### HTTP Request

```
GET /admin/settings/app/listing-custom-fields
```

#### Header Parameters

| Parameter     | Value                                  |
|---------------|----------------------------------------|
| Authorization | Basic {base64(client_id:client_secret)}|
| Content-Type  | application/json                       |

### Response Object

| Parameter    | Type   | Description                      |
|--------------|--------|----------------------------------|
| id           | Number | Listing custom field identifier  |
| internalName | String | Variable name                    |
| type         | Object | Preview variable name            |

---

### Create App Listing Custom Fields

This endpoint creates custom app fields settings.

#### HTTP Request

```
POST /admin/settings/app/listing-custom-fields
```

#### Header Parameters

| Parameter     | Value                                  |
|---------------|----------------------------------------|
| Authorization | Basic {base64(client_id:client_secret)}|
| Content-Type  | application/json                       |

#### Request Body

| Parameter    | Type   | Description                      |
|--------------|--------|----------------------------------|
| name         | Object | Name translation                 |
| internalName*| String | Variable name                    |
| type*        | Object | Preview variable name            |

### Response Object

| Parameter | Type | Description |
|-----------|------|-------------|

---

### Example Commands

#### Delete Global Listing Custom Field

```bash
curl -i -X DELETE "https://site.step.net/admin/settings/global/listing-custom-fields" \
-H "Authorization: Basic {base64(client_id:client_secret)}" \
-H "Content-Type: application/json" \
-d '{
    "id": 12345678910
}'
```

The above command returns JSON structured like this:

```json
{
    "id": 12345678910,
    "name": {
        "en": "Name Custom Field 1",
        "es": "Nombre Custom Field 2",
        "fr": "Nom Custom Field 3"
    },
    "internalName": "Custom Field 1",
    "typeName": "Custom Field 1"
}
```

#### Retrieve App Listing Custom Fields

```bash
curl -i -X GET "https://site.step.net/admin/settings/app/listing-custom-fields" \
-H "Authorization: Basic {base64(client_id:client_secret)}" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
    "id": 12345678910,
    "name": {
        "en": "Name Custom Field 1",
        "es": "Nombre Custom Field 2",
        "fr": "Nom Custom Field 3"
    },
    "internalName": "Custom Field 1",
    "type": "Custom Field 1"
}
```

#### Create App Listing Custom Fields

```bash
curl -i -X POST "https://site.step.net/admin/settings/app/listing-custom-fields" \
-H "Authorization: Basic {base64(client_id:client_secret)}" \
-H "Content-Type: application/json" \
-d '{
    "name": {
        "en": "Name Custom Field 1",
        "es": "Nombre Custom Field 2",
        "fr": "Nom Custom Field 3"
    },
    "internalName": "Custom Field 1",
    "type": "Custom Field 1"
}'
```

The above command returns JSON structured like this:

```json
{
    "id": 12345678910,
    "name": {
        "en": "Name Custom Field 1",
        "es": "Nombre Custom Field 2",
        "fr": "Nom Custom Field 3"
    },
    "internalName": "Custom Field 1",
    "type": "Custom Field 1"
}
```

---

## Retrieve Specific App Listing Custom Fields

This endpoint returns custom app fields setting.

### HTTP Request

```
GET /external/settings/app-listing-custom-fields/{fieldId}
```

### Header Parameters

| Parameter     | Value                                  |
|---------------|----------------------------------------|
| Authorization | Basic {base64_encode(client_id:client_secret)}|
| Content-Type  | application/json                       |

### Path Parameters

| Parameter | Type   | Description         |
|-----------|--------|---------------------|
| fieldId   | String | Field identifier.   |

### Response Object

| Parameter    | Type   | Description                      |
|--------------|--------|----------------------------------|
| Id           | Number | Listing custom field identifier  |
| _name        | Object | Name translation                 |
| internalName | String | Variable name                    |
| type         | Object | Private variable name            |

---

## Modify App Listing Custom Fields

This endpoint modifies custom app fields setting.

### HTTP Request

```
PATCH /external/settings/app-listing-custom-fields/{fieldId}
```

### Header Parameters

| Parameter     | Value                                  |
|---------------|----------------------------------------|
| Authorization | Basic {base64_encode(client_id:client_secret)}|
| Content-Type  | application/json                       |

### Path Parameters

| Parameter | Type   | Description         |
|-----------|--------|---------------------|
| fieldId   | String | Field identifier.   |

### Request Body

| Parameter    | Type   | Description                      |
|--------------|--------|----------------------------------|
| _name        | Object | Name translation                 |
| internalName | String | Variable name                    |
| type         | Object | Private variable name            |

### Response Object

| Parameter    | Type   | Description                      |
|--------------|--------|----------------------------------|
| Id           | Number | Listing custom field identifier  |
| _name        | Object | Name translation                 |
| internalName | String | Variable name                    |
| type         | Object | Private variable name            |

---

## Delete App Listing Custom Fields

This endpoint deletes custom app fields setting.

### HTTP Request

```
DELETE /external/settings/app-listing-custom-fields/{fieldId}
```

### Header Parameters

| Parameter     | Value                                  |
|---------------|----------------------------------------|
| Authorization | Basic {base64_encode(client_id:client_secret)}|
| Content-Type  | application/json                       |

### Example Commands

#### Retrieve Specific App Listing Custom Field

```bash
curl -i -GET "https://api.ctct.com/external/settings/app-listing-custom-fields/{fieldId}" \
-H "Authorization: Basic {base64_encode(client_id:client_secret)}" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
    "_id": 1684353660,
    "_name": {
        "en": "Test Custom Field 1",
        "es": "Test Custom Field 1"
    },
    "internalName": "Custom Field 1",
    "type": "Custom Field 1"
}
```

#### Modify App Listing Custom Field

```bash
curl -i -PATCH "https://api.ctct.com/external/settings/app-listing-custom-fields/{fieldId}" \
-H "Authorization: Basic {base64_encode(client_id:client_secret)}" \
-H "Content-Type: application/json" \
-d '{
    "_name": {
        "en": "Test Custom Field 1",
        "es": "Test Custom Field 1"
    },
    "internalName": "Custom Field 1",
    "type": "Custom Field 1"
}'
```

The above command returns JSON structured like this:

```json
{
    "_id": 1684353660,
    "_name": {
        "en": "Test Custom Field 1",
        "es": "Test Custom Field 1"
    },
    "internalName": "Custom Field 1",
    "type": "Custom Field 1"
}
```

#### Delete App Listing Custom Field

```bash
curl -i -DELETE "https://api.ctct.com/external/settings/app-listing-custom-fields/{fieldId}" \
-H "Authorization: Basic {base64_encode(client_id:client_secret)}" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
    "_id": 1684353660,
    "_name": {
        "en": "Test Custom Field 1",
        "es": "Test Custom Field 1"
    },
    "internalName": "Custom Field 1",
    "type": "Custom Field 1"
}
```
```

---

```markdown
```plaintext
extraGuests          Object   Contains rules for charging extra guests

extraGuests.type     String   Extra guests commission type. Can be "fixed" or "percent"

extraGuests._._._    Number   Extra guests commission value

extraGuests._._.isAbsolute   Number   Extra guests absolute commission value. Exists if type is "percent".

You must replace client_id, client_secret with real credentials. You must replace domain.plus.stays.net with your real system's domain.

Listing booking settings

This endpoint returns booking settings for certain listing

HTTP Request

GET /parameters/v1/setting/listing/{listingId}/booking

Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_based(client_id:client_secret)  |
| Content-Type  | application/json                           |

Path Parameters

| Parameter | Type   | Description                                       |
|-----------|--------|---------------------------------------------------|
| listingId | String | Listing identifier. Both identifiers (long and short) are supported |

Response Object

| Parameter            | Type   | Description                         |
|----------------------|--------|-------------------------------------|
| ._.listing           | String | Listing identifier                  |
| ._.masterListingId   | String | Master listing identifier           |
| policy               | Object | Cancellation policy object          |
| policy.id            | String | Cancellation policy identifier      |
| policy.ex_rules      | Object | Extra information about policy      |
| bookingSettings      | Object | Listing instant booking settings    |
| checkInTime          | String | Default check-in time start         |
| checkInTimeEnd       | String | Default check-in time end           |
| checkOutTime         | String | Default check-out time start        |
| checkOutTimeEnd      | String | Default check-out time end          |

You must replace client_id, client_secret with real credentials. You must replace domain.plus.stays.net with your real system's domain.

```bash
curl -i -GET "https://api.stays.net/parameters/v1/setting/listing/5040/booking" \
-H "Authorization: Basic hash_based(client_id:client_secret)" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
  "._.listing": "identifierOfThisListingHere",
  "policy": {
    "id": "123",
    "ex_rules": {
      "0": {
        "type": "header",
        "value": "header"
      },
      "1": {
        "type": "text",
        "value": "Aquí puedes poner cualquier especificación en el texto antes de chequear. Aquí este período será calculado en base a la fecha de check-in. Si el huésped cancela 7 días antes de la fecha de llegada, la booking será cancelada sin penalidad."
      }
    }
  },
  "bookingSettings": {
    "instantBooking": true,
    "checkInTime": "14:00",
    "checkInTimeEnd": "23:59",
    "checkOutTime": "11:00",
    "checkOutTimeEnd": "11:59"
  }
}
```

Retrieve house rules for listing

This endpoint returns listing house rules

HTTP Request

GET /parameters/v1/setting/listing/{listingId}/house-rules

Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_based(client_id:client_secret)  |
| Content-Type  | application/json                           |

Path Parameters

| Parameter | Type   | Description                                       |
|-----------|--------|---------------------------------------------------|
| listingId | String | Listing identifier. Both identifiers (long and short) are supported |

* = required params

You must replace client_id, client_secret with real credentials. You must replace domain.plus.stays.net with your real system's domain.

```bash
curl -i -GET "https://api.stays.net/parameters/v1/setting/listing/5040/house-rules" \
-H "Authorization: Basic hash_based(client_id:client_secret)" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
  "acceptChildren": false,
  "acceptPets": false,
  "acceptSmoking": false,
  "acceptEvents": false,
  "rules": {
    "0": {
      "type": "header",
      "value": "Información"
    },
    "1": {
      "type": "text",
      "value": "Agregue aquí reglas, información de carta de bienvenida o también las reglas informadas en tasas de pedido, entre otros."
    }
  }
}
```

Update listing house rules

This endpoint returns listing house rules

HTTP Request

PATCH /parameters/v1/setting/listing/{listingId}/house-rules

Header Parameters

| Parameter     | Value                                      |
|---------------|--------------------------------------------|
| Authorization | Basic hash_based(client_id:client_secret)  |
| Content-Type  | application/json                           |

Path Parameters

| Parameter | Type   | Description                                       |
|-----------|--------|---------------------------------------------------|
| listingId | String | Listing identifier. Both identifiers (long and short) are supported |

* = required params

You must replace client_id, client_secret with real credentials. You must replace domain.plus.stays.net with your real system's domain.

```bash
curl -i -PATCH "https://api.stays.net/parameters/v1/setting/listing/5040/house-rules" \
-H "Authorization: Basic hash_based(client_id:client_secret)" \
-H "Content-Type: application/json"
```

The above command returns JSON structured like this:

```json
{
  "acceptChildren": true,
  "acceptPets": true,
  "acceptSmoking": true,
  "acceptEvents": true,
  "rules": {
    "0": {
      "type": "header",
      "value": "Información"
    },
    "1": {
      "type": "text",
      "value": "Agregue aquí reglas, información de carta de bienvenida o también las reglas informadas en tasas de pedido, entre otros."
    }
  }
}
```
```

---

Lo siento, no puedo extraer el texto de la imagen.

---

Lo siento, no puedo extraer texto de esta imagen.

---

```markdown
## Reservation Notifications

| Action                  | Payload             |
|-------------------------|---------------------|
| reservation.cancelled   | Reservation object  |
| reservation.modified    | Reservation object  |
| reservation.created     | Reservation object  |
| reservation.deleted     | { id, _listings_from, to } |
| reservation.reactivated | Reservation object  |

Example of reservation notification:

```json
{
    "action": "reservation.created",
    "payload": {
        "id": "1234567890abcdef",
        "listing_id": "0987654321",
        "start_date": "2023-10-01",
        "end_date": "2023-10-07",
        "status": "confirmed",
        "guest": {
            "id": "guest123",
            "name": "John Doe",
            "email": "johndoe@example.com"
        },
        "amount": 500,
        "currency": "USD"
    }
}
```

## Calendar Notifications

| Action                         | Payload                                                      |
|--------------------------------|--------------------------------------------------------------|
| calendar.rates.modified        | { _listings_from, to, prices }                               |
| calendar.restrictions.modified | { _listings_from, to, closedToDeparture, closedToArrival, weekdays } |

Example of calendar rates notification:

```json
{
    "action": "calendar.rates.modified",
    "payload": {
        "id": "0987654321",
        "listing_id": "1234567890abcdef",
        "rates": [
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
}
```

Example of calendar restrictions notification:

```json
{
    "action": "calendar.restrictions.modified",
    "payload": {
        "id": "0987654321",
        "listing_id": "1234567890abcdef",
        "restrictions": {
            "closedToDeparture": true,
            "closedToArrival": false,
            "weekdays": [1, 2, 3]
        }
    }
}
```

## Price-region Notifications

| Action               | Payload             |
|----------------------|---------------------|
| price-region.created | Price-region object |
| price-region.modified| Price-region object |
| price-region.deleted | Price-region object |

Example of Price-region notification:

```json
{
    "action": "price-region.created",
    "payload": {
        "id": "region123",
        "name": "Region 1",
        "description": "This is a test region",
        "listings": ["listing1", "listing2"]
    }
}
```

## Season-sell Notifications

| Action                  | Payload             |
|-------------------------|---------------------|
| season-sell.created     | Season-sell object  |
| season-sell.modified    | Season-sell object  |
| season-sell.deleted     | { id, from, to }    |
| season-sell.reactivated | Season-sell object  |

Example of Season-sell notification:

```json
{
    "action": "season-sell.created",
    "payload": {
        "id": "season123",
        "name": "Summer Sale",
        "description": "Discounts for summer",
        "start_date": "2023-06-01",
        "end_date": "2023-08-31",
        "discount": 15,
        "listings": [
            {
                "id": "listing1",
                "price": 85
            },
            {
                "id": "listing2",
                "price": 90
            }
        ]
    }
}
```

## Client Notifications

| Action        | Payload        |
|---------------|----------------|
| client.created| Client object  |

Example of Client notification:

```json
{
    "action": "client.created",
    "payload": {
        "id": "client123",
        "name": "Jane Smith",
        "email": "janesmith@example.com",
        "phone": "+1234567890"
    }
}
```
```

---

```markdown
```json
{
  "action": "client.created",
  "payload": {
    "id": "1234567890abcdef12345678",
    "createdAt": "2023-01-01T12:00:00Z",
    "updatedAt": "2023-01-01T12:00:00Z",
    "name": "Client Name",
    "email": "client@example.com",
    "phone": "+15555555555",
    "notes": "Client notes",
    "tags": [
      "tag1",
      "tag2"
    ],
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "zip": "12345",
      "country": "US"
    },
    "contacts": [
      {
        "name": "Contact Name",
        "email": "contact@example.com",
        "phone": "+15555555555",
        "notes": "Internal note"
      }
    ]
  }
}
```

## Promocode Notifications

**Action**

- Payload

- `promocode.created`: Promocode object
- `promocode.modified`: Promocode object
- `promocode.deleted`: `{ _id, name }`

Example of Promocode notification:

```json
{
  "action": "promocode.created",
  "payload": {
    "id": "abcdef1234567890abcdef12",
    "createdAt": "2023-01-01T12:00:00Z",
    "updatedAt": "2023-01-01T12:00:00Z",
    "name": "Promo Name",
    "description": "Promo Description",
    "discount": 10,
    "isActive": true,
    "isPercentage": false,
    "expirationDate": "2023-12-31T23:59:59Z",
    "usageLimit": 100,
    "usedCount": 0
  },
  "nestedNotification": {
    "nestedField1": {
      "nestedField2": {
        "nestedField3": "value"
      }
    }
  }
}
```

## Listing Notifications

**Action**

- Payload

- `listing.created`: Listing object
- `listing.linked`: Listing object, it triggered when you link listing to target application
- `listing.unlinked`: Listing object, it triggered when you unlink listing from target application
- `listing.modified`: Listing object, it triggered when you modify listing

Example of Listing notification:

```json
{
  "action": "listing.created",
  "payload": {
    "id": "abcdef1234567890abcdef12",
    "createdAt": "2023-01-01T12:00:00Z",
    "updatedAt": "2023-01-01T12:00:00Z",
    "title": "Listing Title",
    "description": "Listing Description",
    "price": 100,
    "currency": "USD",
    "isActive": true,
    "isFeatured": false,
    "category": {
      "id": "category_id",
      "name": "Category Name"
    },
    "location": {
      "latitude": 37.7749,
      "longitude": -122.4194
    }
  }
}
```

## Listing Notifications Rates Sell

**Action**

- Payload

- `listing.rates-sell.modified`: Listing object, it triggered when you modify listing

Example of Listing notification:

```json
{
  "action": "listing.rates-sell.modified",
  "payload": {
    "id": "abcdef1234567890abcdef12",
    "createdAt": "2023-01-01T12:00:00Z",
    "updatedAt": "2023-01-01T12:00:00Z",
    "title": "Listing Title",
    "description": "Listing Description",
    "price": 100,
    "currency": "USD",
    "isActive": true,
    "isFeatured": false,
    "category": {
      "id": "category_id",
      "name": "Category Name"
    },
    "location": {
      "latitude": 37.7749,
      "longitude": -122.4194
    },
    "rates": [
      {
        "quantity": 1,
        "price": 100
      },
      {
        "quantity": 2,
        "price": 90
      },
      {
        "quantity": 3,
        "price": 80
      }
    ]
  }
}
```
```