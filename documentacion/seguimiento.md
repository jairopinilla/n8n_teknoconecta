# Seguimiento del Repositorio

## Cómo usar este archivo

Este documento es la bitácora viva del repositorio. Toda modificación sustantiva debe dejar aquí, como mínimo:

- qué se hizo,
- cuál es el estado actual resultante,
- cuál es el siguiente paso recomendado.

## Última actualización

- Fecha: `2026-05-15` (reorganización mayor)
- Motivo: auditoría completa del repositorio, detección de problemas estructurales y de seguridad, y ejecución de reorganización como base de conocimiento y acción para agentes.

## Qué se hizo en esta iteración

### Reorganización estructural mayor del repositorio

Se creó la nueva estructura como base de conocimiento y acción (22 archivos nuevos en 00_ a 09_, secrets/):

- `00_contexto_negocio/`: sandiegoapart.md, unidades.md, ubicacion.md, politica_no_sobreprometer.md, glosario.md
- `01_source_of_truth/stays/`: listings.md, api.md, calendars.md
- `01_source_of_truth/pricelabs/`: pricing_rules.md
- `02_operacion/`: checkin_checkout.md, reglas_huespedes.md, edificio_tarapaca_1140.md, seguridad_camaras.md
- `03_marketing_y_ads/`: marca.md, tono_de_voz.md
- `04_mensajeria/`: checkin.md, durante_estadia.md
- `05_finanzas_y_pricing/`: kpis.md, revenue_management.md
- `06_automatizacion/`: n8n.md, mcp.md
- `08_playbooks/`: publicar_nuevo_anuncio.md, revisar_coherencia_anuncio_realidad.md, responder_huesped.md, actualizar_precios.md, checklist_pre_publicacion.md
- `secrets/`: README.md

Reescritos: AGENTS.md, CLAUDE.md, OPENCODE.md, README.md

### Auditoría de seguridad

- **CRITICAL** `exportadata/exportar_supabase.ipynb`: Supabase anon key + PII huéspedes + dirección personal del host en celdas de output. Debe removerse de git history.
- **CRITICAL** `exportadata/export_20260504_104837.xlsx`: Datos de reservas con PII. Debe removerse de git.
- **HIGH** Workflows con teléfonos hardcodeados: N8n_Update_Reservas, N8n_Update_Reservas_v2, N8n_SandiegoChatbot, N8n_NotificacionWhats_Aseo, N8n_ProcesaWhatsapp. Migrar a credential nodes.
- **HIGH** Workflows con emails personales hardcodeados: N8n_Update_Reservas, N8n_Update_Reservas_v2.
- **MEDIUM** `documentacion/tecnologias.md` con teléfonos operativos expuestos.
- `.gitignore` actualizado: `*.xlsx`, `*.ipynb`, `__pycache__/`, `.venv/`.

### AGENTS.md y documentación de agentes

- AGENTS.md reescrito con: orden de lectura obligatorio, lecciones aprendidas persistentes, jerarquía actualizada, glosario trilingüe, 7 skills documentados, compatibilidad multi-agente.
- CLAUDE.md y OPENCODE.md reescritos como archivos delgados compatibles.

### Tareas anteriores (síntesis)
- PriceLabs Academy: 365/370 artículos del portal de ayuda PriceLabs en español extraídos y consolidados en `documentacion/pricelabs-academy/`.
- Documentado bug de Scrapling MCP (LD_LIBRARY_PATH no heredado).
- Exploración API Stays.net para descripciones de anuncios. Resultados:
- Se exploró la API de Stays.net para obtener descripciones de anuncios. Resultados:
  - El endpoint `/v1/parameters/content/properties/{id}` devuelve 404 tanto con ObjectId como con short ID.
  - El endpoint `/external/docs/index/` (Swagger) también devuelve 404.
  - `/external/v1/booking/search-listings` devuelve `[]`.
  - Las descripciones reales de los anuncios están en el sitio público `sandiegoapart.com` y se extrajeron con `jina_parallel_read_url`.
  - Los 4 anuncios de Tarapacá comparten la misma descripción; solo cambia número de unidad.
  - Directus tiene mapeo entre IDs cortos (FX08J) y largos (ObjectId) en colección `Alojamiento`, pero `AlojamientoDescripcion` está null.
