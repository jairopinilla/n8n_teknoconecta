# Active Context — TeknoConecta

> Ultima actualizacion: 2026-06-23
>
> 🔴 **Directus cloud y Supabase cloud YA NO SE USAN.** Todo en chitara (VPS 5.252.52.190).
> Para operar usar SIEMPRE los MCPs chitara (`n8n-chitara`, `directus-chitara`, `supabase-chitara`).
>
> 🔵 **Este repo (n8n_teknoconecta) es el hub central.** Coordina infra, MCPs, Hermes, Coolify y los otros repos.
> Los repos de proyectos (`topic_system`, `Procesa_doc`, `gestion_gastos`, `kiosko_laflorida`) tienen su propio AGENTS.md y contexto.

## Estado del sistema

| Componente | Estado | Detalle |
|-----------|--------|---------|
| OpenCode Web | ✅ | `https://opencode.chitaraagenteia.com`, Google SSO |
| OpenCode Bridge | ✅ | `127.0.0.1:4097`, Bearer auth, para Telegram/n8n |
| **Hermes Agent** | ✅ | `https://hermes.chitaraagenteia.com`, DeepSeek V4 Pro directo |
| **Obsidian Vaults (NUEVO)** | ✅ | beer-ai + jairo, Quartz static sites, token auth, cron sync 15min |
| **Coolify** | ✅ | 9 proyectos, 9 apps desplegadas con auto-deploy |
| n8n | ✅ | 25 workflows, `n8n.teknoconectapp.com` |
| 20+ servicios web | ✅ | Todos con HTTPS via Cloudflare Tunnel |
| **S3 Backups** | ✅ | PostgreSQL + Qdrant → `chitara-backups`, diario 3 AM Chile |
| Seguridad | ✅ | Solo puertos 22/80/443 expuestos, resto iptables + 127.0.0.1 |
| SSH / OpenCode Windows | ✅ | Llave `id_ed25519` en `C:\Users\jairo\.ssh\`, usable desde Windows nativo |

## Coolify — Apps desplegadas (auto-deploy via GitHub App, source_id=2)

| App | UUID | Dominio | Puerto host | Repo | Watch paths |
|-----|------|---------|-------------|------|-------------|
| kiosko-front | `tjsxn4ds3u6o8onl37fvxctn` | `https://kiosko.chitaraagenteia.com` | 127.0.0.1:4281 | jairopinilla/kiosko_laflorida | `apps/front/**` |
| kiosko-back | `nojhn2t0uvtfbhf39f7w4jky` | `https://api-kiosko.chitaraagenteia.com` | 127.0.0.1:4282 | jairopinilla/kiosko_laflorida | `apps/back/**` |
| saldito-frontend | `v5p0g5emcti9ej4a8ot7ct08` | `https://saldito.chitaraagenteia.com` | 127.0.0.1:4280 | jairopinilla/gestion_gastos | `frontend/*` |
| saldito-api | `p33rw7wj1i4duba954v3d727` | `https://api-saldito.chitaraagenteia.com` | 127.0.0.1:4283 | jairopinilla/gestion_gastos | `backend/*` |
| test-viral-app | `f8kxqoahu0hwlwimhktgjp7t` | `https://test.chitaraagenteia.com` | 127.0.0.1:4284 | jairopinilla/test_viral | (auto) |
| topic-front | `nidwrfwt1a9vu41p0q8x4tns` | `https://topic.chitaraagenteia.com` | 127.0.0.1:4285 | jairopinilla/topic_system | `front/**` |
| topic-back | `tp9delvkuk4tj41fvqe5j87s` | `https://api-topic.chitaraagenteia.com` | 127.0.0.1:4286 | jairopinilla/topic_system | `back/**` |
| procesadoc-front | `m9zorl3mx3iu4ujk6ybwtecc` | `https://procesadoc.chitaraagenteia.com` | 127.0.0.1:4287 | jairopinilla/Procesa_doc | `front/**` |
| procesadoc-back | `ae7b2m3w6janv082js1he4q5` | `https://api-procesadoc.chitaraagenteia.com` | 127.0.0.1:4288 | jairopinilla/Procesa_doc | `backend/**` |

