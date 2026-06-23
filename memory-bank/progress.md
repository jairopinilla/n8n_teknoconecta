# Progress — TeknoConecta

> Ultima actualizacion: 2026-06-22
> Este repo (n8n_teknoconecta) es el hub central de coordinacion.
> Los repos de proyectos (`topic_system`, `Procesa_doc`, `gestion_gastos`, `kiosko_laflorida`) son independientes.

## Completado

### Infraestructura VPS
- [x] 32 contenedores Docker (9 Coolify + 16 servicios + 4 workers/infra + 3 Coolify internos)
- [x] 17 redes Docker, principal `coolify` (10.0.1.0/24)
- [x] Cloudflare Tunnel + Access: 20 servicios con HTTPS
- [x] Seguridad: iptables + bind 127.0.0.1, solo puertos 22/80/443 expuestos
- [x] PostgreSQL en redes `coolify` + `postgres_default` (fix conectividad 2026-06-14)
- [x] Redis unificado `redis-topic` (DB 0=topic, 1=procesadoc, 2=RAG)
- [x] Qdrant hardened: API key, docker-compose, healthcheck, docs, tooling
- [x] RAG API: docker-compose en `/opt/homelab/rag/`, repo clonado, build from source

### topic_system — TopicPack AI
- [x] DB `topic_system` creada, user `topic_system_app`, extensiones pgvector + pgcrypto
- [x] Coolify proyectos topic-front + topic-back con auto-deploy
- [x] Dockerfiles creados (`front/Dockerfile`, `back/Dockerfile`) y pusheados
- [x] `source_id` corregido (0→2), `dockerfile_location`, `watch_paths` configurados
- [x] Imágenes Docker built manualmente, compose actualizado con port bindings
- [x] Port bindings Coolify: `127.0.0.1:4285` (front), `127.0.0.1:4286` (back)
- [x] HTTPS: `https://topic.chitaraagenteia.com` y `https://api-topic.chitaraagenteia.com`
- [x] S3 bucket `topicsystem` + IAM user `topic-system-user`
- [x] Celery worker `celery-topic` (docker run manual, conecta a redis-topic:6379/0)
- [x] 11 variables de entorno en Coolify (DATABASE_URL, TOPIC_*, AI keys)
- [x] MCP `topic-system-db` (12 tools) + `aws-topic-system` en opencode.jsonc

### procesadoc — ProcesaDoc
- [x] DB `procesadoc` creada, user `procesadoc_app`
- [x] Coolify proyectos procesadoc-front + procesadoc-back con auto-deploy
- [x] HTTPS: `https://procesadoc.chitaraagenteia.com` y `https://api-procesadoc.chitaraagenteia.com`
- [x] DNS + Cloudflare Tunnel configurados
- [x] DATABASE_URL + 6 AI keys en Coolify env vars
- [x] Qdrant collection `system_procesadoc_bge_m3_1024` (1024 dim, 7 índices payload)
- [x] Redis DB 1 (backend) + DB 2 (RAG) configurados
- [x] RAG API: docker-compose en VPS, .env, repo clonado, git credential helper
- [x] `RAG_API_URL=http://rag-api:8000` en Coolify backend
- [x] MCP `procesadoc-db` (12 tools) en opencode.jsonc

### Qdrant — Base vectorial compartida
- [x] Contenedor hardened: API key, docker-compose, healthcheck (bash /dev/tcp)
- [x] Red `coolify` + `qdrant_default`, puertos 127.0.0.1:6333-6334
- [x] Tooling: init_collections.py, smoke_test.py, backup_snapshot.sh, payload_schema.md, README.md, restore_snapshot.md
- [x] Colección `system_procesadoc_bge_m3_1024` creada con 7 índices de payload
- [x] Aislamiento por workspace_id documentado y verificado

