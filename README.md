# SandiegoApart — Base de conocimiento y accion

Operador de renta corta en Santiago Centro, Chile.
4 estudios en Tarapaca 1140: 901, 902, 709, 702.

> Estudios modernos con terraza en Santiago Centro, pensados para trabajar y descansar.

## Leer primero

- `AGENTS.md` — instrucciones canonicas para asistentes de IA
- `00_contexto_negocio/` — quien somos, que operamos
- `01_source_of_truth/` — Stays, PriceLabs
- `documentacion/seguimiento.md` — estado actual y cambios recientes

## Estructura del repositorio

| Carpeta | Proposito |
|---------|-----------|
| `00_contexto_negocio/` | Negocio, unidades, ubicacion, glosario, politica de marca |
| `01_source_of_truth/` | Fuentes de verdad: Stays, PriceLabs |
| `02_operacion/` | Reglas operativas, check-in/out, edificio, seguridad |
| `03_marketing_y_ads/` | Marca, tono, anuncios, Instagram |
| `04_mensajeria/` | Plantillas de mensajes a huespedes (ES/EN/PT-BR) |
| `05_finanzas_y_pricing/` | KPIs, revenue management |
| `06_automatizacion/` | n8n, MCP, workflows |
| `07_data_exports/` | Exportaciones de datos (raw → processed) |
| `08_playbooks/` | Guias paso a paso para tareas operativas |
| `09_archive/` | Contenido deprecated preservado |
| `workflows/` | Exportaciones JSON de workflows n8n |
| `documentacion/` | Documentacion legacy (APIStays, pricelabs-academy, etc.) |
| `mcp-servers/` | Servidores MCP locales (stays-docs, pricelabs-docs) |
| `secrets/` | Documentacion de seguridad (sin valores reales) |

## Stack tecnologico

- **Orquestador:** n8n self-hosted
- **Persistencia:** PostgreSQL (Neon) + pgvector
- **Backend:** Directus
- **PMS:** Stays.net
- **Pricing:** PriceLabs
- **Mensajeria:** Twilio (WhatsApp) + Gmail
- **IA:** OpenAI, Google Gemini
- **Agentes IA:** Protocolo MCP (15 servidores)

## Seguridad

⚠️ **CRITICAL:** `exportadata/` contiene datos sensibles con PII de huespedes.
Ver `secrets/README.md` para el inventario completo de secretos detectados y acciones requeridas.

## Estado y seguimiento

`documentacion/seguimiento.md` — registro vivo de cambios, estado actual y proximos pasos.