**rag-api:** No usa Coolify. Docker-compose manual en `/opt/homelab/rag/`. Puerto `127.0.0.1:4289`.
**Deploy:** Push a `main` → Coolify redeploy automatico (GitHub App `coolify-chitara`, source_id=2).
**APIs publicas:** HTTPS via Cloudflare Tunnel. Auth es responsabilidad del desarrollador de cada proyecto.
**Coolify API:** `http://localhost:8000/api/v1/` con token `1|GP1qcJjN3Hyi9HmEvyPDfXAoLp0LomhB1Bgul5DEaf517cae`
**Nota:** El MCP `coolify_list_apps` y `coolify_deploy_app` fallan. Usar API REST via SSH como fallback.

## Infraestructura compartida (red `coolify`)

| Servicio | Hostname | Puerto | Notas |
|----------|----------|--------|-------|
| PostgreSQL | `postgres` | 5432 | Redes `coolify` + `postgres_default`. DBs: `topic_system`, `procesadoc`, `sandiegoapart`, `test_viral`, `kioskomunicipio`, `n8n`, `chitara`, `shlink`, `healthchecks` |
| Qdrant | `qdrant` | 6333 | API key obligatoria. Colección por sistema: `system_{slug}_bge_m3_1024` |
| Redis | `redis-topic` | 6379 | Compartido por DB number: 0=topic, 1=procesadoc, 2=RAG |

## PostgreSQL — Fix conectividad Coolify (2026-06-14)

**Problema:** Contenedores Coolify no podían resolver `postgres` (redes separadas).
**Fix:** Agregada red `coolify` como externa en `/opt/homelab/postgres/docker-compose.yml`. PostgreSQL ahora en ambas redes.
**DATABASE_URL correcto:** `postgresql://{user}:{pass}@postgres:5432/{db}` — usar hostname `postgres`, no `host.docker.internal`.

## Qdrant — Base vectorial compartida (2026-06-16)

Servicio de infraestructura multi-tenant. No pertenece a ningún sistema.

| Recurso | Detalle |
|---------|---------|
| **docker-compose** | `/opt/homelab/qdrant/docker-compose.yml` + `.env` |
| **Red** | `coolify` + `qdrant_default` |
| **Puertos** | `127.0.0.1:6333` (REST), `127.0.0.1:6334` (gRPC) |
| **API key** | ✅ Obligatoria |
| **Volumen** | `qdrant_qdrant_storage` |
| **Tooling** | `infra/qdrant/` (README, init_collections.py, smoke_test.py, payload_schema.md, backup_snapshot.sh, restore_snapshot.md) |
| **Colecciones activas** | `system_procesadoc_bge_m3_1024` (1024 dim, Cosine, 7 índices de payload) |
| **Aislamiento** | Por `workspace_id` en payload (filtro `must`), backend impone desde JWT |

## Redis — Instancia unificada

| DB | Sistema | Uso |
|----|---------|-----|
| 0 | topic_system | Celery worker + cache |
| 1 | procesadoc | Backend queue |
| 2 | procesadoc | RAG / LightRAG |

## topic_system — TopicPack AI (2026-06-17)

| Recurso | Detalle |
|---------|---------|
| **DB** | `topic_system`, user `topic_system_app` |
| **Repo** | `jairopinilla/topic_system` (privado) |
| **Frontend** | `https://topic.chitaraagenteia.com` → `127.0.0.1:4285`, Nuxt 3, Dockerfile en `front/` |
| **Backend** | `https://api-topic.chitaraagenteia.com/health` → `127.0.0.1:4286`, FastAPI, Dockerfile en `back/` |
| **Celery** | `celery-topic` (docker run manual, no Coolify), conecta a `redis-topic:6379/0` |
| **S3** | `topicsystem` en us-east-1, IAM user `topic-system-user` |
| **DATABASE_URL** | `postgresql+asyncpg://topic_system_app:...@postgres:5432/topic_system` |
| **MCPs** | `topic-system-db` (12 tools SSH), `aws-topic-system` |
| **Fix Coolify** | Dockerfiles creados y pusheados. `source_id` corregido: 0→2. `dockerfile_location` seteado. `watch_paths` agregados. Imágenes built manualmente, compose recreado con port bindings. |

