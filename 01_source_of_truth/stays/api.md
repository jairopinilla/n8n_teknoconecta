# API Stays.net

Fuente: `documentacion/APIStaysDoc.md` (canonica).

## Endpoints verificados

### Funcionan

| Endpoint | Metodo | Uso |
|----------|--------|-----|
| `/external/v1/booking/reservations` | GET | Listar reservas por rango de fechas |
| `/external/v1/booking/reservations/{id}` | GET | Detalle de una reserva |
| `/external/checkout/initiate` | POST | Iniciar checkout |

### No funcionan (404)

- `/v1/parameters/content/properties/{id}` — endpoint de propiedades no existe en esta instancia
- `/parameters/v1/setting/listing/{id}/booking` — booking settings no existe
- `/external/docs/index/` — Swagger docs no accesible

### Devuelve vacio

- `/external/v1/booking/search-listings` — POST, devuelve `[]`

## Autenticacion

Basic Auth via API key (configurada en `.vscode/mcp.json` como variable de entorno).
No exponer en archivos versionados.

## Ver tambien

- `documentacion/APIStaysDoc.md` — referencia completa
- `06_automatizacion/stays_api_workflows.md` — workflows que usan la API
