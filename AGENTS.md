# AGENTS.md

Este archivo es la fuente canónica de instrucciones para cualquier asistente de código que trabaje en este repositorio. El contenido debe mantenerse neutral respecto de un proveedor concreto; los archivos `CLAUDE.md`, `OPENCODE.md` y `.github/copilot-instructions.md` existen solo como puntos de entrada compatibles y no deben divergir de este documento.

## Orden de lectura obligatorio

Antes de proponer o aplicar cambios, leer en este orden:

1. `AGENTS.md` (este archivo, incluyendo la sección "Lecciones aprendidas")
2. `README.md`
3. `memory-bank/projectbrief.md`
4. `memory-bank/productContext.md`
5. `memory-bank/techContext.md`
6. `memory-bank/systemPatterns.md`
7. `memory-bank/activeContext.md`
8. `memory-bank/progress.md`
9. `documentacion/guia-repositorio.md`
10. `documentacion/seguimiento.md`
11. `documentacion/tecnologias.md`
12. `documentacion/APIStaysDoc.md` si el cambio toca Stays.net

### Memoria persistente entre sesiones

Cada sesión empieza sin contexto previo. La única memoria son estos archivos. Por eso:

- Al inicio de cada sesión el asistente DEBE leer `AGENTS.md` completo, incluyendo la sección "Lecciones aprendidas".
- Todo descubrimiento operativo (endpoints que fallan, rutas alternativas, mapeos de IDs entre sistemas, limitaciones de herramientas) debe registrarse en la sección "Lecciones aprendidas" de este mismo archivo para no repetir el proceso de descubrimiento.
- Si el aprendizaje es sustantivo, también debe reflejarse en `documentacion/tecnologias.md` y `documentacion/seguimiento.md`.

## Contexto del proyecto

El repositorio contiene exportaciones de workflows de n8n y documentación operativa para una plataforma de automatización de renta corta. La plataforma opera múltiples departamentos con mínima intervención humana, principalmente mediante n8n, PostgreSQL, Directus, integraciones externas y LLMs.

## Estructura relevante del repositorio

- `workflows/`: exportaciones JSON de workflows de n8n.
- `documentacion/APIStaysDoc.md`: referencia manual de la API de Stays.net.
- `documentacion/tecnologias.md`: inventario tecnológico y credenciales por nombre o ubicación, nunca por secreto.
- `documentacion/guia-repositorio.md`: guía operativa detallada del repositorio.
- `documentacion/seguimiento.md`: bitácora viva de estado, cambios recientes y próximos pasos.
- `sync_workflows.sh`: script para descargar workflows desde n8n usando `secrets.json` local.
- `.vscode/mcp.json`: configuración local de MCP del workspace. Es local, está ignorada por git y debe preferirse sobre configuraciones globales del usuario.
- `secrets.json`: credenciales locales para automatizaciones del repo. Está ignorado por git.

## Protocolo de interacción obligatorio

Ante cada solicitud del usuario, el asistente debe aplicar el protocolo **grill-me**: entrevistar sin piedad cada aspecto del plan o diseño hasta alcanzar un entendimiento compartido. Recorrer cada rama del árbol de decisión, resolviendo dependencias una por una.

- Hacer las preguntas **de una en una** (nunca en lote).
- Para cada pregunta, proporcionar una **respuesta recomendada**.
- Si una pregunta puede responderse explorando el código base, **explorarlo** en lugar de preguntar.
- No ejecutar ni proponer cambios hasta que el árbol de decisión esté completamente resuelto.
- Si la solicitud es trivial o puramente informativa, aplicar criterio: el grill-me escala con la complejidad de la decisión.

## Reglas operativas no negociables

- La zona horaria operativa es `America/Santiago`.
- Las fechas operativas deben obtenerse desde PostgreSQL con `now() AT TIME ZONE 'America/Santiago'`; no se deben recalcular en nodos JavaScript cuando el dato puede venir de SQL.
- Stays.net no tiene servidor MCP en este proyecto. Si el cambio toca reservas, pagos, checkout, promo codes o disponibilidad, se debe consultar `documentacion/APIStaysDoc.md` antes de proponer endpoints o payloads.
- Airbnb no tiene API pública dentro de esta arquitectura; los flujos relacionados se apoyan en correo y parsing con LLM.
- Los workflows deben seguir referenciando credenciales por nombre o por tipo de credencial de n8n. Nunca se deben agregar tokens, API keys o secretos en archivos versionados.
- Nunca usar ni documentar el `mcp.json` global del usuario para este repo. La referencia válida es el `.vscode/mcp.json` local del workspace.
- Toda documentación nueva o modificada debe mantener el mismo nivel de detalle entre recursos y componentes relacionados.
- Toda modificación sustantiva del repo debe actualizar `documentacion/seguimiento.md` con dos cosas: qué se hizo y cuál es el siguiente paso recomendado.

## Protocolo para cambios en workflows

1. Identificar el workflow exacto y revisar su exportación JSON en `workflows/`.
2. Verificar el disparador real del workflow y las integraciones que usa.
3. Si el cambio impacta Stays.net, contrastar el endpoint y la autenticación contra `documentacion/APIStaysDoc.md`.
4. Mantener nombres de credenciales, IDs funcionales y convenciones del proyecto; nunca introducir secretos en texto plano.
5. Si cambian responsabilidades, integraciones, estados o convenciones, actualizar `README.md`, `documentacion/guia-repositorio.md`, `documentacion/tecnologias.md` y `documentacion/seguimiento.md` según corresponda.

