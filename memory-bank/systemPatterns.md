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

## Design Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| PostgreSQL como fuente de verdad | Consistencia entre sistemas, queries complejas, pgvector para RAG | 2024 |
| Directus como CMS, no como fuente | PostgreSQL ya es canónico; Directus es capa de presentación | 2024 |
| Polling cada 15 min a Stays | API no ofrece webhooks; 15 min es balance entre frescura y carga | 2024 |
| LLM para correos Airbnb | Airbnb no tiene API pública | 2024 |
| Colas con timestamps para envíos | Desacopla generación de envío; permite reprocesar | 2024 |
