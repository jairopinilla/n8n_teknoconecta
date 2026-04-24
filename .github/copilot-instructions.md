# Copilot Instructions — Plataforma Automatización Renta Corta

## Contexto General

Este repositorio contiene los workflows de n8n y documentación para una **plataforma de automatización de renta corta** (estilo Airbnb) que opera múltiples departamentos con mínima intervención humana.

**Propietario:** Jairo Pinilla  
**Dominio Stays:** `jairop.stays.net`  
**Zona horaria operativa:** `America/Santiago` (Chile)

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Orquestación | n8n (self-hosted en `n8n.teknoconectapp.com`) |
| Base de datos | PostgreSQL + pgvector (Neon) |
| CMS / Operación | Directus (`directus.teknoconectapp.com`) |
| IA | OpenAI (GPT-4o / GPT-5.2, embeddings) |
| RAG | pgvector + búsqueda semántica |
| Reservas | Stays.net API |
| Mensajería | WhatsApp Business vía Twilio (`+15559078472`) |
| Email | Gmail (IMAP) |
| Pagos | Mercado Pago |
| Formularios | Tally.so |

---

## Integración con Stays.net

> ⚠️ **Stays.net NO tiene servidor MCP.** Para cualquier tarea relacionada con la API de Stays, Copilot DEBE consultar la documentación en `documentacion/APIStaysDoc.md`.

### Credenciales y dominio

- **Base URL:** `https://jairop.stays.net`
- **Auth:** HTTP Header con credenciales `client_id:client_secret` en Base64 (`Basic` auth)
- En n8n se usa la credencial de tipo `httpHeaderAuth` llamada `"Stays Auth account"` (id: `I4YWvpXuZv5reReY`)

### Endpoints principales usados en este proyecto

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/external/v1/booking/reservations` | GET | Listar reservas activas por rango de fechas |
| `/external/v1/booking/reservations/{reservationId}` | GET | Detalle de una reserva |
| `/external/v1/booking/reservations/{reservationId}/payments` | GET | Pagos de una reserva |
| `/external/checkout/initiate` | POST | Iniciar proceso de checkout |
| `/external/promocodes/create-promo-code` | POST | Crear código promocional |
| `/external/v1/booking/search-listings` | POST | Buscar listados disponibles |

### Parámetros comunes de búsqueda de reservas

```http
GET /external/v1/booking/reservations?from=YYYY-MM-DD&to=YYYY-MM-DD&dateType=arrival
```

Valores de `dateType`: `arrival`, `departure`, `creation`, `modification`, `include`

Tipos de reserva (`type`): `reserved`, `blocked`, `contract`, `ownerBlocked`, `maintenance`, `cleaning`

### Referencia completa

Ver `documentacion/APIStaysDoc.md` para todos los endpoints, parámetros y ejemplos de respuesta.

---

## Workflows en n8n

### Convenciones de código

- Nodos Postgres usan la credencial `"Postgres account"` (id: `zvx0J3DPht42SAUp`)
- Siempre obtener hora actual con: `SELECT now() AT TIME ZONE 'America/Santiago' AS santiago_datetime;`
- **Fechas siempre desde PostgreSQL:** usar `now() AT TIME ZONE 'America/Santiago'` en SQL. Nunca calcular fechas en nodos JavaScript/Code de n8n.
- Los workflows usan polling por scheduler (no webhooks de Stays, ya que no hay MCP)
- Airbnb **no tiene API** → se procesa vía parsing de correo electrónico con LLM

### Workflows activos

| Archivo | Función |
|---------|---------|
| `N8n_Update_Reservas.json` | Sincroniza reservas de Stays.net → PostgreSQL. Consulta por rango de fechas y upsert de huéspedes y reservas. |
| `N8n_EnviarCorreosReserva.json` | Envía correos programados de notificación a huéspedes (pre check-in, instrucciones, etc.) desde tabla `ReservaBandejaCorreo`. |
| `N8n_ProcesaWhatsapp.json` | Envía mensajes WhatsApp programados vía Twilio desde tabla `ReservaBandejaWhatsapp`. Incluye links de formulario de aseo (`https://tally.so/r/vGeKkd`) y contacto (`https://wa.me/56964972508`). |
| `N8n_SandiegoChatbot.json` | Agente IA (RAG + LLM) para responder consultas de huéspedes del departamento San Diego vía WhatsApp. Usa tools: `general_chat` y otras herramientas configuradas. |
| `N8n_interpreta_email_conserjeria.json` | Interpreta correos de conserjería usando GPT (extrae nombre huésped, fecha check-in, departamento). Usa tabla `BandejaConserjeriaInput`. Corre cada 10 min. |
| `N8n_Procesa_Formularios.json` | Recibe webhooks de Tally.so (formularios de aseo/limpieza) y los almacena en tabla `BandejaInputTally`. |
| `N8n_procesa_tarapaca_conserjeria.json` | Procesa mensajes de conserjería para el departamento Tarapacá. |
| `N8n_procesar_email_isaias.json` | Procesa correos entrantes del buzón de Isaías. |
| `N8n_procesar_email_tekno.json` | Procesa correos entrantes del buzón principal TeknoConect. |
| `N8n_getAseosHtml.json` | Genera reporte HTML de aseos/limpiezas. |