## procesadoc — ProcesaDoc (2026-06-15)

| Recurso | Detalle |
|---------|---------|
| **DB** | `procesadoc`, user `procesadoc_app` |
| **Repo** | `jairopinilla/Procesa_doc` (privado) |
| **Frontend** | `https://procesadoc.chitaraagenteia.com` → `127.0.0.1:4287` |
| **Backend** | `https://api-procesadoc.chitaraagenteia.com` → `127.0.0.1:4288` |
| **DATABASE_URL** | `postgresql://procesadoc_app:...@postgres:5432/procesadoc` |
| **RAG API** | `/opt/homelab/rag/`, build desde `apps/rag/` del repo, puerto `127.0.0.1:4289` |
| **Qdrant** | `system_procesadoc_bge_m3_1024` |
| **Redis** | DB 1 (backend), DB 2 (RAG) |
| **MCP** | `procesadoc-db` (12 tools SSH) |
| **AI Keys** | OpenAI, DeepSeek, Gemini, Kimi, Mistral — todas en Coolify env vars |
| **Repo VPS** | Clonado en `/opt/homelab/rag/repo/`, git credential helper configurado |

## DNS Cloudflare (zona: chitaraagenteia.com, zone_id: 71a7e23d2f3406a9e755614a51cd3f3c)

Todos los registros son CNAME → `779b9db0-b10e-4048-90e4-e09256d40f39.cfargotunnel.com`, proxied.

| Subdominio | → Puerto host |
|------------|--------------|
| topic.chitaraagenteia.com | 127.0.0.1:4285 |
| api-topic.chitaraagenteia.com | 127.0.0.1:4286 |
| procesadoc.chitaraagenteia.com | 127.0.0.1:4287 |
| api-procesadoc.chitaraagenteia.com | 127.0.0.1:4288 |
| saldito.chitaraagenteia.com | 127.0.0.1:4280 |
| kiosko.chitaraagenteia.com | 127.0.0.1:4281 |
| api-kiosko.chitaraagenteia.com | 127.0.0.1:4282 |
| api-saldito.chitaraagenteia.com | 127.0.0.1:4283 |
| test.chitaraagenteia.com | 127.0.0.1:4284 |

## Contenedores Docker — No Coolify (servicios base + workers)

| Contenedor | docker-compose | Red |
|-----------|---------------|-----|
| `postgres` | `/opt/homelab/postgres/` | `coolify` + `postgres_default` |
| `qdrant` | `/opt/homelab/qdrant/` | `coolify` + `qdrant_default` |
| `redis-topic` | docker run manual | `coolify` |
| `celery-topic` | docker run manual | `coolify` |
| `n8n` | `/opt/homelab/n8n/` | `n8n_default` |
| `directus` | `/opt/homelab/directus/` | `postgres_default` |
| `litellm` | `/opt/homelab/litellm/` | `litellm_default` |
| `open-webui` | `/opt/homelab/open-webui/` | `open-webui_default` |
| `hermes` | `/opt/homelab/hermes/` | `hermes_default` |
| `code-server` | `/opt/homelab/code-server/` | `code-server_default` |
| `homepage` | `/opt/homelab/homepage/` | `homepage_default` |
| `dozzle` | `/opt/homelab/dozzle/` | `dozzle_default` |
| `shlink` | `/opt/homelab/shlink/` | `postgres_default` |
| `supabase-*` | `/opt/homelab/supabase/` | `supabase_supabase_net` |
| `uptime-kuma` | `/opt/homelab/uptime-kuma/` | `uptime-kuma_default` |
| `healthchecks` | `/opt/homelab/healthchecks/` | (host) |
| `portainer` | docker run | (host) |
| `pgadmin` | `/opt/homelab/postgres/` | `postgres_default` |

