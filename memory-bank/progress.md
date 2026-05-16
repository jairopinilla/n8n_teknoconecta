# Progress — TeknoConecta

## Completed

- [x] 12 workflows de n8n exportados y versionados
- [x] Documentación canónica (`AGENTS.md`, `README.md`, `guia-repositorio.md`, `tecnologias.md`, `APIStaysDoc.md`)
- [x] 14 servidores MCP configurados en `opencode.jsonc`
- [x] Sección "Lecciones aprendidas" en `AGENTS.md` como memoria persistente
- [x] Mapeo completo de IDs Stays.net ↔ Directus (`Alojamiento`)
- [x] Identificados endpoints Stays.net funcionales vs no funcionales (404)
- [x] Procedimiento documentado para obtener descripciones de anuncios
- [x] Estructura `memory-bank/` creada con 6 archivos
- [x] Script `sync_workflows.sh` funcional
- [x] Instalación de Scrapling y stays-docs MCP
- [x] Skill `grill-me` instalado y codificado como regla obligatoria
- [x] **Documentación del patrón MCP local con APIs externas** en `AGENTS.md` (stays-docs, pricelabs-docs)
- [x] **Revisión de copy de anuncios** desde sitio público `sandiegoapart.com`
- [x] **Detección de conflictos** entre anuncio publicado y reglas del repo (estacionamiento, espacios comunes)
- [x] **Copys mejorados con emojis** para todas las unidades en ES/EN/PT-BR:
  - `03_marketing_y_ads/anuncios_mejorados/anuncio_901_902_702.md` (3 huéspedes)
  - `03_marketing_y_ads/anuncios_mejorados/anuncio_709.md` (2 huéspedes)

## In Progress

- [ ] Push de commits pendientes al remoto (falla autenticación HTTPS en entorno)

## Planned

- [ ] **Aplicar copys mejorados a Stays.net** — actualizar títulos, descripciones, bullets y FAQ en el CMS
- [ ] **Corregir anuncio publicado actual** — eliminar estacionamiento en edificio y espacios comunes no confirmados
- [ ] Sincronizar `AlojamientoDescripcion` desde sandiegoapart.com a Directus
- [ ] Workflow n8n para mantener actualizadas descripciones de anuncios
- [ ] Instalar `sudo playwright install-deps chromium` para habilitar scraping browser
- [ ] Rotar credencial de Directus expuesta en historial
- [ ] Ampliar documentación por workflow (entradas, salidas, tablas)
- [ ] Decidir si sync_workflows.sh debe exportar workflows inactivos

## Known Issues

| Issue | Impacto | Estado |
|-------|---------|--------|
| API Stays.net no expone propiedades ni descripciones | Hay que usar web scraping | Workaround: sitio público |
| Scrapling browser tools no funcionan en WSL | Sin stealth scraping | Workaround: HTTP tools + jina |
| `search-listings` devuelve `[]` | No se pueden buscar alojamientos vía API | Workaround: usar reservas para obtener IDs |
| Token Directus expuesto en historial git | Riesgo de seguridad | Pendiente rotación |
| sync_workflows.sh cubre solo workflows activos | Repo tiene inactivos que no se actualizan | Decisión pendiente |
| `AlojamientoDescripcion` es null en Directus | Workflows no pueden consultar descripciones locales | Pendiente sincronización |
| **Anuncio publicado promete estacionamiento en edificio** | Conflicto con reglas del repo | **Pendiente corrección en Stays.net** |
| **Anuncio publicado menciona cowork/gimnasio/quinchos** | Espacios no confirmados como disponibles | **Pendiente corrección en Stays.net** |
| Push falla por falta de auth HTTPS en entorno remoto | Commits no llegan a origin/main | **Workaround: push desde terminal local** |

## Metrics

- Workflows activos: 10
- Workflows inactivos: 2
- MCP servers: 14
- Propiedades activas: 4 (Tarapacá 901, 902, 702, 709) + 1 test
- Endpoints Stays funcionales: 3
- Endpoints Stays no funcionales: 3
- Zona horaria: America/Santiago
