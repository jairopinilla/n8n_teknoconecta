# Seguimiento del Repositorio

## Como usar este archivo

Este documento es la bitacora viva del repositorio. Toda modificacion sustantiva debe dejar aqui:
- que se hizo
- cual es el estado actual resultante
- cual es el siguiente paso recomendado

## Ultima actualizacion

- Fecha: `2026-05-15` (reorganizacion mayor + auditoria de salud)
- Motivo: auditoria completa del repositorio, deteccion de problemas estructurales/de seguridad, ejecucion de reorganizacion, instalacion de graphify, y revision de salud

## Que se hizo en esta iteracion

### Reorganizacion estructural mayor del repositorio

Se creo la nueva estructura como base de conocimiento y accion (22 archivos nuevos):

- `00_contexto_negocio/`: sandiegoapart.md, unidades.md, ubicacion.md, politica_no_sobreprometer.md, glosario.md (con glosario trilingue completo)
- `01_source_of_truth/stays/`: listings.md, api.md, calendars.md
- `01_source_of_truth/pricelabs/`: pricing_rules.md
- `02_operacion/`: checkin_checkout.md, reglas_huespedes.md, edificio_tarapaca_1140.md, seguridad_camaras.md
- `03_marketing_y_ads/`: marca.md, tono_de_voz.md
- `04_mensajeria/`: checkin.md, durante_estadia.md
- `05_finanzas_y_pricing/`: kpis.md, revenue_management.md
- `06_automatizacion/`: n8n.md, mcp.md
- `08_playbooks/`: publicar_nuevo_anuncio.md, revisar_coherencia_anuncio_realidad.md, responder_huesped.md, actualizar_precios.md, checklist_pre_publicacion.md
- `secrets/`: README.md

Reescritos: AGENTS.md, CLAUDE.md, OPENCODE.md, README.md, copilot-instructions.md, .gitignore

### Clarificacion datos fijos vs dinamicos en AGENTS.md

Agregada seccion explicita: descripciones de anuncios, titulos, amenities activos → Stays API o sandiegoapart.com.
Precios, tarifas, restricciones → PriceLabs. Advertencia: "descripciones de anuncios NO estan en PriceLabs."

### Removido MCP airroi

airroi removido de `.vscode/mcp.json` (no relevante para el negocio). Ahora 14 servidores.
Corregido `06_automatizacion/mcp.md` y `README.md` con el conteo actualizado.

### Instalado graphify

Graphify instalado (v0.7.16) y registrado para OpenCode: `graphify opencode install`.
Hook en `.opencode/plugins/graphify.js` para revisar grafo antes de responder.
Agregado a `AGENTS.md` como skill disponible.

### Inconsistencias corregidas en revision de salud

- `06_automatizacion/mcp.md`: tenia airroi listado (corregido)
- `00_contexto_negocio/sandiegoapart.md`: duplicaba la jerarquia de fuente de verdad (simplificado a referencia)
- `00_contexto_negocio/glosario.md`: faltaba el glosario trilingue de AGENTS.md (agregado)
- `README.md`: deci 15 servidores MCP (corregido a 14)
- `documentacion/seguimiento.md`: secciones duplicadas (limpiado)

### Auditoria de seguridad

- **CRITICAL** `exportadata/exportar_supabase.ipynb`: Supabase anon key + PII huespedes + direccion personal del host en celdas de output. Debe removerse de git history.
- **CRITICAL** `exportadata/export_20260504_104837.xlsx`: Datos de reservas con PII. Debe removerse de git.
- **HIGH** Workflows con telefonos hardcodeados: N8n_Update_Reservas, N8n_Update_Reservas_v2, N8n_SandiegoChatbot, N8n_NotificacionWhats_Aseo, N8n_ProcesaWhatsapp. Migrar a credential nodes.
- **HIGH** Workflows con emails personales hardcodeados: N8n_Update_Reservas, N8n_Update_Reservas_v2.
- **MEDIUM** `documentacion/tecnologias.md` con telefonos operativos expuestos.
- `.gitignore` actualizado: `*.xlsx`, `*.ipynb`, `__pycache__/`, `.venv/`.

### Tareas anteriores (sintesis)

- PriceLabs Academy: 365/370 articulos del portal de ayuda PriceLabs en espanol extraidos y consolidados en `documentacion/pricelabs-academy/` (7 archivos .md).
- Documentado bug de Scrapling MCP: el proceso no hereda LD_LIBRARY_PATH al lanzar Playwright.
- Exploracion API Stays.net: endpoints funcionales (`/external/v1/booking/reservations`), no funcionales (404), y mapeo IDs Stays-Directus.
- Las descripciones de anuncios estan en el sitio publico sandiegoapart.com, no accesibles via API.
- Se creo memory-bank/ con 6 archivos segun patron Memory Bank.
- Se documentaron lecciones aprendidas en AGENTS.md como memoria persistente.

## Estado actual

- Estructura del repositorio: 10 carpetas base (00_ a 09_, secrets/) + documentacion legacy + workflows + mcp-servers
- AGENTS.md es la fuente canonica de instrucciones con orden de lectura, datos fijos vs dinamicos, fuente de verdad, glosario trilingue y lecciones aprendidas
- 14 servidores MCP en `.vscode/mcp.json` (airroi removido)
- 12 workflows exportados en `workflows/` (10 activos, 2 inactivos)
- Graphify instalado y registrado para OpenCode
- Academias: PriceLabs (365 arts), Stays (7 docs legacy)
- Secretos criticos identificados y documentados en `secrets/README.md`

## Proximos pasos recomendados

1. Rotar la credencial de Directus que estuvo expuesta historicamente en documentacion versionada
2. Remover de git history los archivos `exportadata/exportar_supabase.ipynb` y `exportadata/export_20260504_104837.xlsx`
3. Migrar telefonos y emails hardcodeados en workflows a credential nodes de n8n
4. Redactar telefonos operativos en `documentacion/tecnologias.md`
5. Decidir si `sync_workflows.sh` debe exportar tambien workflows inactivos
6. Ampliar documentacion por workflow (entradas, salidas, tablas, dependencias)
7. Ejecutar `/graphify .` desde OpenCode para construir el grafo de conocimiento del repo
8. Agregar plantillas EN y PT-BR en `04_mensajeria/`

## Riesgos y observaciones

- Aunque el token expuesto fue retirado del arbol de trabajo actual, el historial remoto puede seguir conteniendolo. Esto requiere tratamiento operativo fuera de este commit.
- El script de sincronizacion y el contenido actual del repositorio no cubren exactamente el mismo universo de workflows, porque el repo contiene archivos inactivos y el script descarga solo activos.
- `07_data_exports/` y `09_archive/` existen como estructura pero estan vacios (listos para uso futuro).
- `03_marketing_y_ads/` y `04_mensajeria/` tienen contenido minimo; las plantillas EN/PT-BR y guias de Instagram/SEO son pendientes.

## Historial resumido

| Fecha | Cambio | Estado |
|-------|--------|--------|
| 2026-04-30 | Normalizacion de documentacion multi-agente y creacion de bitacora | Completado |
| 2026-05-15 | Exploracion API Stays.net, lecciones aprendidas en AGENTS.md, mapeo Stays-Directus | Completado |
| 2026-05-15 | Scraping PriceLabs (365 art), bug Scrapling MCP documentado | Completado |
| 2026-05-15 | Reorganizacion mayor del repo (22 archivos, nueva estructura), auditoria de seguridad, airroi removido, graphify instalado, revision de salud | Completado |