---

## Modelo de Datos (PostgreSQL)

### Tablas principales identificadas en workflows

| Tabla | Descripción |
|-------|-------------|
| `ReservaBandejaCorreo` | Cola de correos programados. Campos clave: `FechaProgramacionEnviar`, `EstadoCodigo` |
| `ReservaBandejaWhatsapp` | Cola de mensajes WhatsApp programados. Misma estructura que correos. |
| `BandejaConserjeriaInput` | Entrada de correos de conserjería. Campo estado: `BandejaConserjeriaInputEstado` (`PENDIENTE`) |
| `BandejaInputTally` | Formularios recibidos de Tally.so. Campos: `BandejaInputTallyEventId`, `BandejaInputTallyFormId`, `BandejaInputTallyPayload_crudo` |

### Convenciones de nomenclatura DB

- Las columnas usan el nombre de la tabla como prefijo: `{NombreTabla}{NombreColumna}`
- El estado estándar para registros pendientes: `EstadoCodigo = 'Generada'` o `Estado = 'PENDIENTE'`
- Todos los timestamps en zona horaria `America/Santiago`

---

## Inteligencia Artificial

### Modelos usados

- `gpt-4o`: Embeddings y tareas generales
- `gpt-5.2`: Procesamiento avanzado (interpretación de correos con lógica compleja)

### RAG (Retrieval-Augmented Generation)

- Embeddings almacenados en pgvector (PostgreSQL)
- Búsqueda híbrida: vector + texto
- Memoria conversacional en Postgres

### Chatbot San Diego

El chatbot usa un router de tools basado en el campo `tool` del JSON:
- `general_chat`: Respuesta conversacional general
- Otras tools según contexto de la propiedad

---

## Operaciones

### Mensajería WhatsApp

- **Número Twilio origen:** `+15559078472`
- **Número personal operador:** `+56954862320`
- **Link respuesta huésped:** `https://wa.me/56964972508`
- **Formulario aseo:** `https://tally.so/r/vGeKkd`

### Flujo de check-in por conserjería

1. Correo llega al buzón monitorizado
2. n8n lo parsea con GPT (extrae nombre, fecha, departamento)
3. Validación: si faltan datos → respuesta automática solicitándolos
4. Si completo → registro en DB + notificaciones al operador

### Flujo de reservas Stays

1. Scheduler en n8n llama `GET /external/v1/booking/reservations` con rango de fechas
2. Para cada reserva obtiene detalle completo vía `GET /external/v1/booking/reservations/{id}`
3. Upsert en PostgreSQL con datos normalizados
4. Genera eventos en la base de datos

---

## Principios de Diseño

- **Airbnb no tiene API** → procesamiento vía correo + LLM parsing
- Zona horaria siempre `America/Santiago`
- Todo evento queda registrado (event logging)
- Webhooks autenticados con header auth
- Limpieza como KPI principal
- Diseño orientado a bajo costo y alta confiabilidad

---

## Cómo ayuda Copilot con este proyecto

Con estas instrucciones, Copilot puede:

1. **Generar workflows n8n** siguiendo las convenciones del proyecto (credenciales, zona horaria, tablas DB)
2. **Escribir queries SQL** usando la nomenclatura de tablas establecida
3. **Construir llamadas a la API de Stays.net** (consultar `APIStaysDoc.md` para parámetros exactos)
4. **Diseñar prompts de sistema** para los nodos LLM de OpenAI
5. **Depurar flows existentes** entendiendo la arquitectura completa
6. **Diseñar integraciones** con WhatsApp, Gmail, Tally, Mercado Pago
7. **Optimizar pipelines RAG** con pgvector

> Cuando se trabaje con la API de Stays.net, siempre revisar `documentacion/APIStaysDoc.md` ya que no existe servidor MCP para esta integración.
