# Active Context — TeknoConecta

## Current Focus

Servidor chitara (5.252.52.190): **18/20 servicios Docker operativos**. Infraestructura consolidada con dominio principal `n8n.teknoconectapp.com` y servicios expuestos via Cloudflare Access + nginx + Google SSO.

## Cambios de esta sesion (2026-05-29)

### Migracion n8n cloud → chitara
- **Dominio `n8n.teknoconectapp.com`** ahora apunta a chitara (DNS en Google Domains)
- **SSL:** Let's Encrypt via nginx en chitara
- **EncryptionKey corregida:** `SL2H/UvNuDsNQBjsN/Czty6HiRQA1ida` (extraida del VPS viejo 5.78.152.6)
- **n8n chitara:** 25 workflows, 24 credenciales, DB `n8n` en postgres local
- **n8n.cloud (`n8n-mcp`):** ya no accesible (dominio repunteado a chitara)

### Migracion archivos Directus cloud → S3 chitara
- **155 archivos** migrados de Directus cloud a `s3://sandiegoapart-directus`
- **97.7 MB** transferidos via Python boto3. 0 fallos
- Metadatos ya existian en DB compartida

### Limpieza DB sandiegoapart
- **53 tablas n8n eliminadas** de `sandiegoapart` (n8n usa su propia DB `n8n`)
- **4 tablas huerfanas** (`auth_identity`, `folder_tag`, `processed_data`, `role_scope`) eliminadas
- **Directus corregido:** `directus_deployments` recreado. `app.js` parcheado para saltar `ensureDeploymentWebhooks`

### Nuevos servicios instalados

| Servicio | URL | Auth |
|----------|-----|------|
| **Coolify** | `https://coolify.chitaraagenteia.com` | Google SSO |
| **Healthchecks** | `https://health.chitaraagenteia.com` | Google SSO |
| **Terminal web (ttyd)** | `https://term.chitaraagenteia.com` | Google SSO |
| **Code-server** | `https://code.chitaraagenteia.com` | Google SSO |
| **Directus** | `https://directus.chitaraagenteia.com` | Google SSO |

### Credenciales de servicios

| Servicio | Usuario/Email | Password |
|----------|--------------|----------|
| n8n | admin | ElefantesEbrios1Renca |
| Directus | contacto@teknoconecta.com | ChitaraAdmin2026! |
| Coolify | contacto@teknoconecta.com | CoolifyAdmin2026! |
| Code-server | - | ElefantesEbrios1Renca |
| Healthchecks | contacto@teknoconecta.com | HealthChecks2026! |

### Cloudflare Access (Google SSO)
- **Todos los servicios** protegidos con Google login via Cloudflare Access
- Identity provider: Google (`ffca5d15-e9f0-463d-adfb-30ea0066fe5f`)
- Solo `contacto@teknoconecta.com` autorizado
- DNS gestionado via API (Global Key)

### Backup S3
- **Bucket:** `s3://chitara-backups/`
- **Snapshot:** `chitara_backup_20260529_0028.tar.gz` (343 MB)
- **Contenido:** 4 DBs dump + nginx + docker configs + restore.sh

### Coolify + GitHub
- **GitHub App:** `coolify-chitara` instalada, acceso a todos los repos
- **Coolify MCP:** `mcp-servers/coolify-mcp/` instalado. Herramientas: list/create/deploy apps, proyectos, templates
- **API Token:** configurado en `opencode.jsonc`

### Archivos encriptados
- `documentacion/credenciales.enc` — AES-256, clave `5486`
- `documentacion/decrypt.sh` — script de desencriptado
- **AGENTS.md** actualizado con protocolo de desencriptado

### Servicios Docker (18/20 online)

| # | Servicio | Puerto | Estado |
|---|----------|--------|--------|
| 1 | n8n | 5678 | ✅ |
| 2 | Directus | 8055 | ✅ (parcheado) |
| 3 | PostgreSQL | 5432 | ✅ |
| 4 | Coolify | 8000 | ✅ |
| 5 | Supabase Studio | 8001 | ✅ |
| 6 | Supabase Gotrue | 9999 | ✅ |
| 7 | Supabase Meta | 8080 | ✅ |
| 8 | PostgREST | — | ✅ |
| 9 | pgAdmin | 5050 | ✅ |
| 10 | Uptime Kuma | 3002 | ✅ |
| 11 | Code-server | 8443 | ✅ |
| 12 | Litellm | 4000 | ✅ |
| 13 | Open WebUI | 3001 | ✅ |
| 14 | Qdrant | 6333 | ✅ |
| 15 | Portainer | 9000 | ✅ |
| 16 | Homepage | 3000 | ✅ |
| 17 | Shlink | 8087 | ✅ |
| 18 | Healthchecks | 8100 | ✅ |
| 19 | Dozzle | 8088 | ✅ |
| 20 | Shlink Web | 8089 | ✅ |

### DNS
- **teknoconectapp.com:** Google Domains (Squarespace). `n8n` → 5.252.52.190
- **chitaraagenteia.com:** Cloudflare (zone `71a7e23d2f3406a9e755614a51cd3f3c`). Subdominios: n8n, directus, coolify, code, term, health
- **Cloudflare Global Key:** (encriptada en `credenciales.enc`)

### Patches aplicados
- **Directus `app.js`:** `ensureDeploymentWebhooks` saltado (tablas deployment corruptas)
- **Coolify MCP:** tsconfig relajado, require paths corregidos, `type: module` removido

## Servicios accesibles desde celular

| Servicio | URL | Uso |
|----------|-----|-----|
| Terminal | `https://term.chitaraagenteia.com` | Bash directo a chitara |
| VS Code | `https://code.chitaraagenteia.com` | Editor completo |
| Coolify | `https://coolify.chitaraagenteia.com` | Deploy apps |
| Directus | `https://directus.chitaraagenteia.com` | CMS / DB visual |
| Healthchecks | `https://health.chitaraagenteia.com` | Monitoreo cron jobs |
| n8n | `https://n8n.teknoconectapp.com` | Workflows |

## Next Steps

1. **Configurar cron jobs en Healthchecks** — migrar backups existentes
2. **Probar Coolify MCP** — requiere reinicio de OpenCode
3. **Deployar apps desde Coolify** — `n8n_teknoconecta` y otros repos
4. **Crear backup automático diario a S3**
5. **Dar de baja VPS viejo (5.78.152.6)**

## Blockers

- **OpenCode necesita reinicio** para cargar MCPs nuevos (coolify-mcp, AWS)
- **Git push falla** por falta de auth HTTPS en WSL — workaround: push desde terminal local del usuario
- **API Stays.net** sin endpoints de escritura
- **Directus app.js parcheado** — se pierde si se actualiza la imagen Docker

## Active Decisions

- **¿DB sandiegoapart?** ✅ Limpia (solo tablas Directus + negocio, sin n8n)
- **¿EncryptionKey n8n?** ✅ `SL2H/UvNuDsNQBjsN/Czty6HiRQA1ida`
- **¿Storage Directus?** ✅ AWS S3 (`sandiegoapart-directus`, us-east-1)
- **¿Autenticacion servicios?** ✅ Cloudflare Access + Google SSO
- **¿Backups?** ✅ S3 (`chitara-backups`) + Healthchecks para monitoreo