### test_viral
- [x] DB `test_viral` + user `testviral_app`
- [x] `host.docker.internal` no resuelve → fix: postgres en red `coolify`
- [x] DATABASE_URL corregido: `postgresql://testviral_app:...@postgres:5432/test_viral`
- [x] HTTPS: `https://test.chitaraagenteia.com`

### Coolify (todos)
- [x] 9 apps con auto-deploy via GitHub App `coolify-chitara` (source_id=2)
- [x] Watch paths configurados para deploy selectivo
- [x] Port bindings via sed en docker-compose.yaml (API PATCH falla en formato ports_mappings)
- [x] Variables de entorno gestionadas via API `/envs`

### Anteriores (sesiones previas)
- [x] Llave SSH `id_ed25519` copiada de WSL a `C:\Users\jairo\.ssh\` para OpenCode nativo Windows
- [x] 25 workflows de n8n en VPS chitara
- [x] 30 servidores MCP en opencode.jsonc
- [x] Migraciones cloud → chitara: n8n, Directus, Supabase
- [x] Credenciales encriptadas AES-256-CBC, `bash decrypt.sh`
- [x] OpenCode Web (`opencode.chitaraagenteia.com`, Google SSO)
- [x] Hermes Agent (Docker, DeepSeek V4 Pro via OpenRouter)
- [x] Carpeta `obsidian/` como vault de Hermes
- [x] Cloudflare Skills (`.agents/skills/cloudflare/`)
- [x] OpenAlex MCP + PubMed MCP (investigacion academica)
- [x] Carpeta `chitara-jorge/` (grupo "Beers and AI")
- [x] 4 apps Coolify: kiosko-front, kiosko-back, saldito-frontend, saldito-api

### Pricing / SandiegoApart
- [x] 702: base $28,000→$24,000, min $20,000→$18,000
- [x] 709: base $28,000→$25,000
- [x] Push a Stays confirmado

### Asesoría Airbnb — SandiegoApart (2026-06-22)
- [x] Transcripción de asesoría (Gianfranco broker) procesada → `documentacion/Asesorias/insights_airbnb_2026-06-22.md`
- [x] Memory-bank actualizado con diagnóstico y acciones
- [x] Consolidado contenido único en `playbook_renta_corta.md` y eliminados `asesorias.md` + `Asesoria_personal.md` (fuente única, sin legacy)
- [ ] Rehacer fotos horizontales (técnica + ADN por unidad) — todas las unidades
- [ ] Eliminar y recrear anuncio en calificación 4.4
- [ ] Plan de recuperación anuncio en 4.7 (precio bajo + reseñas → 4.85)
- [ ] Reescribir títulos con ubicación (<=50 caracteres)
- [ ] Reestructurar descripción con emojis, solo en español
- [ ] Subir precios a 60 días (cobrando bajo el mercado)
- [ ] Configurar ajuste inteligente por ocupación en PriceLabs
- [ ] Eliminar promoción "10% / 30 noches" duplicada
- [x] Legacy de asesorías eliminados y consolidados en `playbook_renta_corta.md` (fuente única)
- [x] Creado anuncio con emojis ES/EN/PT (`anuncio_emojis_todas_unidades.md`), verificado dentro de límites Airbnb
- [x] Chitara (Telegram): cheat-sheet `obsidian/knowledge/renta_corta.md` + referencia en `hermes-soul.md` (recomendaciones de renta corta)
- [x] Webinar PriceLabs (Daniel Zamata) procesado: insights nuevos en playbook (sección PriceLabs) + cheat-sheet, sin duplicar
- [x] Commit+push de cambios para que Chitara los tome en el VPS (git pull cada 1h)
- [x] Chitara sincronizada al día (`db6319d`) y auto-sync arreglado (`/opt/scripts/hermes-git-sync.sh` con stash/pull --ff-only/pop, cron actualizado y probado)

## En Progreso

- [ ] Grupo "Beers and AI": Obtener Telegram ID de Jorge
- [ ] Grupo "Beers and AI": Configurar en Hermes VPS
- [ ] RAG API: esperar `apps/rag/` en repo Procesa_doc para build + deploy
- [ ] topic_system: verificar auto-deploy funcione en próximo push (ahora debería con source_id=2 + watch_paths + dockerfile_location)

## Pendiente

- [ ] Dar de baja VPS viejo (5.78.152.6)
- [ ] Backup automatico diario a S3 con Healthchecks
- [ ] Configurar Google OAuth en Clerk Dashboard (saldito)
- [ ] Rotar credencial de Directus expuesta en historial git
- [ ] Evaluar migracion OpenCode a Windows nativo (para chrome-devtools-mcp)
- [ ] Crear colección Qdrant para topic_system cuando se necesite

## Known Issues

| Issue | Impacto | Estado |
|-------|---------|--------|
| API Stays.net limitada (3 endpoints) | No se puede modificar contenido | Workaround: panel web |
| Directus app.js parcheado | Se pierde al actualizar imagen | Documentado: re-aplicar |
| Token Directus en historial git | Riesgo seguridad | Pendiente rotacion |
| Coolify MCP: list_apps/deploy_app fallan | Usar API REST via SSH | Workaround estable |
| Coolify proxy Traefik no activo | Conflicta con Nginx 80/443 | Todo via Cloudflare Tunnel |
| OpenCode CLI `run` inestable con DeepSeek | Solo funciona `--model` explicito | Web funciona normal |
| Coolify `ports_mappings` PATCH validation fails | No se puede setear via API | Workaround: sed en docker-compose |
| `chrome-devtools-mcp` no funciona en WSL | Necesita Chrome nativo | Requiere OpenCode en Windows nativo |
| topic-front/topic-back deploy via Coolify falla auto-build | Imágenes built manualmente | Watchers + source_id corregidos, probar en próximo push |

## Metricas

- Workflows n8n: 25
- MCP servers (opencode.jsonc): 30
- Contenedores Docker: 38
- Servicios web con HTTPS: 24 (+2 vaults Obsidian)
- Apps Coolify con auto-deploy: 9
- Puertos expuestos: 3 (22, 80, 443)
- Zonas Cloudflare: 1 (chitaraagenteia.com)
- VPS: 5.252.52.190

## Completado (2026-06-18)

### S3 Backups
- [x] Bucket `chitara-backups` (us-east-1, versioning, lifecycle 30d, public blocked)
- [x] AWS CLI v2 instalado en VPS
- [x] backup-postgres.sh: pg_dumpall + per-DB + coolify-db + S3 upload + weekly
- [x] backup-qdrant.sh: snapshot API + docker cp + S3 upload
- [x] Cron: 0 9 / 30 9 * * * Berlin (3 AM Chile)
- [x] Verificado: postgres ~381 MB, coolify ~1.4 MB, qdrant ~478 MB

### Obsidian Vaults (HTTPS + token)
- [x] Vault beer-and-ai: 14 archivos (Jorge + EAS + chat)
- [x] Vault jairo: 19 archivos (SandiegoApart + TeknoConecta + chat)
- [x] sync-chat-to-vault.py: extrae state.db → daily notes
- [x] Quartz v4.4.0: static sites con graph view, backlinks, search
- [x] Nginx token auth: /TOKEN/ → 200, sin token → 403
- [x] Cloudflare Tunnel: beer-ai + jairo.chitaraagenteia.com
- [x] Cron rebuild cada 15 min
- [x] hermes-soul.md actualizado con reglas proactivas de vaults

### Hermes fix (DeepSeek broken pipe)
- [x] compression.threshold: 0.5 → 0.15
- [x] max_turns: 60 → 40
- [x] session_reset.at_hour: 4 → 8 (4 AM Chile)
- [x] Cron restart diario: 0 8 * * *

### Negocio
- [x] Esquema rotativo reserva Jun-Ago 2026: 10 semanas, 4 deptos, $1,405,253
- [x] Bucket `testviral-app` creado en S3 para otro proyecto
- [x] Chitara respondio en grupo Beer and AI tras fix

### Clasificacion Docker
- [x] 38 contenedores clasificados: infra (5 con volumen), apps estado (14), Coolify (7 sin estado), servicios sin estado (12)
- [x] Sin riesgo de perdida de datos: todos los motores con volumen persistente

### Hermes: Jorge en Beer & AI
- [x] Jorge `8959498850` agregado a `TELEGRAM_ALLOWED_USERS` en docker-compose
- [x] `require_mention: false` + `free_response_channels: -5045911302`
- [x] Chitara lee TODOS los mensajes del grupo sin @mention
- [x] Hermes restarted con nueva config, verificado sin errores

### Test-viral: volume mount persistente
- [x] Diagnostico: Coolify no respeta docker-compose del repo, borra volume mount
- [x] Watchdog `/opt/scripts/testviral-volume-fix.sh` (cron */2 min)
- [x] Repo `jairopinilla/test_viral`: compose con volumes documentados (2 commits)
- [x] Container con volume mount activo: `/data/test-viral/images:/app/public/assets/visual/tests`

### Nginx vaults fix
- [x] `listen [::]:80` IPv6 (Cloudflare Tunnel va por IPv6)
- [x] `try_files \$uri \$uri/ \$uri.html` corregido (escapado mal por heredoc)
- [x] Emojis y em-dashes limpiados de Inicio.md + quartz.config.ts pageTitle

### Procesa_doc Graphify
- [x] Workspace `caso-audios` validado con GraphML real
- [x] Ejecutado `python -m app.cli build-graphify --workspace-id caso-audios` dentro de `rag-api`
- [x] Generados `graph.json` y `GRAPH_REPORT.md` en `/opt/homelab/rag/data/graphify/procesadoc/caso-audios/`
- [x] Resultado verificado: 540 nodos, 611 aristas
- [x] Runbook creado: `documentacion/procesadoc_graphify.md`

### Procesa_doc — Migracion completa a Coolify
- [x] App creada en Coolify (procesadoc-back, UUID ae7b2m3w6janv082js1he4q5)
- [x] 3 fixes: source_id=2 (GitHub App auth), base_directory=/ (estaba en /backend), dockerfile_location=/apps/web/Dockerfile
- [x] Env vars: NODE_ENV + todas las API keys marcadas runtime-only via SQL
- [x] SESSION_SECRET, TAVILY_API_KEY, JINA_API_KEY, MISTRAL_API_KEY, GEMINI_API_KEY agregadas via API
- [x] Port binding: 127.0.0.1:4287→3000 fijo (watchdog /opt/scripts/procesadoc-port-fix.sh, cron */2)
- [x] Cloudflare Tunnel: procesadoc.chitaraagenteia.com → 127.0.0.1:4287
- [x] Container viejo removido (procesadoc-web en 3200)
- [x] Build exitoso con commit a235fff. URL publica: 200 OK
- [x] Detectado que Coolify restart NO actualiza codigo → se necesita build manual

### Neo4j — 3 instancias
- [x] Docker compose en /opt/homelab/neo4j/ con 3 containers (neo4j, neo4j-procesadoc, neo4j-topicsystem)
- [x] Credenciales neo4j/flacavonoteni30. Volumenes persistentes
- [x] Cloudflare Tunnel + DNS: https://neo4j.chitaraagenteia.com → 200 OK
- [x] Documentacion: documentacion/neo4j_chitara.md
- [x] Politica PascalCase + separacion por labels para workspaces documentada

### Fichas de sistemas
- [x] Procesa_doc, Topic System, Saldito analizados en profundidad
- [x] 12 dimensiones documentadas: objetivo, front/back, DB, auth, billing, workers, deploy, integraciones, datos sensibles, flujos criticos, riesgos

### Politica DB + Diagnostic First
- [x] PascalCase documentado con ejemplos Cliente/Compra
- [x] Diagnostic First consolidado: 7 fases, gates de aprobacion, reglas de riesgo
