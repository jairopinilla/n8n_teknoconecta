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
- [x] **Copys mejorados sin emoticones** para todas las unidades en ES/EN/PT-BR:
  - `03_marketing_y_ads/anuncios_mejorados/anuncio_todas_unidades_stays.md` (archivo único, 4 unidades)
- [x] **Descripciones actualizadas en Stays.net** (unidad 702 ya refleja cambios en sitio público)
- [x] **Análisis PriceLabs completo** (ocupación 7d/30d/60d, diagnóstico por unidad)
- [x] **MCP pricelabs-docs modificado** para permitir escritura con confirmación previa (`confirmed=True`)
- [x] **Wrappers específicos de escritura** en pricelabs-docs: update_listings, push_prices, add_listings_data, fetch_prices
- [x] **Bug fix encoding JSON** en pricelabs_api_call (POST/PUT/PATCH)
- [x] **Reglas adicionales con multa de 100 USD** por fumar dentro del estudio
- [x] **MCP stays-docs modificado** para permitir POST/PUT/PATCH con `confirmed=True` (aunque endpoints fallen)
- [x] **Investigación completa de API Stays.net** — 13 endpoints probados, solo 3 funcionan (todos GET/POST de lectura)
- [x] **Protocolo formal de cambios de precios en PriceLabs** — 10 pasos obligatorios documentados en `AGENTS.md`
- [x] **Bug fixes en MCP pricelabs-docs** — nombres de campo corregidos (`base_price`→`base`, `listing`→`listing_id`, auto-append `pms`)
- [x] **Cambios de precios aplicados en 902** — base $25k, min $23k, max $50k, push a Stays ejecutado

## In Progress

- [ ] **Reinicio de opencode** para activar MCP pricelabs-docs con modo escritura
- [ ] **Aplicar cambios de precios en PriceLabs** (propuestos, pendientes de ejecución)
- [ ] **Corregir configuraciones manuales en Stays** (camas, mascotas, gimnasio, tiempo de descanso)

## Planned

- [ ] Sincronizar `AlojamientoDescripcion` desde sandiegoapart.com a Directus
- [ ] Workflow n8n para mantener actualizadas descripciones de anuncios
- [ ] Instalar `sudo playwright install-deps chromium` para habilitar scraping browser
- [ ] Rotar credencial de Directus expuesta en historial
- [ ] Ampliar documentación por workflow (entradas, salidas, tablas)
- [ ] Decidir si sync_workflows.sh debe exportar workflows inactivos
- [ ] Monitorear métricas semanales de PriceLabs (ocupación, ADR, nuevas reseñas)

## Known Issues

| Issue | Impacto | Estado |
|-------|---------|--------|
| API Stays.net es extremadamente limitada (solo 3 endpoints funcionan) | No se puede modificar nada vía API. Todo manual desde CMS | Workaround: panel web de Stays |
| Scrapling browser tools no funcionan en WSL | Sin stealth scraping | Workaround: HTTP tools + jina |
| `search-listings` requiere `rooms` como array | Documentación dice Integer pero API exige Array | Solución: enviar `rooms: [1]` |
| Token Directus expuesto en historial git | Riesgo de seguridad | Pendiente rotación |
| sync_workflows.sh cubre solo workflows activos | Repo tiene inactivos que no se actualizan | Decisión pendiente |
| `AlojamientoDescripcion` es null en Directus | Workflows no pueden consultar descripciones locales | Pendiente sincronización |
| Push falla por falta de auth HTTPS en entorno remoto | Commits no llegan a origin/main | **Workaround: push desde terminal local** |
| **MCP pricelabs-docs requiere reinicio** | Cambios de precios pendientes | **Pendiente: reiniciar opencode** |
| **902 tiene 0% ocupación a 7 días** | Unidad en crisis | **Acción urgente: bajar precio base** |
| **709 tiene 27% ocupación a 30 días** | Precio base más alto del portafolio sin justificación | **Acción: bajar base a $30k** |

## Metrics

- Workflows activos: 10
- Workflows inactivos: 2
- MCP servers: 14
- Propiedades activas: 4 (Tarapacá 901, 902, 702, 709) + 1 test
- Endpoints Stays funcionales: 3
- Endpoints Stays no funcionales: 3
- Zona horaria: America/Santiago
