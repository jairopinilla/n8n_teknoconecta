# Active Context — TeknoConecta

## Current Focus

Exploración y documentación de la API de Stays.net para mapear endpoints funcionales vs no funcionales, y establecer el flujo de obtención de descripciones de anuncios.

## Recent Changes

- **2026-05-15**: Se exploró la API de Stays.net. Resultados:
  - Confirmados 3 endpoints funcionales (reservations GET, reservations/{id} GET, checkout POST).
  - Identificados 3 endpoints que devuelven 404 (properties, booking settings, swagger).
  - `search-listings` devuelve array vacío.
  - Las descripciones de anuncios no son accesibles vía API; se extraen del sitio público `sandiegoapart.com`.
  - Se mapearon IDs Stays↔Directus en colección `Alojamiento`.
- Se agregó sección "Lecciones aprendidas" en `AGENTS.md` como memoria persistente.
- Se creó estructura `memory-bank/` con 6 archivos.
- Scrapling instalado pero sus tools de browser no funcionan en WSL por falta de Chromium deps.

## Next Steps

1. Sincronizar `AlojamientoDescripcion` desde Stays.net (web scraping) hacia Directus para consultas sin scraping.
2. Instalar `playwright install-deps chromium` con sudo para habilitar scraping dinámico.
3. Crear workflow en n8n que mantenga actualizadas las descripciones de anuncios.
4. Rotar credencial de Directus expuesta históricamente.
5. Ampliar documentación por workflow con entradas/salidas y tablas afectadas.

## Active Decisions

- ¿Las descripciones se sincronizan a Directus o se consultan on-demand desde la web pública?
- ¿Se usa `jina_read_url` o un workflow de n8n con HTTP Request para el scraping?

## Blockers

- Sin `sudo` en WSL no se pueden instalar dependencias de Chromium para Scrapling.
- La API de Stays.net no expone propiedades; depende del sitio público.