## MCP servers en opencode.jsonc

30 servidores MCP. Los nuevos de esta sesión:
- `aws-topic-system`: AWS API MCP con credenciales `topic-system-user` (solo bucket `topicsystem`)
- `topic-system-db`: PostgreSQL via SSH (12 tools, DB `topic_system`)
- `procesadoc-db`: PostgreSQL via SSH (12 tools, DB `procesadoc`)

## Comandos clave

```bash
# Desencriptar
bash decrypt.sh

# Re-encriptar opencode.jsonc y credenciales
cat opencode.jsonc | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass pass:5486 -base64 -A > opencode.jsonc.enc
cat documentacion/credenciales | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass pass:5486 -base64 -A > documentacion/credenciales.enc

# Coolify: update app via API
ssh root@5.252.52.190 "curl -s -X PATCH 'http://localhost:8000/api/v1/applications/<UUID>' -H 'Authorization: Bearer 1|GP1qcJjN3Hyi9HmEvyPDfXAoLp0LomhB1Bgul5DEaf517cae' -H 'Content-Type: application/json' -d '{\"key\":\"value\"}'"

# Cloudflared: config + restart
ssh root@5.252.52.190 "cat /etc/cloudflared/config.yml"
ssh root@5.252.52.190 "systemctl restart cloudflared"

# Qdrant: init collection
python infra/qdrant/init_collections.py --host 5.252.52.190 --port 6333 --api-key $KEY --collection system_nuevo_bge_m3_1024 --dim 1024
```

## Blockers

- Coolify MCP: `list_apps` y `deploy_app` fallan → usar API REST via SSH
- Coolify proxy Traefik no activo (conflicta con Nginx en 80/443) → todo via Cloudflare Tunnel
- OpenCode CLI `run` inestable con deepseek-v4-pro → web funciona OK
- `chrome-devtools-mcp` no funciona en WSL → requiere OpenCode nativo en Windows
- Coolify no respeta docker-compose del repo (extra_hosts, volumes) → requiere watchdog scripts

## Cambios recientes (2026-06-18, 2026-06-19, 2026-06-20)

### Procesa_doc — Migracion a Coolify
- App en Coolify: `procesadoc-back` (UUID `ae7b2m3w6janv082js1he4q5`), repo `jairopinilla/Procesa_doc`, rama `main`
- Puerto fijo: `127.0.0.1:4287→3000`. Watchdog `/opt/scripts/procesadoc-port-fix.sh` (cron */2)
- URL: `https://procesadoc.chitaraagenteia.com`
- Builds correctos tras fix de: source_id=2 (GitHub App), base_directory=/, dockerfile /apps/web/Dockerfile
- NODE_ENV y todas las env vars marcadas runtime-only (evita que pnpm saltee devDependencies)
- Contenedor viejo manual (`procesadoc-web` en puerto 3200) eliminado
- Watcher de versión: el restart de Coolify NO actualiza código → necesita build completo desde UI

### Neo4j — Instancias por sistema
- 3 contenedores: `neo4j` (general, Bolt 7687), `neo4j-procesadoc` (Bolt 7688), `neo4j-topicsystem` (Bolt 7689)
- Credenciales: `neo4j` / `flacavonoteni30`
- Neo4j Browser: `https://neo4j.chitaraagenteia.com`
- Compose en `/opt/homelab/neo4j/docker-compose.yml`
- Sin multi-database (Community Edition) — separación lógica por labels: `WorkspaceCasoAudios:Entidad`
- Doc: `documentacion/neo4j_chitara.md`

