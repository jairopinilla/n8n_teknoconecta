# Progress — TeknoConecta

## Completed

- [x] 12 workflows de n8n exportados y versionados
- [x] Documentación canónica (`AGENTS.md`, `README.md`, `guia-repositorio.md`, `tecnologias.md`, `APIStaysDoc.md`)
- [x] 14 servidores MCP configurados en `.vscode/mcp.json`
- [x] Sección "Lecciones aprendidas" en `AGENTS.md` como memoria persistente
- [x] Mapeo completo de IDs Stays.net ↔ Directus (`Alojamiento`)
- [x] Identificados endpoints Stays.net funcionales vs no funcionales (404)
- [x] Procedimiento documentado para obtener descripciones de anuncios
- [x] Estructura `memory-bank/` creada con 6 archivos
- [x] Script `sync_workflows.sh` funcional
- [x] Instalación de Scrapling y stays-docs MCP
- [x] Skill `grill-me` instalado y codificado como regla obligatoria

## In Progress

- (nada activo)

## Planned

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

## Metrics

- Workflows activos: 10
- Workflows inactivos: 2
- MCP servers: 14
- Propiedades activas: 4 (Tarapacá 901, 902, 702, 709) + 1 test
- Endpoints Stays funcionales: 3
- Endpoints Stays no funcionales: 3
- Zona horaria: America/Santiago
