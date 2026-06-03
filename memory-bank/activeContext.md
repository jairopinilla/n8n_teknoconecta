# Active Context — TeknoConecta

> Ultima actualizacion: 2026-06-03

## Current Focus

**Despliegue gestion_gastos completo** — frontend (Angular+Ionic) y backend (Node.js+Clerk+Neon) en VPS chitara (5.252.52.190) con dominio `https://saldito.chitaraagenteia.com`.

**Migracion a OpenCode Web** — configurando workspace para ser usado via OpenCode Web con DeepSeek como modelo default.

## Estado del sistema

| Componente | Estado | Detalle |
|-----------|--------|---------|
| Frontend saldito | ✅ | `https://saldito.chitaraagenteia.com` |
| Backend API | ✅ | `/health` → `{"status":"ok","database":"ok"}` |
| Auto-provisioning | ✅ | `POST /api/usuarios/ensure` crea Usuario |
| Clerk auth | ⚠️ | Instancia de Emilio (0 users). Pendiente migrar. |
| Coolify backend | ✅ | `saldito-api` en proyecto "Saldito Backend" |
| Coolify frontend | ❌ | nixpacks no soporta Angular 20 |
| DNS | ✅ | `saldito.chitaraagenteia.com` → A → 5.252.52.190 |
| SSL | ✅ | Let's Encrypt (auto-renovacion) |
| Encriptacion | ✅ | opencode.jsonc + credenciales en .enc |

## Infraestructura

### VPS chitara (5.252.52.190)

**22 contenedores Docker** running:
- n8n, Directus, PostgreSQL, Coolify, Supabase (5 modulos), pgAdmin, Uptime Kuma, Code-server, Litellm, Open WebUI, Qdrant, Portainer, Homepage, Shlink, Healthchecks, Dozzle, **saldito-frontend**, **saldito-backend**

**Nginx host** como reverse proxy (no Traefik):
- `/etc/nginx/sites-enabled/` → config de cada dominio
- `saldito` → proxy_pass `127.0.0.1:4200`
- SSL via certbot con Let's Encrypt

### DNS Cloudflare (zone: chitaraagenteia.com)

| Tipo | Nombre | Valor |
|------|--------|-------|
| A | saldito | 5.252.52.190 |
| A | coolify | 5.252.52.190 |
| A | directus | 5.252.52.190 |
| A | code | 5.252.52.190 |
| A | term | 5.252.52.190 |
| A | health | 5.252.52.190 |

### Repositorios

| Repo | Ubicacion | Nota |
|------|-----------|------|
| n8n_teknoconecta | `teknoconecta/n8n_teknoconecta` (privado) | Workspace principal |
| gestion_gastos | `jairopinilla/gestion_gastos` (privado) | Transferido desde teknoconecta org |
| gestion_gastos (VPS) | `/srv/saldito/` | Clonado via token OAuth |

## Proyecto gestion_gastos — Arquitectura de deploy

### Stack
| Capa | Tecnologia |
|------|-----------|
| Frontend | Angular 20 + Ionic 8 (salditoapp) |
| Auth (frontend) | @clerk/clerk-js v6 |
| Backend | Node.js ESM (server.mjs) |
| Auth (backend) | @clerk/backend v1.34 |
| DB | Neon PostgreSQL (old-lab-07457522) |
| Proxy | Nginx host → 127.0.0.1:4200 → Docker nginx → backend:3001 |

### Docker Compose (`/srv/saldito/docker-compose.yml`)
```yaml
backend:
  build: ./backend/Dockerfile (Node 22 Alpine)
  env: DATABASE_URL, CLERK_SECRET_KEY, ALLOW_UNSAFE_DATABASE_ROLE, CORS_ALLOWED_ORIGINS
  network: internal

frontend:
  build: ./frontend/Dockerfile (multi-stage: ng build + nginx)
  ports: "127.0.0.1:4200:80"
  proxy /api → backend:3001
```

### Coolify projects
| Proyecto | UUID |
|----------|------|
| Saldito Backend | w31bjvs7hqf1t3am8i9ufr45 |
| Saldito Frontend | r1qq6daq11mo3ly63o1l5vn7 |

## Comandos clave

```bash
# Verificar salud
curl https://saldito.chitaraagenteia.com/health

# Desencriptar workspace
bash decrypt.sh

# Re-encriptar opencode.jsonc
cat opencode.jsonc | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass pass:5486 -base64 -A > opencode.jsonc.enc

# Deploy gestion_gastos (via script en VPS)
ssh root@5.252.52.190 /srv/saldito/deploy.sh
```

## Blockers

- **Clerk instance**: la actual es de Emilio (0 usuarios). Los usuarios de BD (isaias1984@gmail.com, etc.) tienen Clerk IDs de instancia anterior.
- **Coolify frontend**: nixpacks no compila Angular 20. Solo backend via Coolify.
- **Google OAuth Clerk**: no configurado. El sign-in con Google falla.