### Fichas de sistemas
- Procesa_doc, Topic System y Saldito documentados en detalle: objetivo, front/back, DB, auth, workers, deploy, integraciones, riesgos
- Procesa_doc: Nuxt 4 + FastAPI RAG + Qdrant/LightRAG + 5 LLMs. 🔴 Passwords texto plano
- Topic System: Nuxt 3 + FastAPI + Celery + pgvector + Mistral OCR + MCP. 🔴 Passwords texto plano
- Saldito: Angular Ionic + Node.js puro + Neon.tech + Clerk + OpenAI. 🔴 Workflow n8n inactivo

### Politica DB PascalCase + Diagnostic First
- Documentado y consolidado: tablas PascalCase singular, columnas camelCase, PKs NombreTablaId
- Diagnostic First: 7 fases (entendimiento → diagnostico → propuesta → gate aprobacion → plan → ejecucion → validacion)
- Aplica a todos los agentes del ecosistema

### Otros
- Graphify ejecutado para `caso-audios`: 540 nodos, 611 aristas. Output en `/opt/homelab/rag/data/graphify/procesadoc/caso-audios/`
- Doc: `documentacion/procesadoc_graphify.md` y `documentacion/procesadoc_graphify_para_otro_repo.md`
- Docker: 38 contenedores clasificados (servicios vs apps), sin riesgo de pérdida de datos

