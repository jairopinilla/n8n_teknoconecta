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
- [x] **Diagnostico completo 4 unidades + ajuste precios (2026-05-25):**
  - 902: base $25k → $27k (+8%), push ejecutado
  - 702: base $32.3k → $28k (-13%), min $22.4k → $20k, push ejecutado
  - 709: base $33.3k → $28k (-16%), min $25.1k → $20k, push ejecutado
  - 901: sin cambios ($28.2k, 93% ocup a 30d)
  - Pendiente manual: descuentos -20% 3+ noches, ultimo minuto -15% 702+709
- [x] **Harness Engineering implementado (2026-05-25):** hooks de verificacion, reglas anti-error, verificacion en capas, limpieza periodica, archivos legacy marcados
- [x] **Migracion Supabase → chitara (2026-05-26):** sandiegoapart recreada, 152 tablas, datos 100% identicos, pgvector/postgis instalados, workaround halfvec documentado en chitara.md
- [x] **Servidor MCP cloudflare (2026-05-25):** 9 herramientas (DNS, Workers, D1, AI Gateway, docs search)
- [x] **Servidor MCP interactive-terminal (2026-05-25):** SSH persistente con sesiones stateful
- [x] **Connection SSH a chitara (2026-05-26):** Setup de llaves SSH documentado. Agente puede conectarse via `ssh root@5.252.52.190`
- [x] **Supabase Studio fix (2026-05-26):** Meta no podia resolver `postgres` — solucion: agregar `postgres_default` al servicio meta en docker-compose.yml. Studio carga schemas correctamente
- [x] **Documentacion SSH VPS (2026-05-26):** Seccion 28 en `chitara.md` y seccion en `AGENTS.md` con procedimiento completo de conexion y ejecucion de comandos
- [x] **Directus instalado en chitara (2026-05-26):** Stack `/opt/homelab/directus/`, conectado a sandiegoapart (152 tablas), Cloudflare tunnel + DNS configurados
- [x] **Directus S3 storage (2026-05-26):** Bucket `sandiegoapart-directus` (us-east-1), upload verificado via API, driver `s3`
- [x] **6 AWS MCPs en opencode.jsonc (2026-05-26):** awsKnowledge, awsApi, awsServerless, awsSnsSqs, awsCloudWatch, awsIam — requieren reinicio
- [x] **Supabase CLI actualizado (2026-05-26):** CURRENT_CLI_VERSION 2.53.6 → 2.101.0
- [x] **Auth keys Supabase Studio (2026-05-26):** JWT secret + ANON_KEY + SERVICE_KEY configurados
- [x] **Cloudflare Access Google SSO (2026-05-26):** n8n, Directus, Supabase Studio y Shlink Web protegidos con autenticacion Google
- [x] **Shlink instalado (2026-05-26):** URL shortener con servidor (go) + web client (links), API funcional
- [x] **MCPs chitara creados (2026-05-26):** n8n-chitara, directus-chitara, supabase-chitara en mcp-servers/ + opencode.jsonc

## In Progress

- [ ] **Migrar 155 archivos Supabase S3 → AWS S3** — archivos estan en bucket `supabase.teknoconecta` (privado), necesita service role key
- [ ] **Reparar n8n en chitara** — requiere recrear DB limpia
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
| **902 tiene 57% ocupacion a 7d (recuperado)** | Ya no esta en crisis | 🟢 Base subida a $27k |
| **709 tiene 33% ocup a 30d con 1 sola reserva** | Unidad mas cara y mas vacia del portafolio | 🟡 Base bajada a $28k, min $20k |
| **702 tiene 30% ocup a 30d** | Precio base era el mas alto sin justificar | 🟡 Base bajada a $28k, min $20k |

## Metrics

- Workflows activos: 10
- Workflows inactivos: 2
- MCP servers: 26
- Propiedades activas: 4 (Tarapacá 901, 902, 702, 709) + 1 test
- Endpoints Stays funcionales: 3
- Endpoints Stays no funcionales: 3
- Zona horaria: America/Santiago
