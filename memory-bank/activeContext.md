# Active Context — TeknoConecta

## Current Focus

Optimización de copy de anuncios (listings) para todas las unidades de SandiegoApart, con corrección de conflictos entre anuncio publicado y reglas del repo.

## Recent Changes

- **2026-05-16**: Revisión y mejora de descripciones de anuncios:
  - Se extrajo descripción actual de la unidad 901 desde `sandiegoapart.com`.
  - **CONFLICTO DETECTADO** entre anuncio publicado y `AGENTS.md`:
    - Anuncio dice "Estacionamiento de visitas en edificio" → AGENTS.md dice "No prometer estacionamiento — no hay"
    - Anuncio menciona "cowork, gimnasio y sala gourmet/quinchos" como disponibles → AGENTS.md dice "No hay piscina, gimnasio, quincho, cowork ni terraza común confirmados"
  - Se crearon copys mejorados con emojis para todas las unidades en ES/EN/PT-BR:
    - `03_marketing_y_ads/anuncios_mejorados/anuncio_901_902_702.md` (3 huéspedes)
    - `03_marketing_y_ads/anuncios_mejorados/anuncio_709.md` (2 huéspedes, sin sofá cama)
  - Los nuevos anuncios eliminan promesas no verificadas y siguen tono sobrio/concreto.
- **2026-05-16**: Documentación del patrón MCP local con APIs externas en `AGENTS.md`:
  - Sección "MCPs locales con APIs externas (patron stays-docs / pricelabs-docs)".
  - Incluye ventajas, ejemplo de configuración en `opencode.jsonc`, estructura del servidor, y 7 reglas para crear nuevos MCPs.
- **Commits pendientes de push** (falla autenticación HTTPS en entorno remoto):
  - `33faed0` — docs(AGENTS): document MCP local pattern for external APIs
  - `673663e` — feat(marketing): add improved listing copies with emojis for all units in ES/EN/PT-BR

## Next Steps

1. **🔴 CRÍTICO: Push de commits pendientes** — ejecutar `git push origin main` desde terminal local.
2. **Aplicar copys mejorados a Stays.net** — actualizar títulos, descripciones, bullets y FAQ en el CMS de Stays para las 4 unidades.
3. **Corregir anuncio publicado actual** — eliminar referencias a estacionamiento en edificio y espacios comunes no confirmados.
4. Sincronizar `AlojamientoDescripcion` desde Stays.net (web scraping) hacia Directus para consultas sin scraping.
5. Instalar `playwright install-deps chromium` con sudo para habilitar scraping dinámico.
6. Rotar credencial de Directus expuesta históricamente.

## Active Decisions

- **¿Aplicar copys mejorados directamente en Stays.net o pasar por revisión humana primero?** — Los archivos están listos en `03_marketing_y_ads/anuncios_mejorados/`.
- **¿Cómo manejar el conflicto de estacionamiento/espacios comunes en el anuncio actual publicado?** — Se recomienda eliminar esas menciones para coherencia anuncio↔realidad.

## Blockers

- **Push falla por autenticación HTTPS** — no hay credenciales de GitHub configuradas en el entorno remoto. Solución: ejecutar `git push` desde terminal local del usuario.
- Sin `sudo` en WSL no se pueden instalar dependencias de Chromium para Scrapling.
- La API de Stays.net no expone propiedades ni descripciones; depende del sitio público o del CMS de Stays.
