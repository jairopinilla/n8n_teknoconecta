# Seguimiento del Repositorio

## Cómo usar este archivo

Este documento es la bitácora viva del repositorio. Toda modificación sustantiva debe dejar aquí, como mínimo:

- qué se hizo,
- cuál es el estado actual resultante,
- cuál es el siguiente paso recomendado.

## Última actualización

- Fecha: `2026-05-15`
- Motivo: exploración de API Stays.net para obtener descripciones de anuncios; implementación de "memoria persistente" en AGENTS.md.

## Qué se hizo en esta iteración

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