- Se creó estructura `memory-bank/` con 6 archivos (projectbrief, productContext, activeContext, systemPatterns, techContext, progress) según patrón Memory Bank.
- Se enlazó `memory-bank/` en el orden de lectura de `AGENTS.md`, `CLAUDE.md` y `OPENCODE.md`.
- Se agregó sección "Lecciones aprendidas" en `AGENTS.md` como memoria persistente entre sesiones.
- Se documentó el protocolo de "memoria persistente": todo descubrimiento debe registrarse en `AGENTS.md` (Lecciones aprendidas), `tecnologias.md` y `seguimiento.md`.
- Se actualizó `documentacion/tecnologias.md` con tabla de endpoints confirmados, no disponibles y mapeo Stays-Directus.

## Próximo paso recomendado

- Dado que `documentacion/pricelabs-academy/` ya existe con contenido completo, el siguiente paso natural es usar este conocimiento para entrenar o alimentar workflows que requieran respuestas sobre el funcionamiento de PriceLabs.
- Los scripts de scraping (`/tmp/pl_collect_urls.py`, `/tmp/pl_download.py`) quedan disponibles para re-scraping futuro si el portal se actualiza.
- Sincronizar las descripciones de anuncios desde Stays.net hacia Directus (`AlojamientoDescripcion`) para que los workflows puedan consultarlas sin web scraping.
- Instalar dependencias de sistema de Chromium (`sudo playwright install-deps chromium`) para habilitar scraping dinámico y stealth con Scrapling.

- Se creó `AGENTS.md` como fuente canónica y neutral para cualquier asistente de código.
- Se añadió `README.md` como puerta de entrada del repositorio.
- Se añadieron `CLAUDE.md` y `OPENCODE.md` como puntos de entrada compatibles, sin reglas divergentes.
- Se reemplazó el contenido de `.github/copilot-instructions.md` por una versión alineada con la nueva fuente canónica.
- Se creó `documentacion/guia-repositorio.md` con inventario del repo, convenciones y limitaciones conocidas.
- Se sanitizó `documentacion/tecnologias.md` para eliminar un token versionado y se reforzó la política de secretos.
- Se amplió `documentacion/tecnologias.md` para reflejar que el repo usa OpenAI, Google Gemini y Tavily en workflows específicos.
- Se creó `opencode.jsonc` con 12 servidores MCP convertidos desde `.vscode/mcp.json` (6 remote, 6 local).
- Se agregó `opencode.jsonc` a `.gitignore` por contener secretos de conexión.

## Estado actual

- El repositorio tiene 12 workflows exportados en `workflows/`.
- De esas exportaciones, 10 aparecen activas y 2 inactivas en los JSON actuales.
- La instrucción canónica (`AGENTS.md`) ahora incluye sección de "Lecciones aprendidas" como memoria persistente entre sesiones.
- `documentacion/tecnologias.md` diferencia entre endpoints Stays.net que funcionan, los que fallan (404) y los que devuelven vacío.
- Se conoce el mapeo completo Stays-Directus para IDs de anuncios y cómo obtener descripciones desde el sitio público.
- Las herramientas HTTP de Scrapling funcionan; las de browser requieren Chromium deps.
- La academia de PriceLabs en `documentacion/pricelabs-academy/` contiene 365 artículos del portal de ayuda en español, listos para consulta offline o entrenamiento de modelos.

## Próximos pasos recomendados

1. Rotar la credencial de Directus que estuvo expuesta históricamente en documentación versionada.
2. Decidir si `sync_workflows.sh` debe exportar también workflows inactivos o si se mantendrá la limitación actual de forma explícita y permanente.
3. Ampliar la documentación por workflow con entradas, salidas, tablas afectadas y dependencias de credenciales para reducir más el contexto implícito.
4. Probar la conectividad MCP desde OpenCode para verificar que los 12 servidores responden correctamente.

## Riesgos y observaciones

- Aunque el token expuesto fue retirado del árbol de trabajo actual, el historial remoto puede seguir conteniéndolo. Esto requiere tratamiento operativo fuera de este commit.
- El script de sincronización y el contenido actual del repositorio no cubren exactamente el mismo universo de workflows, porque el repo contiene archivos inactivos y el script descarga solo activos.

## Historial resumido

| Fecha | Cambio | Estado |
|-------|--------|--------|
| 2026-04-30 | Se normalizó la documentación para asistentes multi-agente y se creó una bitácora viva del repositorio | Completado |
| 2026-05-15 | Se exploró API Stays.net para obtener descripciones; se documentaron endpoints funcionales/no funcionales; se creó sección "Lecciones aprendidas" en AGENTS.md como memoria persistente; se mapearon IDs Stays↔Directus y URLs públicas de anuncios | Completado |
| 2026-05-15 | Scraping completo del portal de ayuda PriceLabs: 365 artículos en español consolidados en `documentacion/pricelabs-academy/` (7 archivos .md por categoría). Se documentó bug de Scrapling MCP con LD_LIBRARY_PATH | Completado |