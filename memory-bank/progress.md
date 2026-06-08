# Progress — TeknoConecta

## Completado

- [x] 25 workflows de n8n en VPS chitara
- [x] 27 servidores MCP en `opencode.jsonc`
- [x] Infraestructura VPS: 22 contenedores Docker
- [x] Cloudflare Tunnel + Access: 16 servicios con Google SSO
- [x] Seguridad: iptables + bind 127.0.0.1, solo puertos 22/80/443 expuestos
- [x] Migracion n8n cloud → chitara (dominio `n8n.teknoconectapp.com`)
- [x] Migracion Directus cloud → chitara (`directus.chitaraagenteia.com`)
- [x] Migracion Supabase cloud → chitara (`supabase.chitaraagenteia.com`)
- [x] SSL Let's Encrypt via nginx + certbot
- [x] Credenciales encriptadas: AES-256-CBC, clave 5486, `bash decrypt.sh`
- [x] Protocolo de encriptacion en AGENTS.md (REGLA #0)
- [x] Arquitectura esqueletica en AGENTS.md (REGLA #1)
- [x] Memoria de encriptacion en cada push (REGLA #2)
- [x] Deploy gestion_gastos (saldito) en VPS + dominio + SSL
- [x] Auto-provisioning Clerk→DB (`POST /api/usuarios/ensure`)
- [x] OpenCode Web en chitara (`opencode.chitaraagenteia.com`, Google SSO)
- [x] OpenCode Bridge para Telegram/n8n (puerto 4097, Bearer auth)
- [x] Repo gestion_gastos transferido a `jairopinilla/gestion_gastos`
- [x] Coolify proyectos creados (Backend + Frontend)
- [x] Zona tarapaca1140.cl eliminada de Cloudflare
- [x] Cloudflare Skills instaladas (`.agents/skills/cloudflare/`)
- [x] Datos dummy en gestion_gastos (3 meses, 61 egresos, 5 ingresos)
- [x] Hermes Agent instalado en chitara (Docker, DeepSeek V4 Pro via OpenRouter)
- [x] Carpeta `obsidian/` creada como vault de Hermes con AGENTS.md propio
- [x] Cloudflare Tunnel + Access para dashboard Hermes (`hermes.chitaraagenteia.com`)
- [x] Cron job sync repo cada 1 hora en VPS
- [x] Git configurado en VPS para que Hermes pueda commitear y pushear

## En Progreso

- [ ] Crear bot de Telegram (@BotFather) para Hermes Agent
- [ ] Configurar Telegram gateway en Hermes
- [ ] Configurar Cloudflare Access para hermes.chitaraagenteia.com
- [ ] Importar workflows n8n (Telegram + Notificaciones)
- [ ] Configurar Google OAuth en Clerk Dashboard

## Pendiente

- [ ] Dar de baja VPS viejo (5.78.152.6)
- [ ] Backup automatico diario a S3 con Healthchecks
- [ ] Sincronizar `AlojamientoDescripcion` desde sandiegoapart.com a Directus
- [ ] Rotar credencial de Directus expuesta en historial git
- [ ] Evaluar migracion backend gestion_gastos de Node → Python (ver `documentacion/plan_arquitectura_gastos.md`)

## Known Issues

| Issue | Impacto | Estado |
|-------|---------|--------|
| API Stays.net limitada (3 endpoints) | No se puede modificar contenido | Workaround: panel web |
| Directus app.js parcheado | Se pierde al actualizar imagen | Documentado: re-aplicar |
| Token Directus en historial git | Riesgo seguridad | Pendiente rotacion |
| Coolify frontend: nixpacks falla Angular 20 | Frontend via docker-compose | Workaround estable |
| OpenCode CLI `run` inestable con DeepSeek | Solo funciona `--model` explicito | Web funciona normal |
| Supabase Studio loguea "unhealthy" | Container funciona pero healthcheck falla | Cosmetico |
| Clerk instance sin Google OAuth | Solo email magic link | Pendiente config |
| Google OAuth no configurado en Clerk | No funciona sign-in con Google | Dashboard Clerk |

## Métricas

- Workflows n8n: 25
- MCP servers: 27
- Contenedores Docker: 23
- Servicios web con Google SSO: 17
- Puertos expuestos: 3 (22, 80, 443)
- Zonas Cloudflare: 1 (chitaraagenteia.com)
- Zona horaria: America/Santiago
- VPS: 5.252.52.190
