# AGENTS.md — SandiegoApart

> Fuente canonica de instrucciones para cualquier asistente de IA que trabaje en este repositorio.
> Version: 2026-05-15

## Proposito

Este repositorio es la base de conocimiento y accion para **SandiegoApart**, operador de renta corta en Santiago Centro, Chile.

Los asistentes deben usar este repo para:
- crear y optimizar anuncios (ES/EN/PT-BR)
- generar mensajes a huespedes
- revisar reglas operativas
- analizar pricing y ocupacion
- trabajar con Stays.net y PriceLabs
- crear contenido para Instagram
- disenar automatizaciones n8n
- mantener documentacion limpia y trazable

## Orden de lectura obligatorio

Antes de proponer cambios, leer en este orden:

1. `00_contexto_negocio/` — quien es SandiegoApart, que unidades opera, donde esta ubicado
2. `01_source_of_truth/` — fuentes de verdad (Stays, PriceLabs)
3. `02_operacion/` — reglas operativas, check-in/out, edificio
4. `03_marketing_y_ads/` — marca, tono, anuncios
5. `04_mensajeria/` — mensajes a huespedes, plantillas
6. `05_finanzas_y_pricing/` — KPIs, revenue management
7. `06_automatizacion/` — n8n, MCP, workflows
8. `08_playbooks/` — guias paso a paso
9. `documentacion/` — documentacion existente (legacy)
10. `seguimiento.md` — estado actual y cambios recientes
11. `tecnologias.md` — stack tecnologico
12. `APIStaysDoc.md` — si el cambio toca Stays.net
13. `pricelabs-academy/` — si el cambio toca PriceLabs

## Datos fijos vs datos que se buscan dinamicamente

**Datos fijos en este repo** (no cambiar sin aprobacion):
- Contexto del negocio (`00_contexto_negocio/`)
- Reglas operativas (`02_operacion/`)
- Marca y tono (`03_marketing_y_ads/`)
- Plantillas de mensajes (`04_mensajeria/`)
- KPIs y finanzas (`05_finanzas_y_pricing/`)
- Playbooks (`08_playbooks/`)

**Datos que deben buscarse dinamicamente** (NO estan en este repo; consultar la fuente indicada):
| Que buscas | Donde consultarlo |
|------------|------------------|
| Descripciones de anuncios, titulos, amenities activos por unidad | Stays API o sitio publico sandiegoapart.com |
| Precios actuales, tarifas, restricciones de estadia | PriceLabs |
| Disponibilidad, calendario | Stays |
| Reservas activas, huespedes actuales | Stays API |
| Reglas de pricing dinamico | PriceLabs |
| Fotos de unidades | Stays / repositorio de imagenes |

**Importante**: Las descripciones de anuncios NO estan en PriceLabs. PriceLabs es solo pricing.
Si necesitas el contenido de un anuncio (descripcion, titulo, amenities), consulta Stays directamente.

## Fuente de verdad (jerarquia obligatoria)

1. **Stays**: calendario, tarifas, disponibilidad, contenido publicado, amenities, reglas activas, IDs
2. **Manuales oficiales Tarapaca 1140 y artefactos**: reglas del edificio, mantenciones, espacios comunes, restricciones
3. **Exportaciones actuales**: analisis operativo y financiero con fecha de corte
4. **PriceLabs**: pricing, reglas tarifarias, revenue management cuando este actualizado
5. **Asesorias y ebooks**: buenas practicas, marketing, comunicacion, pricing
6. **Memoria del repo**: contexto auxiliar, no fuente final

## Reglas criticas

- No inventar amenities — si no esta en Stays o en un archivo, no existe
- No inventar politicas — no asumir reglas del edificio sin fuente
- No exponer claves, tokens, codigos de acceso, Wi-Fi, passwords
- No prometer estacionamiento — no hay
- No prometer espacios comunes — sin confirmacion, no se mencionan
- No decir "a pasos" si no esta medido
- No usar claims exagerados (lujo, unico, imperdible, espectacular, increible)
- Mantener coherencia anuncio ↔ realidad
- Si falta un dato, dejar placeholder o pedir confirmacion
- Si hay conflicto entre documentos, usar formato de conflicto (abajo)
- En respuestas a huespedes: tono claro, amable y directo
- En contenido comercial: tono urbano, sobrio y confiable
- **TODOS los cambios realizados DEBEN quedar documentados en el `memory-bank/`** — actualizar `activeContext.md` y `progress.md` al finalizar cada tarea

