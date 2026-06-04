# Active Context — TeknoConecta

> Ultima actualizacion: 2026-06-04
>
> 🔴 **Directus cloud y Supabase cloud YA NO SE USAN.** Todo en chitara (VPS 5.252.52.190).
> Para operar usar SIEMPRE los MCPs chitara (`n8n-chitara`, `directus-chitara`, `supabase-chitara`).

## Estado del sistema

| Componente | Estado | Detalle |
|-----------|--------|---------|
| OpenCode Web | ✅ | `https://opencode.chitaraagenteia.com`, Google SSO |
| OpenCode Bridge | ✅ | `127.0.0.1:4097`, Bearer auth, para Telegram/n8n |
| Saldito Frontend | ✅ | `https://saldito.chitaraagenteia.com`, Angular 20 + Ionic 8 |
| Saldito Backend | ✅ | `/health`, auto-provisioning Clerk→DB |
| Coolify Backend | ⏸️ | Detenido (usamos docker-compose) |
| Coolify Frontend | ❌ | nixpacks no soporta Angular 20 |
| Clerk | ⚠️ | Instancia compartida, 2 usuarios (Jairo + Emilio) |
| n8n | ✅ | 25 workflows, `n8n.teknoconectapp.com` |
| 16 servicios web | ✅ | Todos con Google SSO via Cloudflare Access |
| Seguridad | ✅ | Solo puertos 22/80/443 expuestos, resto iptables + 127.0.0.1 |

## Infraestructura

### VPS chitara (5.252.52.190) — 22 contenedores

| Servicio | Puerto | Acceso |
|----------|--------|--------|
| n8n | 5678 | Google SSO |
| Directus | 8055 | Google SSO |
| PostgreSQL | 5432 | 127.0.0.1 |
| Coolify | 8000 | Google SSO |
| Supabase Studio | 8001 | Google SSO |
| Supabase GoTrue | 9999 | 127.0.0.1 |
| Supabase Meta | 8080 | 127.0.0.1 |
| PostgREST | 3100 | 127.0.0.1 |
| pgAdmin | 5050 | Google SSO |
| Uptime Kuma | 3002 | Google SSO |
| Code-server | 8443 | Google SSO |
| Litellm | 4000 | Google SSO |
| Open WebUI | 3001 | Google SSO |
| Qdrant | 6333 | 127.0.0.1 |
| Portainer | 9000 | Google SSO |
| Homepage | 3000 | Google SSO |
| Shlink | 8087 | Google SSO |
| Shlink Web | 8089 | Google SSO |
| Healthchecks | 8100 | Google SSO |
| Dozzle | 8088 | Google SSO |
| Saldito Frontend | 4200 | Clerk JWT |
| Saldito Backend | 3001 | Interno |

### Capas de seguridad

| Capa | Mecanismo |
|------|-----------|
| Cloudflare Tunnel | `*.chitaraagenteia.com` → Google SSO → localhost |
| Cloudflare Access | 16 apps con Google identity provider |
| iptables DOCKER-USER | Bloquea acceso externo a puertos Docker |
| iptables INPUT | Bloquea acceso externo a puertos de host |
| Docker compose | Servicios bind a `127.0.0.1` |
| Nginx | Solo expone 80/443 |

### Puertos expuestos a internet

| Puerto | Servicio | Motivo |
|--------|----------|--------|
| 22 | SSH | Acceso admin |
| 80 | Nginx | Web |
| 443 | Nginx | Web + SSL |

## Proyecto gestion_gastos (saldito)

### Stack
| Capa | Tecnologia |
|------|-----------|
| Frontend | Angular 20 + Ionic 8 (salditoapp) |
| Auth | Clerk (@clerk/clerk-js + @clerk/backend) |
| Backend | Node.js ESM (server.mjs), puerto 3001 |
| DB | Neon PostgreSQL (old-lab-07457522) |
| Proxy | Nginx host → 127.0.0.1:4200 → Docker nginx → backend:3001 |

### Deploy
- **Repo**: `jairopinilla/gestion_gastos` (privado)
- **VPS**: `/srv/saldito/docker-compose.yml`
- **Deploy script**: `/srv/saldito/deploy.sh`
- **Dominio**: `https://saldito.chitaraagenteia.com`

### Coolify (organizacion)
| Proyecto | UUID | Apps |
|----------|------|------|
| Saldito Backend | w31bjvs7hqf1t3am8i9ufr45 | saldito-api (detenido) |
| Saldito Frontend | r1qq6daq11mo3ly63o1l5vn7 | (vacio) |

## Telegram Bridge

| Componente | Detalle |
|-----------|--------|
| Bridge | `opencode-bridge.service` :4097 |
| Auth | Bearer `chitara-bridge-2026` |
| Bind | `127.0.0.1` (solo local) |
| Workflows | `n8n/workflows/N8n_ChitaraBot_Telegram.json` |
| Notificaciones | `n8n/workflows/N8n_NotificaCheckins.json` |
| Valentina | chat_id: 56982737381, contexto aseo (2d past / 7d future) |

## Comandos clave

```bash
# Desencriptar
bash decrypt.sh

# Deploy saldito
ssh root@5.252.52.190 /srv/saldito/deploy.sh

# Ver salud
curl https://saldito.chitaraagenteia.com/health

# Re-encriptar opencode.jsonc
cat opencode.jsonc | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass pass:5486 -base64 -A > opencode.jsonc.enc
```

## Blockers

- Clerk: instancia de desarrollo, Google OAuth no configurado
- Coolify frontend: nixpacks no compila Angular 20
- OpenCode CLI `run`: inestable con modelo deepseek-v4-pro (funciona via web)
