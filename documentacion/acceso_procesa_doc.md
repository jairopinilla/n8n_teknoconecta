# Acceso Procesa_doc — VPS chitara

## VPS

| Campo | Valor |
|-------|-------|
| **IP** | `5.252.52.190` |
| **Usuario** | `root` |
| **Puerto SSH** | `22` |

La llave SSH `id_ed25519` ya está autorizada en el VPS desde este computador.  
Si necesitás generar una nueva:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "procesadoc@teknoconecta"
cat ~/.ssh/id_ed25519.pub  # → pedile a Jairo que la agregue
```

Probar conexión:
```bash
ssh -i ~/.ssh/id_ed25519 root@5.252.52.190 "echo OK"
```

---

## Proyecto Procesa_doc

### Repositorio
| Campo | Valor |
|-------|-------|
| **GitHub** | `jairopinilla/Procesa_doc` |
| **Rama** | `main` |
| **URL git** | `https://github.com/jairopinilla/Procesa_doc.git` |

### Ubicación en VPS
```
/opt/homelab/procesadoc-web/
├── docker-compose.yml
├── .env                  ← variables de entorno
├── apps/web/             ← Nuxt frontend/API
├── apps/web/Dockerfile
├── apps/web/app/server/utils/auth.ts
├── tools/                ← Python: procesador de documentos
├── mcp-servers/
└── ...
```

### Deploy — paso a paso

```bash
# 1. Conectarse al VPS
ssh root@5.252.52.190

# 2. Ir al proyecto
cd /opt/homelab/procesadoc-web

# 3. Pull de cambios
git pull

# 4. Rebuild (sin cache para asegurar que toma la imagen nueva)
docker compose build --no-cache

# 5. Redeploy
docker compose up -d

# 6. Verificar
docker ps | grep procesadoc
curl -s http://127.0.0.1:3200/login -o /dev/null -w '%{http_code}\n'
```

Comando rápido todo junto:
```bash
ssh root@5.252.52.190 "cd /opt/homelab/procesadoc-web && git pull && docker compose build --no-cache && docker compose up -d && docker ps | grep procesadoc"
```

### Estructura del compose
- **Contenedor**: `procesadoc-web`
- **Puerto interno**: `3000` → expuesto en `127.0.0.1:3200`
- **Red**: `coolify` (bridge 10.0.1.0/24)
- **DB**: PostgreSQL en `10.0.1.10:5432`, base `procesadoc`, user `procesadoc_app`
- **Volúmenes**: `storage_uploads`, `storage_processed`

### Variables de entorno (.env)
```
DATABASE_URL=postgresql://procesadoc_app:********@10.0.1.10:5432/procesadoc
SESSION_SECRET=********
OPENAI_API_KEY=sk-********
DEEPSEEK_API_KEY=sk-********
RAG_API_URL=http://rag-api:8000
RAG_API_TOKEN=********
NODE_ENV=production
```

### URL pública
```
https://procesadoc.chitaraagenteia.com
```

---

## Servicios relacionados

| Servicio | URL | Puerto interno |
|----------|-----|---------------|
| Procesa_doc web | `https://procesadoc.chitaraagenteia.com` | `127.0.0.1:3200` |
| RAG API | interno | `rag-api:8000` (misma red Docker) |
| PostgreSQL | `10.0.1.10:5432` | `postgres` container |
| Qdrant | interno | `http://localhost:6333` |

---

## Monitoreo

```bash
# Ver logs del contenedor
ssh root@5.252.52.190 "docker logs procesadoc-web --tail 50"

# Ver estado
ssh root@5.252.52.190 "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep procesadoc"

# Ver logs en tiempo real
ssh root@5.252.52.190 "docker logs -f procesadoc-web"
```

---

## Notas

- El deploy se hace por `docker compose build` (no por Coolify). Es standalone.
- La imagen se reconstruye desde el Dockerfile en `apps/web/Dockerfile`
- Si hay cambios en el `.env`, solo requiere `docker compose up -d` (sin rebuild)
- Si hay cambios en código (auth.ts, etc.), requiere rebuild + redeploy
- El archivo crítico de auth está en `apps/web/app/server/utils/auth.ts`