## Contexto comercial

SandiegoApart: **Estudios modernos con terraza en Santiago Centro, pensados para trabajar y descansar.**

Ubicacion: Tarapaca 1140, Santiago Centro, Chile.

Unidades (4 estudios):
- 901 (piso 9)
- 902 (piso 9)
- 709 (piso 7)
- 702 (piso 7)

Atributos base (todas las unidades):
- Terraza privada
- Cama king
- Escritorio + silla
- Mesa alta para 2
- TV 50"
- Wi-Fi rapido
- A/C frio-calor
- Cocinha equipada
- Bano privado

No incluir sillon cama como amenity general — solo si la unidad lo tiene habilitado en Stays.
No hay estacionamiento.
No hay piscina, gimnasio, quincho, cowork ni terraza comun confirmados.

## Idiomas

- Espanol (ES)
- English (EN)
- Portugues do Brasil (PT-BR)

No traducir literal. Localizar segun cultura del huesped.

Glosario trilingue:
| ES | EN | PT-BR |
|----|----|-------|
| terraza | terrace/balcony (segun contexto) | varanda/terraco |
| cama king | king bed | cama king |
| sofa cama | sofa bed | sofa-cama |
| Wi-Fi rapido | fast Wi-Fi | Wi-Fi rapido |
| A/C frio-calor | hot/cold A/C | ar-condicionado quente/frio |
| escritorio | desk/workspace | mesa de trabalho |
| Santiago Centro | Downtown Santiago | Santiago Centro |
| Metro Moneda | Moneda metro station | metro Moneda |

## Entregables esperados

Cuando generes contenido, entregar:
- Copy de anuncio completo (titulo, subtitulo, bullets, FAQ, CTA)
- Mensajes a huesped listos para enviar
- Checklist operativo
- Contenido Instagram (copy + descripcion)
- Instrucciones para automatizacion n8n
- Todo en ES/EN/PT-BR cuando aplique

## Seguridad

**Jamas exponer en este repo:**
- Claves Wi-Fi
- Codigos de cerradura
- Codigos de caja fuerte
- Tokens API
- Passwords
- Datos de huespedes (nombres, telefonos, emails personales)
- Credenciales de plataformas
- URLs privadas con secretos
- Numeros de telefono operativos internos

Los secretos reales deben vivir en:
- Variables de entorno
- Gestor de secretos
- `.vscode/mcp.json` (ignorado por git)
- `secrets.json` (ignorado por git)

Si detectas un secreto en un archivo versionado, marcalo como CRITICAL y reportalo.

## Resolucion de conflictos

Cuando haya conflicto entre documentos, usar:

> CONFLICTO DETECTADO
> Tema:
> Archivo A:
> Archivo B:
> Diferencia:
> Fuente recomendada:
> Accion sugerida:

## Lecciones aprendidas (memoria persistente)

### Stays.net API
**Endpoints FUNCIONALES (2026-05-18):**
- ✅ `GET /external/v1/booking/reservations` — lista de reservas
- ✅ `GET /external/v1/booking/reservations/{id}` — detalle de reserva
- ✅ `POST /external/v1/booking/search-listings` — buscar listings disponibles (requiere `rooms` como array)

**Endpoints NO FUNCIONALES (404 confirmado en jairop.stays.net):**
- ❌ `POST /external/checkout/initiate`
- ❌ `POST /external/promocodes/create-promo-code`
- ❌ `POST /reservations/booking/reservations/export`
- ❌ `POST /sell-price-rules`
- ❌ `PATCH /v1/parameters/content/properties/{id}` — modificar propiedad
- ❌ `PATCH /parameters/v1/setting/listing/{id}/house-rules` — modificar reglas
- ❌ `GET /v1/parameters/content/properties/{id}` — obtener propiedad
- ❌ `GET /parameters/v1/setting/listing/{id}/house-rules` — obtener reglas
- ❌ `GET /adminmasters/price-groups`
- ❌ `GET /external/settings/app-listing-custom-fields`
- ❌ `POST /external/book-request`
- ❌ `GET /external/v1/listings`
- ❌ `GET /external/v1/properties`
- ❌ `GET /external/docs/index/`

