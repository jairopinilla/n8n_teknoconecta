# Progress — TeknoConecta

## Completed

- [x] 12 workflows de n8n exportados y versionados
- [x] Documentación canónica (`AGENTS.md`, `README.md`, `guia-repositorio.md`, `tecnologias.md`, `APIStaysDoc.md`)
- [x] 14 servidores MCP configurados en `opencode.jsonc`
- [x] Sección "Lecciones aprendidas" en `AGENTS.md` como memoria persistente
- [x] Mapeo completo de IDs Stays.net ↔ Directus (`Alojamiento`)
- [x] Identificados endpoints Stays.net funcionales vs no funcionales (404)
- [x] Estructura `memory-bank/` creada con 6 archivos
- [x] Skill `grill-me` instalado y codificado como regla obligatoria
- [x] **Documentación del patrón MCP local con APIs externas** en `AGENTS.md`
- [x] **Análisis PriceLabs completo** (ocupación 7d/30d/60d, diagnóstico por unidad)
- [x] **MCP pricelabs-docs modificado** para permitir escritura con confirmación previa
- [x] **Protocolo formal de cambios de precios en PriceLabs** — 10 pasos obligatorios
- [x] **Harness Engineering implementado:** hooks de verificacion, reglas anti-error, verificacion en capas
- [x] **Migracion Supabase → chitara:** sandiegoapart recreada, 152 tablas, datos 100% identicos
- [x] **Servidor MCP cloudflare** — 9 herramientas (DNS, Workers, D1, AI Gateway)
- [x] **Conexion SSH a chitara** — setup de llaves documentado
- [x] **Directus instalado en chitara** — stack `/opt/homelab/directus/`, Cloudflare tunnel + DNS
- [x] **Directus S3 storage** — bucket `sandiegoapart-directus` (us-east-1)
- [x] **6 AWS MCPs** en opencode.jsonc
- [x] **Cloudflare Access Google SSO** — todos los servicios protegidos
- [x] **Shlink instalado** — URL shortener con servidor + web client
- [x] **MCPs chitara** — n8n-chitara (12 tools), directus-chitara (25 tools), supabase-chitara (13 tools)

### Sesion 2026-05-29 (infraestructura masiva)

- [x] **Migracion dominio n8n** — `n8n.teknoconectapp.com` → chitara (5.252.52.190)
- [x] **SSL nginx** — Let's Encrypt para n8n, coolify, directus, code, term, health
- [x] **EncryptionKey n8n corregida** — extraida del VPS viejo (5.78.152.6)
- [x] **Migracion 155 archivos Directus cloud → S3** — 97.7 MB, 0 fallos
- [x] **Limpieza DB sandiegoapart** — 53 tablas n8n + 4 huerfanas eliminadas
- [x] **Directus reparado** — deployment tables recreadas, app.js parcheado
- [x] **Coolify instalado** — `coolify.chitaraagenteia.com`, GitHub App conectada
- [x] **Healthchecks instalado** — `health.chitaraagenteia.com`, monitoreo cron jobs
- [x] **Terminal web (ttyd)** — `term.chitaraagenteia.com`, acceso root al VPS
- [x] **Code-server expuesto** — `code.chitaraagenteia.com`, VS Code en navegador
- [x] **Health check 20 servicios Docker** — 18/20 online, 2 reparados
- [x] **Backup completo a S3** — `s3://chitara-backups/`, 343 MB, restore.sh incluido
- [x] **Credenciales encriptadas** — `documentacion/credenciales.enc` (AES-256, clave 5486)
- [x] **Protocolo desencriptado en AGENTS.md** — agente pide clave al usuario
- [x] **Coolify MCP** — `mcp-servers/coolify-mcp/`, deploy apps desde OpenCode
- [x] **Cloudflare DNS management via API** — Global Key permite crear/borrar registros
- [x] **n8n.chitaraagenteia.com desactivado** — DNS borrado, nginx bloquea

## In Progress

- [ ] **Probar Coolify MCP** — requiere reinicio de OpenCode
- [ ] **Configurar cron jobs en Healthchecks** — migrar backups postgres + qdrant
- [ ] **Deployar primer app desde Coolify** — probar con un repo

## Planned

- [ ] Sincronizar `AlojamientoDescripcion` desde sandiegoapart.com a Directus
- [ ] Workflow n8n para mantener actualizadas descripciones de anuncios
- [ ] Rotar credencial de Directus expuesta en historial
- [ ] Ampliar documentación por workflow (entradas, salidas, tablas)
- [ ] Monitorear métricas semanales de PriceLabs (ocupación, ADR, nuevas reseñas)
- [ ] Dar de baja VPS viejo (5.78.152.6)
- [ ] Backup automatico diario a S3 con Healthchecks monitoring
- [ ] Migrar backups de cron a Healthchecks (postgres 3am, qdrant 3:30am)

## Known Issues

| Issue | Impacto | Estado |
|-------|---------|--------|
| API Stays.net es extremadamente limitada (solo 3 endpoints funcionan) | No se puede modificar nada vía API | Workaround: panel web de Stays |
| Push falla por falta de auth HTTPS en WSL | Commits no llegan a origin/main | Workaround: push desde terminal local |
| **Directus app.js parcheado** | Se pierde si se actualiza imagen Docker | Documentado: re-aplicar patch |
| **Token Directus expuesto en historial git** | Riesgo de seguridad | Pendiente rotación |
| **Coolify MCP requiere reinicio** | No disponible hasta reiniciar OpenCode | Pendiente |
| **Supabase Studio en puerto 8001** | Cambiado de 8000 por conflicto con Coolify | Estable |

## Métricas

- Workflows n8n: 25
- Credenciales n8n: 24
- MCP servers: 27 (+ coolify-mcp)
- Contenedores Docker: 20 corriendo
- Archivos Directus S3: 156
- Servicios web expuestos: 6 (n8n, directus, coolify, code, term, health)
- Zona horaria: America/Santiago
- VPS chitara: 5.252.52.190
- VPS viejo: 5.78.152.6 (para dar de baja)
