# Active Context — TeknoConecta

## Current Focus

Servidor chitara (5.252.52.190): **18/20 servicios Docker operativos**. Infraestructura consolidada con dominio principal `n8n.teknoconectapp.com` y servicios expuestos via Cloudflare Access + nginx + Google SSO.

## Cambios de esta sesion (2026-06-01)

### GitHub CLI + autenticacion
- **gh CLI v2.93.0** instalado en `~/.local/bin/gh`
- Autenticado como `jairopinilla` (token classic, scopes: repo, admin:org, workflow, etc.)
- Token encriptado en `credenciales.enc` como `mcp_servers.github.token`
- Organizaciones: SistemaMatematicas, Rukadata, teknoconecta

### Proyecto gestion_gastos — DESPLEGADO ✅ (2026-06-02)

#### Repositorio
- **Repo:** `teknoconecta/gestion_gastos` (privado)
- **Clonado en VPS:** `/srv/saldito/`
- **Autenticación:** GitHub App `chitara_ai` (jairopinilla) + token OAuth para pull

#### Stack
| Capa | Tecnología | Detalle |
|------|-----------|---------|
| Frontend | Angular 20 + Ionic 8 + Capacitor | `salditoapp`, construido con `ng build --configuration production` |
| Backend | Node.js (ESM, `server.mjs`) | `gestion-gastos-backend`, puerto interno 3001 |
| Auth | Clerk (exclusivo) | `@clerk/clerk-js` frontend, `@clerk/backend` backend. Sin Google OAuth directo. |
| DB | Neon PostgreSQL | `control_gastos` (old-lab-07457522), esquema `gestiongastos`, pooled URL |
| Proxy | Nginx (host) | Puerto 80/443 → `127.0.0.1:4200` (frontend Docker) |
| SSL | Let's Encrypt | Expira 2026-08-31, auto-renovación |

#### URLs de producción
| Servicio | URL | Puerto |
|----------|-----|--------|
| **Frontend** | `https://saldito.chitaraagenteia.com` | 443 → nginx → 127.0.0.1:4200 |
| **Backend API** | `https://saldito.chitaraagenteia.com/api` | Proxy via nginx → frontend nginx → backend:3001 |
| **Health** | `https://saldito.chitaraagenteia.com/health` | `{"status":"ok","database":"ok"}` |

#### Docker Compose (`/srv/saldito/docker-compose.yml`)
```yaml
services:
  backend:
    build: ./backend/Dockerfile
    container: saldito-backend
    env: DATABASE_URL, CLERK_SECRET_KEY, CORS_ALLOWED_ORIGINS=*, ALLOW_UNSAFE_DATABASE_ROLE=true
    network: internal (sin puerto público)

  frontend:
    build: ./frontend/Dockerfile (multi-stage: node build + nginx serve)
    container: saldito-frontend
    ports: 127.0.0.1:4200:80 (solo localhost)
    nginx: SPA routing + proxy /api → backend:3001
    network: internal
```

#### Archivos Docker creados
| Archivo | Propósito |
|---------|-----------|
| `backend/Dockerfile` | Node 22 Alpine, `pnpm install --prod`, `node src/server.mjs` |
| `frontend/Dockerfile` | Multi-stage: `ng build` + `nginx:alpine` |
| `frontend/nginx.conf` | SPA (try_files), proxy /api → backend:3001, gzip |
| `docker-compose.yml` | Orquestación de ambos servicios |

#### Configuración Nginx host (`/etc/nginx/sites-enabled/saldito`)
```
server {
    listen 80 → redirect 301 HTTPS
    listen 443 ssl → proxy_pass http://127.0.0.1:4200
    SSL: Let's Encrypt (certbot --nginx)
}
```

#### Variables de entorno (Coolify → ahora en docker-compose)
| Variable | Valor | Nota |
|----------|-------|------|
| `DATABASE_URL` | `postgresql://neondb_owner:npg_...@ep-empty-snow-...pooler.../neondb` | Pooled Neon, RLS bypass |
| `CLERK_SECRET_KEY` | `sk_test_ECOkeWUNYQdWJhpObtEGO0ZAz...` | Clerk secret |
| `CORS_ALLOWED_ORIGINS` | `*` | Abierto para pruebas externas |
| `ALLOW_UNSAFE_DATABASE_ROLE` | `true` | Permite `neondb_owner` (rol unsafe) |