**Conclusión:** Nuestra instancia de Stays.net tiene una API muy limitada. Solo permite **lectura de reservas y búsqueda de listings**. Ningún endpoint de escritura funciona para modificar propiedades, precios, reglas o contenido.

**Mapeo IDs:** reservas devuelven `_idlisting` (MongoDB ObjectId). Directus tiene `AlojamientoStayslistingId` (corto) y `AlojamientoStayslistingIdLargo` (ObjectId)

**Descripciones de anuncios:** no accesibles via API. Obtener del sitio publico sandiegoapart.com

### Scrapling / Chromium
- Las tools HTTP de Scrapling (get, bulk_get) funcionan sin Chromium
- Las tools de browser requieren Chromium con deps de sistema en `~/.local/lib/chrome-deps/`
- BUG: el proceso MCP de Scrapling NO hereda LD_LIBRARY_PATH al lanzar Playwright
- Workaround: usar Python+Playwright directamente desde bash con `export LD_LIBRARY_PATH=...`

> **🔴 DONDE SE DEFINEN LOS MCPs — IMPORTANTE**
>
> **TODOS los servidores MCP de este proyecto se definen en el archivo `opencode.jsonc`** (en la raíz del workspace).
>
> - El cliente OpenCode lee esta configuración al iniciar y lanza/conecta cada servidor.
> - **NO hay otro archivo de configuración MCP**. Ni `mcp.json`, ni settings del sistema, ni variables de entorno globales.
> - Si un MCP no aparece en `opencode.jsonc`, no existe para este workspace.
> - Para modificar un MCP (cambiar su código, agregar tools, cambiar credenciales), editar:
>   1. El archivo `server.py` dentro de `./mcp-servers/{nombre}/`
>   2. Y/o las variables de entorno en la sección `"environment"` de `opencode.jsonc`
>
> Ubicación absoluta: `/mnt/c/Users/jairo/OneDrive/Documents/GitHub/n8n_teknoconecta/opencode.jsonc`

### MCPs disponibles
14 servidores MCP configurados en `opencode.jsonc`: clerk, neon, vercel, openai, jina, perplexity, google-maps, mercadopago, n8n-mcp, supabase, directus, stays-docs, scrapling, pricelabs-docs. (airroi removido — no relevante para el negocio.)

**Tipos de MCP en este proyecto:**
- **Remote**: servidores MCP hospedados por el proveedor (ej. `clerk`, `vercel`, `supabase`). Requieren URL + headers de autenticacion.
- **Local**: servidores MCP ejecutados en la maquina local (ej. `neon`, `openai`, `scrapling`, `n8n-mcp`). Requieren `command` para lanzar el proceso MCP.

### MCPs locales con APIs externas (patron stays-docs / pricelabs-docs)

Algunos MCPs de este proyecto son **locales pero conectan APIs externas**. En vez de llamar directamente a la API desde el agente, se usa un servidor MCP propio que envuelve la API y expone herramientas tipadas.

**Ventajas de este patron:**
- Documentacion embebida: cada tool tiene descripcion, parametros y ejemplos en el servidor MCP
- Validacion de entrada: el servidor MCP valida parametros antes de llamar la API
- Escritura con confirmacion: los servidores de Stays (read-only) y PriceLabs (POST con `confirmed=True`) protegen contra cambios accidentales
- Reutilizable: cualquier agente conectado al mismo MCP obtiene las mismas herramientas

**Como se define en `opencode.jsonc`:**

```json
"stays-docs": {
  "type": "local",
  "command": [
    "uv",
    "run",
    "--directory",
    "/mnt/c/Users/jairo/OneDrive/Documents/GitHub/n8n_teknoconecta",
    "./mcp-servers/stays-docs/server.py"
  ],
  "environment": {
    "STAYS_API_BASE_URL": "https://jairop.stays.net",
    "STAYS_API_KEY": "..."
  }
}
```

**Estructura del servidor MCP local:**
- Ubicacion: `./mcp-servers/{nombre}/server.py`
- Stack: Python + `mcp` SDK (model context protocol)
- Cada servidor define `tools` con nombre, descripcion, parametros (JSON Schema) y handler
- El handler hace la llamada HTTP a la API externa y retorna el resultado formateado

