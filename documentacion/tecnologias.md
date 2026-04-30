# Tecnologías — Plataforma Automatización Renta Corta

## Arquitectura General

La plataforma opera como un sistema de automatización event-driven donde n8n orquesta todos los flujos de negocio. Los datos persisten en PostgreSQL y los servicios externos se integran mediante APIs REST, webhooks y servidores MCP.

---

## n8n (Orquestador principal)

- **URL:** `https://n8n.teknoconectapp.com`
- **MCP:** Disponible en `https://n8n.teknoconectapp.com/mcp-server/http` con JWT Bearer token
- **Autenticación interna:** Credencial `"Key Interna n8n Webhook"` (id: `z0M54nC5Fx9VCrLL`) para webhooks entrantes
- **Versión de nodos Postgres:** 2.6
- **Versión de nodos HTTP:** 4.3

### Patrones comunes en workflows

```javascript
// Obtener hora Santiago
SELECT now() AT TIME ZONE 'America/Santiago' AS santiago_datetime;

// Leer cola de mensajes pendientes
SELECT * FROM "ReservaBandejaCorreo"
WHERE "FechaProgramacionEnviar" <= '{{ $json.santiago_datetime }}'
  AND "EstadoCodigo" = 'Generada'
LIMIT 3;
```

---

## PostgreSQL + pgvector (Neon)

- **Proveedor:** Neon (serverless Postgres)
- **Credencial n8n:** `"Postgres account"` (id: `zvx0J3DPht42SAUp`)
- **Extensión:** pgvector para embeddings semánticos
- **MCP Neon:** Disponible vía `@neondatabase/mcp-server-neon`

### Convenciones de nomenclatura

| Patrón | Ejemplo |
|--------|---------|
| Nombre columna = prefijo tabla | `BandejaConserjeriaInputEstado` |
| Estado inicial | `'Generada'` o `'PENDIENTE'` |
| Timestamps | Siempre `America/Santiago` |

### Tablas de cola (bandejas)

| Tabla | Tipo | Campos clave |
|-------|------|-------------|
| `ReservaBandejaCorreo` | Cola emails | `FechaProgramacionEnviar`, `EstadoCodigo` |
| `ReservaBandejaWhatsapp` | Cola WhatsApp | `FechaProgramacionEnviar`, `EstadoCodigo` |
| `BandejaConserjeriaInput` | Entrada conserjería | `BandejaConserjeriaInputEstado`, `BandejaConserjeriaInputPayload_crudo` |
| `BandejaInputTally` | Formularios Tally | `BandejaInputTallyEventId`, `BandejaInputTallyFormId`, `BandejaInputTallyPayload_crudo` |

---

## Directus (CMS / Backend operacional)

- **URL:** `https://directus.teknoconectapp.com`
- **MCP:** Disponible en `https://directus.teknoconectapp.com/mcp` mediante Bearer token almacenado solo en configuración local no versionada
- **Funciones:** CRUD de reservas, propiedades, huéspedes y configuraciones operacionales
- **API:** REST + GraphQL autogenerada

---

## Stays.net (Gestión de reservas)

> ⚠️ **NO tiene servidor MCP.** Siempre consultar `documentacion/APIStaysDoc.md`.

- **Base URL:** `https://jairop.stays.net`
- **Autenticación:** `Basic base64(client_id:client_secret)`
- **Credencial n8n:** `"Stays Auth account"` (id: `I4YWvpXuZv5reReY`)
- **Tipo credencial:** `httpHeaderAuth`

### Endpoints principales

| Endpoint | Método | Uso |
|----------|--------|-----|
| `/external/v1/booking/reservations` | GET | Listar reservas por rango de fechas |
| `/external/v1/booking/reservations/{id}` | GET | Detalle completo de reserva |
| `/external/v1/booking/reservations/{id}/payments` | GET | Pagos de una reserva |
| `/external/checkout/initiate` | POST | Iniciar checkout de reserva |
| `/external/promocodes/create-promo-code` | POST | Crear código promocional |
| `/external/v1/booking/search-listings` | POST | Buscar propiedades disponibles |
| `/v1/finance/owners/{ownerId}` | GET | Datos financieros por propietario |
| `/reservations/booking/reservations/export` | GET/POST | Exportar reservas (XLSX o JSON) |

### Parámetros de búsqueda de reservas

```
dateType: arrival | departure | creation | modification | include
type: reserved | blocked | contract | ownerBlocked | maintenance | cleaning
```

