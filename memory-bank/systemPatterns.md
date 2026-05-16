# System Patterns — TeknoConecta

## Architecture

```
Stays.net ──API────► n8n ──SQL──► PostgreSQL (Neon)
Airbnb ──Email──► n8n ──LLM──► datos estructurados
Tally.so ──Webhook──► n8n ──► PostgreSQL
Twilio ──HTTP──► n8n ──► WhatsApp
Gmail ──IMAP──► n8n ──► procesamiento
                n8n ──► Directus (CMS/Backend)
                n8n ──► OpenAI/Gemini (LLM)
                n8n ──► MercadoPago (pagos)
```

## Key Patterns

### Event-Driven + Schedule-Driven

- Workflows de sincronización: `scheduleTrigger` cada N minutos.
- Workflows de ingesta: `webhook` para formularios y correos entrantes.
- Workflows de envío: `scheduleTrigger` consultando colas con timestamps.

### Colas (Bandejas)

- `ReservaBandejaCorreo` y `ReservaBandejaWhatsapp`: colas de mensajes con `FechaProgramacionEnviar` y `EstadoCodigo`.
- Workflow consulta `WHERE FechaProgramacionEnviar <= now() AND EstadoCodigo = 'Generada' LIMIT 3`.
- Tras envío exitoso, `EstadoCodigo` cambia a `'Enviada'`.

### Single Source of Truth

- PostgreSQL es la fuente canónica de datos operativos.
- Stays.net es fuente de reservas (sincronizadas cada 15 min).
- Directus es la capa de gestión y UI, pero no la fuente de verdad.

### Stays.net ↔ Directus ID Mapping

- `_idlisting` (MongoDB ObjectId) ↔ `AlojamientoStayslistingIdLargo`
- Short ID (ej: FX08J) ↔ `AlojamientoStayslistingId`
- Las descripciones NO viven en Directus; se obtienen del sitio público.

## Component Relationships

| Componente | Rol | Dependencias |
|-----------|-----|-------------|
| n8n | Orquestador | PostgreSQL, APIs externas |
| PostgreSQL (Neon) | Datos operativos + pgvector | Ninguna |
| Directus | CMS / UI operacional | PostgreSQL |
| Stays.net | Fuente de reservas | API HTTP |
| OpenAI / Gemini | Procesamiento LLM | API keys |
| Twilio | WhatsApp saliente | API HTTP |
| Gmail | Correo entrante/saliente | IMAP/SMTP |
| Tally.so | Formularios | Webhook → n8n |
| MercadoPago | Pagos | MCP |

## MCP Local con API Externa (Patrón stays-docs / pricelabs-docs)

Algunos MCPs del proyecto son **locales pero conectan APIs externas**. En vez de llamar directamente a la API desde el agente, se usa un servidor MCP propio que envuelve la API y expone herramientas tipadas.

**Ventajas:**
- Documentación embebida: cada tool tiene descripción, parámetros y ejemplos
- Validación de entrada: el servidor MCP valida parámetros antes de llamar la API
- Read-only por diseño: solo exponen GET / operaciones seguras
- Reutilizable: cualquier agente conectado obtiene las mismas herramientas

**Estructura:**
- Ubicación: `./mcp-servers/{nombre}/server.py`
- Stack: Python + `mcp` SDK
- Registro en `opencode.jsonc` con `"type": "local"` y `"command"` que ejecute `uv run`

**Ejemplos en el repo:**
| MCP | API externa | Ubicación | Función |
|-----|-------------|-----------|---------|
| `stays-docs` | Stays.net API | `./mcp-servers/stays-docs/server.py` | Reservas, listings, checkout |
| `pricelabs-docs` | PriceLabs API | `./mcp-servers/pricelabs-docs/server.py` | Listings, precios, restricciones |

**Reglas para crear nuevos MCPs locales con API externa:**
1. Crear carpeta `./mcp-servers/{nombre}/`
2. Implementar `server.py` usando el SDK de MCP en Python
3. Definir tools con descripción clara, parámetros tipados y ejemplos
4. Usar variables de entorno para credenciales (NO hardcodear en el script)
5. Registrar en `opencode.jsonc` con `"type": "local"` y `"command"` que ejecute `uv run`
6. Preferir operaciones read-only a menos que el caso de uso justifique writes
7. Documentar endpoints funcionales vs no funcionales en `AGENTS.md`

## Design Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| PostgreSQL como fuente de verdad | Consistencia entre sistemas, queries complejas, pgvector para RAG | 2024 |
| Directus como CMS, no como fuente | PostgreSQL ya es canónico; Directus es capa de presentación | 2024 |
| Polling cada 15 min a Stays | API no ofrece webhooks; 15 min es balance entre frescura y carga | 2024 |
| LLM para correos Airbnb | Airbnb no tiene API pública | 2024 |
| Colas con timestamps para envíos | Desacopla generación de envío; permite reprocesar | 2024 |
| MCPs locales para APIs externas | Tipado, validación, documentación embebida, reutilizable | 2026-05-16 |
