Eres un agente de infraestructura. Tu tarea es conectarte a chitara (VPS en 5.252.52.190), integrarte con Coolify, entender los servicios Docker existentes, y preparar el deploy de gestion_gastos (saldito) via Coolify.

---

## 🔐 PASO 0 — Acceso SSH a Chitara

Ejecuta esto ANTES de cualquier otra cosa:

```bash
# Generar llave SSH (si no existe)
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "opencode@teknoconecta"

# Mostrar llave publica
cat ~/.ssh/id_ed25519.pub
```

Pide al usuario que agregue esta llave al VPS:
```bash
ssh root@5.252.52.190 "mkdir -p ~/.ssh && echo 'LLAVE_PUBLICA' >> ~/.ssh/authorized_keys"
```

Prueba conexion:
```bash
ssh -o StrictHostKeyChecking=accept-new root@5.252.52.190 "echo CONECTADO"
```

---

## 🖥️ VPS Chitara — 5.252.52.190

### Datos de acceso
- **IP**: 5.252.52.190
- **Usuario**: root
- **SSH**: key-based (la que generaste arriba)

### Servicios Docker (22 contenedores)

| Contenedor | Puerto | Descripcion |
|-----------|--------|-------------|
| n8n | 5678 | Automatizaciones (25 workflows) |
| directus | 8055 | CMS headless |
| postgres | 5432 | BD principal (VPS, NO Neon) |
| coolify | 8000:8080 | Plataforma de deploy |
| coolify-db | 5432 (interno) | BD de Coolify |
| coolify-redis | 6379 (interno) | Cache Coolify |
| supabase-studio | 8001 | UI de Supabase |
| supabase-gotrue | 9999 | Auth Supabase |
| supabase-meta | 8080 | API Supabase |
| pgadmin | 5050 | Admin PostgreSQL |
| uptime-kuma | 3002 | Monitoreo |
| code-server | 8443 | VS Code web |
| litellm | 4000 | Proxy LLM |
| open-webui | 3001:8080 | ChatGPT-like UI |
| qdrant | 6333 | Vector DB |
| portainer | 9000, 9443 | Admin Docker |
| homepage | 3000 | Dashboard homelab |
| shlink | 8087 | URL shortener |
| shlink-web | 8089 | UI Shlink |
| healthchecks | 8100 | Cron monitoring |
| dozzle | 8088 | Logs Docker |
| **saldito-frontend** | 4200 (127.0.0.1) | Angular 20 + Ionic 8 |
| **saldito-backend** | 3001 (interno) | Node.js API |

### Reverse Proxy
- **Nginx** en el host (NO Traefik). Traefik esta instalado via Coolify pero esta apagado (exited).
- Configuracion: `/etc/nginx/sites-enabled/`
- SSL: Let's Encrypt via certbot
- Dominios principales:
  - `n8n.teknoconectapp.com`
  - `*.chitaraagenteia.com` (coolify, directus, code, term, health, opencode, saldito)

---

## 🚀 Coolify — https://coolify.chitaraagenteia.com

### API Access
```
URL: https://coolify.chitaraagenteia.com
Token: <ver documentacion/credenciales.enc → clave 5486 → seccion COOLIFY_API_TOKEN>
```

### Credenciales web
- **Email**: contacto@teknoconecta.com
- **Password**: CoolifyAdmin2026!

### Endpoints API utiles

```bash
# Usar el token Coolify del archivo encriptado
COOLIFY_TOKEN="<ver documentacion/credenciales.enc>"
API="https://coolify.chitaraagenteia.com"

# Listar proyectos
curl -s -H "Authorization: Bearer $COOLIFY_TOKEN" "$API/api/v1/projects"

# Crear app via GitHub App (repos privados)
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://coolify.chitaraagenteia.com/api/v1/applications/private-github-app" \
  -d '{
    "project_uuid":"PROJECT_UUID",
    "environment_name":"production",
    "server_uuid":"lxuop8wbcmf7jq75a0ibz6n0",
    "name":"app-name",
    "git_repository":"jairopinilla/gestion_gastos.git",
    "git_branch":"main",
    "ports_exposes":"3001",
    "base_directory":"/backend",
    "build_pack":"nixpacks",
    "github_app_uuid":"in5o5vekkzc1uv1m9noy234e"
  }'

# Iniciar/deployar app
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  "https://coolify.chitaraagenteia.com/api/v1/applications/APP_UUID/start"

# Establecer env vars
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://coolify.chitaraagenteia.com/api/v1/applications/APP_UUID/envs" \
  -d '{"key":"VAR_NAME","value":"var_value","is_buildtime":false,"is_preview":false}'
```