**Ejemplos en este repo:**
| MCP | API externa | Ubicacion servidor | Funcion |
|-----|-------------|-------------------|---------|
| `stays-docs` | Stays.net API | `./mcp-servers/stays-docs/server.py` | Reservas, listings (lectura). Escritura habilitada con `confirmed=True` pero endpoints de Stays devuelven 404 |
| `pricelabs-docs` | PriceLabs API | `./mcp-servers/pricelabs-docs/server.py` | Listings, precios, update/push precios (POST con confirmacion) |

**Reglas para crear un nuevo MCP local con API externa:**
1. Crear carpeta `./mcp-servers/{nombre}/`
2. Implementar `server.py` usando el SDK de MCP en Python
3. Definir tools con descripcion clara, parametros tipados y ejemplos
4. Usar variables de entorno para credenciales (NO hardcodear en el script)
5. Registrar en `opencode.jsonc` con `"type": "local"` y `"command"` que ejecute `uv run`
6. Preferir operaciones read-only a menos que el caso de uso justifique writes
7. Documentar endpoints funcionales vs no funcionales en este archivo (AGENTS.md)

### PriceLabs Academy
- 365 articulos del portal de ayuda PriceLabs en espanol en `documentacion/pricelabs-academy/`
- Organizados en 7 archivos .md por categoria
- URL patron: `https://help.pricelabs.co/portal/es/kb/articles/{slug}`
- El portal es SPA React (Zoho Desk). Requiere browser con JS
- Scripts de scraping: `/tmp/pl_collect_urls.py`, `/tmp/pl_download.py`

### Seguridad detectada en el repo
- CRITICAL: `exportadata/exportar_supabase.ipynb` contiene Supabase anon key + PII de huespedes + direccion personal del host en celdas de output. Debe removerse de git history
- CRITICAL: `exportadata/export_20260504_104837.xlsx` contiene datos de reservas con PII. Debe removerse de git
- HIGH: Varios workflows contienen numeros de telefono y emails hardcodeados. Deben migrarse a credential nodes
- El directorio `09_archive/` existe para contenido deprecated que no debe perderse pero tampoco confundirse con documentacion activa

## Skills / subagentes disponibles

- `sandiegoapart-stays-ops`: operaciones Stays (listings, API, calendarios, reglas)
- `sandiegoapart-brand-ads`: anuncios y marketing trilingue
- `sandiegoapart-guest-messaging`: mensajeria a huespedes
- `sandiegoapart-revenue-pricing`: pricing y finanzas
- `sandiegoapart-building-rules`: reglas del edificio y mantenimiento
- `sandiegoapart-data-curator`: curaduria de conocimiento del repo
- `sandiegoapart-automation-n8n`: automatizacion n8n/MCP
- `graphify`: conocimiento grafico del repo. Mapea todo el proyecto (docs, codigo, datos) en un grafo consultable. Usar `graphify install --platform opencode` para registrar. Output: `graphify-out/graph.html`, `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`.
  - **Usar para**: preguntas cross-dominio (ej: "como se conecta Stays con mensajeria?")
  - **NO usar para**: busqueda de archivos especificos, entender una carpeta, tareas diarias

## Compatibilidad multi-agente

- `AGENTS.md` es la referencia principal
- `CLAUDE.md`, `OPENCODE.md` y `.github/copilot-instructions.md` son archivos delgados que redirigen a este documento sin introducir reglas contradictorias

## graphify

This project has a knowledge graph at `graphify-out/graph.json` (104 nodes, 79 edges).
The graph supplements the directory structure — it does NOT replace it.

**When to use the graph:**
- Cross-module questions: "how does X in operacion connect to Y in automatizacion?"
- Finding unexpected relationships between different domains
- Tracing paths across communities

**When NOT to use the graph (use directory structure instead):**
- Finding specific files (use glob/grep)
- Understanding what a directory contains (read it directly)
- Most day-to-day queries — the directory structure `00_` through `09_` is the primary map

**How to use:**
- `/graphify query "question"` — BFS traversal for broad context
- `/graphify query "question" --dfs` — DFS for specific paths
- `/graphify path "ConceptA" "ConceptB"` — shortest path between concepts
- `/graphify update .` — after code changes (AST-only, no API cost)
- Git hooks installed: auto-rebuilds graph on `git commit` (AST-only, free, no API cost)
