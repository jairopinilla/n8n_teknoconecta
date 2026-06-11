# Progress — TeknoConecta

> Este repo (n8n_teknoconecta) es el hub central de coordinacion.
> Los repos de proyectos (`gestion_gastos`, `kiosko_laflorida`) son independientes.

## Completado

- [x] 25 workflows de n8n en VPS chitara
- [x] 29 servidores MCP en `opencode.jsonc` (27 originales + openalex + pubmed)
- [x] Infraestructura VPS: ~25 contenedores Docker
- [x] Cloudflare Tunnel + Access: 20 servicios con HTTPS
- [x] Seguridad: iptables + bind 127.0.0.1, solo puertos 22/80/443 expuestos
- [x] Migracion n8n cloud → chitara (`n8n.teknoconectapp.com`)
- [x] Migracion Directus cloud → chitara (`directus.chitaraagenteia.com`)
- [x] Migracion Supabase cloud → chitara (`supabase.chitaraagenteia.com`)
- [x] SSL Let's Encrypt via nginx + certbot
- [x] Credenciales encriptadas: AES-256-CBC, clave 5486, `bash decrypt.sh`
- [x] Protocolo de encriptacion en AGENTS.md (REGLA #0)
- [x] Arquitectura esqueletica en AGENTS.md (REGLA #1)
- [x] Memoria de encriptacion en cada push (REGLA #2)
- [x] OpenCode Web en chitara (`opencode.chitaraagenteia.com`, Google SSO)
- [x] OpenCode Bridge para Telegram/n8n (puerto 4097, Bearer auth)
- [x] Cloudflare Skills instaladas (`.agents/skills/cloudflare/`)
- [x] Hermes Agent en chitara (Docker, DeepSeek V4 Pro via OpenRouter)
- [x] Carpeta `obsidian/` como vault de Hermes con AGENTS.md propio
- [x] Cloudflare Tunnel + Access para dashboard Hermes (`hermes.chitaraagenteia.com`)
- [x] Cron job sync repo cada 1 hora en VPS
- [x] Git configurado en VPS para que Hermes pueda commitear y pushear

### Completado sesion 2026-06-11

- [x] **Coolify: 4 apps desplegadas con auto-deploy** (kiosko-front, kiosko-back, saldito-frontend, saldito-api)
- [x] **Port mappings Coolify** → todos bind a `127.0.0.1` (via DB directa, API no soporta formato)
- [x] **Cloudflare Tunnel:** 3 dominios nuevos (`kiosko.chitaraagenteia.com`, `api-kiosko.chitaraagenteia.com`, `api-saldito.chitaraagenteia.com`)
- [x] **DNS CNAME:** 3 registros creados via `cloudflared tunnel route dns`
- [x] **Env vars Coolify:** `NEXT_PUBLIC_API_URL` actualizado en kiosko-front y saldito-frontend
- [x] **Watch paths:** kiosko-front (`apps/front/**`), kiosko-back (`apps/back/**`) — monorepo con deploy selectivo
- [x] **Hermes Telegram:** Valentina autorizada (chat_id: 8516014121) en `config.yaml` + `SOUL.md`
- [x] **Contenedor huerfano:** `competent_payne` eliminado (125MB recuperados)
- [x] **OpenAlex MCP:** Clonado `drAbreu/alex-mcp` → `mcp-servers/openalex/`, API key premium agregada, PEP 723 metadata. En este repo + Chitara.
- [x] **PubMed MCP:** `@cyanheads/pubmed-mcp-server` via npx. En este repo + Chitara. NCBI API key configurada.
- [x] **opencode.jsonc re-encriptado** con los nuevos MCPs

## En Progreso

- [ ] Configurar Google OAuth en Clerk Dashboard (saldito)

## Pendiente

- [ ] Dar de baja VPS viejo (5.78.152.6)
- [ ] Backup automatico diario a S3 con Healthchecks
- [ ] Sincronizar `AlojamientoDescripcion` desde sandiegoapart.com a Directus
- [ ] Rotar credencial de Directus expuesta en historial git

## Known Issues

| Issue | Impacto | Estado |
|-------|---------|--------|
| API Stays.net limitada (3 endpoints) | No se puede modificar contenido | Workaround: panel web |
| Directus app.js parcheado | Se pierde al actualizar imagen | Documentado: re-aplicar |
| Token Directus en historial git | Riesgo seguridad | Pendiente rotacion |
| Coolify MCP: list_apps/deploy_app fallan | Usar API REST via SSH | Workaround estable |
| Coolify proxy Traefik no activo | Conflicta con Nginx 80/443 | Todo via Cloudflare Tunnel |
| OpenCode CLI `run` inestable con DeepSeek | Solo funciona `--model` explicito | Web funciona normal |
| Supabase Studio loguea "unhealthy" | Container funciona pero healthcheck falla | Cosmetico |

## Metricas

- Workflows n8n: 25
- MCP servers (opencode.jsonc): 29
- MCP servers Hermes (Chitara): 5 (chitara, jina, tavily, openalex, pubmed)
- Contenedores Docker: ~25
- Servicios web con HTTPS: 20
- Apps Coolify con auto-deploy: 4
- Puertos expuestos: 3 (22, 80, 443)
- Zonas Cloudflare: 1 (chitaraagenteia.com)
- Zona horaria: America/Santiago
- VPS: 5.252.52.190 (47GB RAM, 12 CPUs, 484GB disco)