---

## OpenAI y otros modelos LLM

- **OpenAI:** `gpt-4o` (general + embeddings), `gpt-5.2` (procesamiento complejo)
- **MCP OpenAI:** Disponible vía `@mzxrai/mcp-openai@latest`
- **Uso en workflows:**
  - `N8n_interpreta_email_conserjeria.json`: Extracción estructurada de datos de correos con GPT-5.2
  - `N8n_SandiegoChatbot.json`: Respuestas conversacionales y rutas RAG
- **Google Gemini:** Presente en `N8n_SandiegoChatbot.json` mediante nodos LangChain para rutas conversacionales específicas
- **Tavily:** Presente en `N8n_SandiegoChatbot.json` como herramienta externa de búsqueda

### Prompt de sistema — Intérprete de conserjería

El workflow `N8n_interpreta_email_conserjeria.json` usa un prompt que:
1. Extrae `nombre_huesped`, `fecha_checkin`, `departamento` (obligatorios)
2. Extrae `fecha_checkout`, `cantidad_huespedes`, `pais` (opcionales)
3. Retorna JSON con estados: `completo` / `incompleto`, `valido: Si/No`
4. Genera mensaje de respuesta automática al remitente

---

## WhatsApp Business / Twilio

- **Número Twilio (origen):** `+15559078472`
- **Número operador (destino notificaciones):** `+56954862320`
- **Link de respuesta a huéspedes:** `https://wa.me/56964972508`
- **Formulario de aseo:** `https://tally.so/r/vGeKkd`
- **Integración:** Nodo HTTP en n8n hacia Twilio API

---

## Gmail (IMAP)

- **Uso:** Ingesta de correos de reservas Airbnb y conserjería
- **Estrategia:** Polling + parsing con LLM (Airbnb no tiene API)
- **Buzones monitorizados:**
  - Buzón principal TeknoConect (`N8n_procesar_email_tekno.json`)
  - Buzón personal Isaías (`N8n_procesar_email_isaias.json`)
  - Correos de conserjería (`N8n_interpreta_email_conserjeria.json`)

---

## Tally.so (Formularios)

- **Formulario aseo/limpieza:** `https://tally.so/r/vGeKkd`
- **Integración:** Webhook POST a n8n con autenticación por header
- **Path webhook:** `/ingesta-formulario`
- **Tabla destino:** `BandejaInputTally`
- **Campos almacenados:** `eventId`, `createdAt`, `formId`, `formName`, `webhookUrl`, payload JSON crudo

---

## Mercado Pago

- **MCP:** Disponible en `https://mcp.mercadopago.com/mcp`
- **Uso:** Procesamiento de pagos de reservas y cobros a huéspedes

---

## Supabase

- **MCP:** `https://mcp.supabase.com/mcp?project_ref=fjebesmrwdceyvllpslv`

---

## Vercel

- **MCP:** `https://mcp.vercel.com`

---

## Perplexity

- **MCP:** Disponible vía `perplexity-mcp`

---

## Jina AI

- **MCP:** `https://mcp.jina.ai/v1`
- **Uso:** Búsqueda semántica y procesamiento de contenido web

---

## Resumen de MCPs disponibles

| Servicio | MCP disponible | Tipo |
|---------|---------------|------|
| n8n | ✅ | HTTP (supergateway) |
| Directus | ✅ | HTTP (Bearer token) |
| Neon DB | ✅ | NPM package |
| OpenAI | ✅ | NPM package |
| Mercado Pago | ✅ | HTTP |
| Supabase | ✅ | HTTP |
| Vercel | ✅ | HTTP |
| Perplexity | ✅ | NPM package |
| Jina AI | ✅ | HTTP |
| **Stays.net** | ❌ | **Requiere API manual** |
| Airbnb | ❌ | **Sin API pública** |

---

## Seguridad y Credenciales

- Las credenciales reales están en `secrets.json` (no commitear)
- La configuración MCP del workspace vive en `.vscode/mcp.json` y también es local (no commitear)
- Los IDs de credenciales en n8n se referencian por nombre en los workflows
- Los webhooks se autentican con `"Key Interna n8n Webhook"`
- Stays.net usa Basic Auth con Base64 del par `client_id:client_secret`
- La documentación versionada nunca debe incluir tokens, API keys o Bearer tokens reales; solo nombres de credenciales, mecanismos de auth o ubicaciones locales