#### DNS Cloudflare
| Tipo | Nombre | Valor | Zona |
|------|--------|-------|------|
| A | `saldito.chitaraagenteia.com` | `5.252.52.190` | `chitaraagenteia.com` |

#### Autenticación (Clerk exclusivo)
- **Frontend:** `ClerkAuthService` (`@clerk/clerk-js` v6.11.0) con UI embebida
- **Publishable key:** `pk_test_Y2hhcm1lZC1saW9uZmlzaC02NS5jbGVyay5hY2NvdW50cy5kZXYk`
- **Backend:** `verifyToken()` de `@clerk/backend` v1.34.0
- **Sin Google OAuth en código** — los providers se configuran en Clerk Dashboard
- **API externa:** accesible con token Clerk válido (`Authorization: Bearer TOKEN`)

#### Comandos de mantenimiento
```bash
# Ver estado
ssh root@5.252.52.190 "docker ps --format '{{.Names}} {{.Status}}' | grep saldito"

# Redeploy (tras git push)
ssh root@5.252.52.190 "cd /srv/saldito && TOKEN=\$(gh auth token) && git pull https://oauth2:\${TOKEN}@github.com/teknoconecta/gestion_gastos.git main && docker compose up -d --build"

# Logs
ssh root@5.252.52.190 "docker logs saldito-backend --tail 20"
ssh root@5.252.52.190 "docker logs saldito-frontend --tail 20"
```

#### Lecciones aprendidas del deploy
1. **Coolify API incompatible** — el MCP usa endpoints de una versión distinta de Coolify. No se pudo usar para el deploy.
2. **Repo privado** — Coolify necesita GitHub App para clonar repos privados. Sin ella, falla el clone.
3. **Traefik no está corriendo** — el proxy real es Nginx en el host, no Traefik. Los labels de Traefik en compose son ignorados.
4. **Nginx host es el reverse proxy** — todos los servicios se exponen via `/etc/nginx/sites-enabled/`. Patrón: proxy_pass a 127.0.0.1:PUERTO.
5. **Certbot integrado** — SSL con Let's Encrypt via nginx plugin. Auto-renovación por systemd timer.
6. **API token Cloudflare DNS** — el token original (`cfat_I9KF...`) solo tenía permisos de analytics. Se creó uno nuevo (`cfat_e43N...`) con permisos Zone:DNS:Edit.

## Cambios de sesion anterior (2026-05-29)

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

### Servicios Docker (20/20 + 2 nuevos)

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
| **21** | **saldito-frontend** | 4200 (127.0.0.1) | ✅ |
| **22** | **saldito-backend** | 3001 (internal) | ✅ |

### DNS
- **teknoconectapp.com:** Google Domains (Squarespace). `n8n` → 5.252.52.190
- **chitaraagenteia.com:** Cloudflare (zone `71a7e23d2f3406a9e755614a51cd3f3c`). Subdominios: n8n, directus, coolify, code, term, health, saldito
- **tarapaca1140.cl:** ELIMINADO de Cloudflare (2026-06-02)
- **Cloudflare API tokens:**
  - `cfat_I9KF...` — analytics/read-only (para cloudflare-dns MCP)
  - `cfat_e43N...` — Zone:DNS:Edit para chitaraagenteia.com (creado 2026-06-02)

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
| **Saldito** | `https://saldito.chitaraagenteia.com` | Gestor de gastos |

## Next Steps

1. **Configurar cron jobs en Healthchecks** — migrar backups existentes
2. **Crear backup automático diario a S3**
3. **Dar de baja VPS viejo (5.78.152.6)**
4. **Configurar Clerk Dashboard** — revisar providers habilitados (email, Google, etc.)
5. **Cerrar CORS** cuando termine fase de pruebas — cambiar `*` por dominio específico

## Blockers

- **Git push falla** por falta de auth HTTPS en WSL — workaround: push desde terminal local del usuario
- **API Stays.net** sin endpoints de escritura
- **Directus app.js parcheado** — se pierde si se actualiza la imagen Docker

## Active Decisions

- **¿DB sandiegoapart?** ✅ Limpia (solo tablas Directus + negocio, sin n8n)
- **¿EncryptionKey n8n?** ✅ `SL2H/UvNuDsNQBjsN/Czty6HiRQA1ida`
- **¿Storage Directus?** ✅ AWS S3 (`sandiegoapart-directus`, us-east-1)
- **¿Autenticacion servicios?** ✅ Cloudflare Access + Google SSO
- **¿Backups?** ✅ S3 (`chitara-backups`) + Healthchecks para monitoreo