## Protocolo para documentación

- `README.md`: puerta de entrada del repositorio.
- `documentacion/guia-repositorio.md`: operación, estructura, flujos y reglas de mantenimiento.
- `documentacion/tecnologias.md`: stack, integraciones y fuentes de credenciales sin exponer secretos.
- `documentacion/seguimiento.md`: historial vivo, estado actual y rumbo inmediato.
- Si una nueva documentación cambia la forma de trabajar con el repo, enlazarla desde `README.md` y desde esta instrucción si aplica.

## Validación mínima esperada

- Para JSON de workflows: validar sintaxis con `jq '.' workflows/<archivo>.json` o equivalente.
- Para shell scripts: validar con `bash -n sync_workflows.sh` si el script fue tocado.
- Para documentación sensible: buscar tokens o secretos residuales antes de commit.
- Antes de commit: revisar `git diff --stat` y `git status --short`.

## Lecciones aprendidas

> ⚠️ Esta sección es memoria persistente entre sesiones. Todo descubrimiento operativo debe registrarse aquí para que el próximo asistente no repita el mismo proceso.

### Stays.net API — Lo que funciona y lo que no

**Endpoints que SÍ funcionan:**
| Endpoint | Método | Notas |
|----------|--------|-------|
| `/external/v1/booking/reservations` | GET | Lista reservas con parámetros `from`, `to`, `dateType`, `listingId`. Límite 20 por página. |
| `/external/v1/booking/reservations/{id}` | GET | Detalle de una reserva |
| `/external/checkout/initiate` | POST | Iniciar checkout |

**Endpoints que NO funcionan (404) en esta instancia:**
| Endpoint | Error |
|----------|-------|
| `/v1/parameters/content/properties/{id}` | 404 — El endpoint de propiedades NO existe en esta instancia. Probado con Mongo ObjectId y IDs cortos (FX08J). |
| `/parameters/v1/setting/listing/{id}/booking` | 404 — El endpoint de booking settings NO existe |
| `/external/docs/index/` | 404 — Swagger docs no accesibles vía API ni web |

**Endpoint que existe pero devuelve vacío:**
| `/external/v1/booking/search-listings` | POST | Devuelve `[]` con parámetros básicos. Posiblemente necesite parámetros específicos. |

### Mapeo de IDs entre Stays.net y Directus

- Las reservas de Stays devuelven `_idlisting` (MongoDB ObjectId, ej: `698ead2e065bcaac0d2f4940`).
- En Directus, la colección `Alojamiento` tiene:
  - `AlojamientoStayslistingId`: ID corto de Stays (ej: `FX08J`)
  - `AlojamientoStayslistingIdLargo`: ID largo de Stays (MongoDB ObjectId)
  - `AlojamientoNombre`: nombre del anuncio
  - `AlojamientoDescripcion`: descripción (frecuentemente `null` en Directus)
  - `AlojamientoTipo`: tipo (Departamento, Casa, Habitacion)
- Las descripciones reales (`_mdesc`, `_mtitle`) viven en Stays.net pero no son accesibles vía API. Hay que obtenerlas del sitio público.

### Cómo obtener descripciones de anuncios

1. Obtener IDs desde reservas (`/external/v1/booking/reservations` → campo `_idlisting`).
2. Cruzar con Directus (`Alojamiento`) para obtener el ID corto (`AlojamientoStayslistingId`).
3. Construir URL pública: `https://www.sandiegoapart.com/es/apartment/{shortId}/{slug}`
4. Usar `jina_parallel_read_url` o `webfetch` para extraer el contenido de la página.

### Scrapling / Web scraping

- Las tools de browser de Scrapling (`fetch`, `stealthy_fetch`, `bulk_stealthy_fetch`, `screenshot`) requieren Chromium con dependencias de sistema (`libnspr4.so` y otras) que NO están instaladas en WSL.
- Las tools HTTP de Scrapling (`get`, `bulk_get`) y `webfetch` / `jina_read_url` SÍ funcionan correctamente.
- Para habilitar scraping completo se necesita `sudo playwright install-deps chromium`.

### MCPs disponibles

14 servidores MCP configurados en `.vscode/mcp.json`: airroi, clerk, neon, vercel, openai, jina, perplexity, google-maps, mercadopago, n8n-mcp, supabase, directus, stays-docs, scrapling.

### Herramientas clave para consultas

- **Reservas Stays:** usar `stays-docs_stays_get_reservations` (wrapper) o `stays-docs_stays_api_call`.
- **Datos de anuncios:** usar `directus_items` sobre colección `Alojamiento`.
- **Descripciones web:** usar `jina_parallel_read_url` sobre `https://www.sandiegoapart.com/es/apartment/{id}/...`.
- **Búsquedas texto Stays docs:** `stays-docs_search_stays_docs`.

## Compatibilidad multi-agente

- `AGENTS.md` es la referencia principal.
- `CLAUDE.md`, `OPENCODE.md` y `.github/copilot-instructions.md` deben ser archivos delgados que redirigen a este documento y no deben introducir reglas contradictorias.
- Si se agrega soporte para otro asistente, el patrón esperado es crear solo un archivo de entrada mínimo que apunte a `AGENTS.md` y a la documentación operativa existente.