### Proyectos Coolify existentes

| Proyecto | UUID | Apps |
|----------|------|------|
| Saldito Backend | w31bjvs7hqf1t3am8i9ufr45 | saldito-api (running) |
| Saldito Frontend | r1qq6daq11mo3ly63o1l5vn7 | (vacio - nixpacks falla con Angular 20) |

### GitHub App
- **Nombre**: coolify-chitara
- **UUID**: in5o5vekkzc1uv1m9noy234e
- **Private Key UUID**: tu00yk3luit3qakalphwy3vr
- **Instalada en**: jairopinilla (cuenta personal, 27 repos)
- **Server UUID**: lxuop8wbcmf7jq75a0ibz6n0 (localhost)
- **Destination UUID**: tbkzt4wko48irq6xggjh05m1

---

## 📦 Proyecto gestion_gastos (saldito)

### Repositorio
- **GitHub**: jairopinilla/gestion_gastos (privado)
- **Stack**: Angular 20 + Ionic 8 (frontend) / Node.js + Clerk + Neon (backend)
- **Monorepo**: frontend/ + backend/ + workers/

### Dockerfiles
- `backend/Dockerfile`: Node 22 Alpine, pnpm, server.mjs en puerto 3001
- `frontend/Dockerfile`: Multi-stage (ng build + nginx:alpine)
- `frontend/nginx.conf`: SPA routing + proxy /api → backend:3001
- `docker-compose.yml`: orquestacion ambos servicios

### Deploy actual (docker-compose en VPS)
- Ubicacion: `/srv/saldito/`
- Deploy script: `/srv/saldito/deploy.sh`
```bash
ssh root@5.252.52.190 "/srv/saldito/deploy.sh"
```

### Variables de entorno (backend)
```
DATABASE_URL=<ver documentacion/credenciales.enc → clave 5486 → seccion NEON>
CLERK_SECRET_KEY=<ver documentacion/credenciales.enc → clave 5486 → seccion CLERK>
ALLOW_UNSAFE_DATABASE_ROLE=true
CORS_ALLOWED_ORIGINS=*
```

### Dominio produccion
- `https://saldito.chitaraagenteia.com` (Cloudflare tunnel)
- Health: `{"status":"ok","database":"ok"}`

---

## 🔐 Protocolo de encriptacion

Al clonar el workspace `jairopinilla/n8n_teknoconecta`, ejecutar:
```bash
bash decrypt.sh    # clave: 5486
```

Esto desencripta:
- `opencode.jsonc` (27 MCPs con todos los tokens)
- `documentacion/credenciales` (passwords de infra)

Los archivos planos estan en `.gitignore`. NUNCA borrarlos despues de desencriptar.

---

## 🎯 Tu mision

1. **Conectate a chitara** via SSH (genera llave, pide al usuario que la agregue)
2. **Explora los servicios Docker** corriendo (`docker ps`)
3. **Integrate con Coolify** via API (token arriba)
4. **Evalua los proyectos Coolify** existentes para gestion_gastos
5. **Prepara el deploy del frontend** en Coolify (el backend ya esta deployado)
6. **Registra TODO** en el memory bank de tu sesion
7. **No modifiques** los otros servicios (n8n, directus, etc.) - solo observa

### Restricciones
- NO borrar/modificar servicios existentes
- NO exponer tokens en texto plano (usa variables de entorno)
- Documentar cada accion en tu memory bank
- El repo `jairopinilla/n8n_teknoconecta` es el workspace canonico
- El repo `jairopinilla/gestion_gastos` es el codigo de la app