### SandiegoApart — Asesoría Airbnb (2026-06-22)
- Procesada transcripción de asesoría con Gianfranco (broker). Insights consolidados en `documentacion/insights_airbnb_2026-06-22.md` (transcripción cruda en `documentacion/Asesorias/`, ignorada por git, como respaldo)
- **Diagnóstico clave:** anuncio aparece en 1ª página (impresiones 53%, sano >50%) pero baja conversión de clic (15%, sano >20%) → cuello de botella en FOTOS y TÍTULO, no en precio
- **Pricing:** a 60 días cobrando bajo el mercado (42% vs 17%) → subir precios lejanos; unidad 709 a 7 días en 14% vs mercado 30% → promo agresiva atada a nº noches; ventana de conversión = 7 días
- **Acciones urgentes:** rehacer fotos (horizontales, técnica ombligo/0.5, ADN por unidad), eliminar y recrear anuncio en 4.4, agregar ubicación al título (La Moneda/museos/metro)
- ✅ **Renta corta consolidada:** contenido único de `asesorias.md` y `Asesoria_personal.md` movido a `playbook_renta_corta.md` (reglas del agente, mensajería pre-llegada, scripts de crisis, estilos de branding, prompts soporte/crisis, inversión, operar como negocio). Ambos legacy ELIMINADOS. `playbook_renta_corta.md` es ahora la fuente única (sin archivos legacy paralelos)
- ✅ **Anuncio con emojis (ES/EN/PT):** creado `03_marketing_y_ads/anuncios_mejorados/anuncio_emojis_todas_unidades.md` (ref 901, aplica a las 4 unidades). Descripción + reglas con emoticones, verificadas con script dentro de límites Airbnb (Título 50, Descripción/secciones 500, Reglas 1000). Capacidad: hasta 3 (cama king + sofá cama). Espacios comunes (cowork/gym rooftop/quincho/gourmet/lavandería) INCLUIDOS: usuario confirmó que existen
- ✅ **Discrepancia de espacios comunes RESUELTA:** corregido en `AGENTS.md`, `obsidian/AGENTS.md`, `obsidian/hermes-soul.md`, `obsidian/knowledge/unidades.md`, `00_contexto_negocio/unidades.md`, `00_contexto_negocio/politica_no_sobreprometer.md` y `documentacion/prompt_chitara.md`. Ahora reflejan la realidad: el edificio SÍ tiene espacios comunes (sala cowork, gimnasio al aire libre rooftop, quinchos/sala gourmet, lavandería) sujetos a disponibilidad y coordinación; NO hay estacionamiento propio (público pago a una cuadra) ni piscina
- ✅ **Webinar PriceLabs (Daniel Zamata, gerente LATAM) procesado:** insights nuevos consolidados en la sección PriceLabs de `documentacion/playbook_renta_corta.md` (sin duplicar) + cheat-sheet `obsidian/knowledge/renta_corta.md`. Nuevo: base=promedio anual, sugerencia de base por mercado (3 criterios), percentiles (econ 25-50/medio 50-75/alto 75-90), mínimo 35-40% bajo base, máximo 2-3x base + 3 efectos de cobrar de más, reglas de estadía mínima en cascada, descuentos último minuto graduales y huérfanos semana/finde, perfiles de temporada, refrescar precios = ranking Airbnb, y Smart Pricing de Airbnb NO usar (velocidad vs calidad). Transcripción cruda en `documentacion/Asesorias/` (ignorada). Verificado SIN duplicados: `pricelabs-academy/` (365 artículos) queda como referencia oficial, enlazada desde la sección PriceLabs del playbook (know-how = fuente única; academia = referencia técnica)
- ✅ **Chitara sincronizada (VPS):** forzado `git pull` → `/opt/hermes-workspace` ahora en `db6319d` con todo lo de hoy (insights, playbook, cheat-sheet, espacios comunes, SOUL con sección RECOMENDACIONES). El cambio local de Hermes "Reglas de vaults" en `hermes-soul.md` se preservó vía stash/pop.
- ✅ **Auto-sync de Chitara ARREGLADO:** creado `/opt/scripts/hermes-git-sync.sh` (stash de tracked -> `git merge --ff-only origin/main` -> stash pop -> `infra/sync-hermes-config.sh`), que preserva los cambios locales de Hermes (append "Reglas de vaults" en `hermes-soul.md`) sin congelar el sync. Cron horario actualizado: `0 * * * * bash /opt/scripts/hermes-git-sync.sh >> /var/log/hermes-git-sync.log 2>&1` (backup del crontab en `/root/`). Probado OK: repo en `db6319d`, cambios locales preservados, SOUL.md/AGENTS.md sincronizados, log escrito. Causa raíz previa: el cron viejo hacía `git pull` (merge) que fallaba por el cambio local sin commitear y cortaba el `&&`
- ✅ **Reglas accionables creadas:** `06_automatizacion/reglas_accionables_renta_corta.md` (R1-R14) — convierte las recomendaciones del playbook/insights en reglas con APIs reales (Stays lectura + PriceLabs base/min/max + push), clasificadas 🟢API/🟡UI/🔴Humano y AUTO (diagnóstico) / GATED (precio con aprobación, protocolo AGENTS.md). Enlazado desde `hermes-soul.md`, `playbook_renta_corta.md` y el cheat-sheet. Límite documentado: la API de PriceLabs solo escribe base/min/max; descuentos, min-stay, ajustes por ocupación y ocupación de mercado son solo UI
- ⚡ **Pricing 902 — min=$17K, max=$80K (2026-06-23):** Unidad con 0 reservas 23-30 Jun (14% vs 30% mercado). Finde largo 27-29 Jun con alta demanda. **min bajado** $23K→$17K (margen para días flojos 23-25). **max subido** $50K→$80K (3x base, elimina cap restrictivo para proteger findes largos). Base mantenida en $27K (cerca del recomendado $27.5K). Push a Stays OK. Estructural pendiente: descuentos huérfanos y last-minute (solo UI).
- ✅ **Chitara (Telegram) — recomendaciones de renta corta:** creado cheat-sheet `obsidian/knowledge/renta_corta.md` (condensado del playbook) y agregada sección "RECOMENDACIONES DE RENTA CORTA" en `obsidian/hermes-soul.md` que apunta a `playbook_renta_corta.md` + `documentacion/insights_airbnb_2026-06-22.md`. El insights se movió de `Asesorias/` (ignorada) a `documentacion/` versionada. Commiteado y pusheado al remoto (Hermes hace git pull cada 1h)
