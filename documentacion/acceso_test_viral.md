# Acceso Test Viral — VPS chitara

## VPS

| Campo | Valor |
|-------|-------|
| **IP** | `5.252.52.190` |
| **Usuario** | `root` |
| **Puerto SSH** | `22` |

La llave SSH `id_ed25519` ya está autorizada.

---

## Proyecto Test Viral

### Repositorio
| Campo | Valor |
|-------|-------|
| **GitHub** | `jairopinilla/test_viral` |
| **Rama** | `main` |
| **URL git** | `https://github.com/jairopinilla/test_viral.git` |

### Ubicación en VPS
```
/data/test-viral/
├── tmp_repo/              ← clon del repo (para referencia, no se usa en deploy)
├── images/                ← imágenes generadas (persistente)

/data/coolify/applications/f8kxqoahu0hwlwimhktgjp7t/
├── docker-compose.yaml    ← compose generado por Coolify
├── .env                   ← variables de entorno (Coolify las sync desde su UI)
└── README.md
```

### URL pública
```
https://test.chitaraagenteia.com
```

---

## Deploy — vía Coolify

Test Viral se despliega **automáticamente por Coolify**. Cada push a `main` del repo `jairopinilla/test_viral` dispara un build y deploy.

### Coolify Dashboard

| Campo | Valor |
|-------|-------|
| **URL** | `https://coolify.chitaraagenteia.com` |
| **Usuario** | `admin` |
| **Password** | `CoolifyAdmin2026!` |

### Proyecto en Coolify
- **Nombre**: `test-viral`
- **App**: `test-viral-app`
- **UUID**: `f8kxqoahu0hwlwimhktgjp7t`
- **Watch paths**: `apps/web/**` o `apps/front/**`
- **Source**: GitHub App (auto-deploy)

### Si Coolify no auto-deploya

1. Entrar a `https://coolify.chitaraagenteia.com`
2. Ir al proyecto `test-viral` → `test-viral-app`
3. Botón **Deploy** o **Redeploy**

### Deploy manual (sin Coolify)

```bash
ssh root@5.252.52.190

# Ir al compose de Coolify
cd /data/coolify/applications/f8kxqoahu0hwlwimhktgjp7t

# Pull manual del repo en tmp_repo
cd /data/test-viral/tmp_repo && git pull

# Forzar rebuild desde Coolify (recomendado usar la UI)
docker compose -f /data/coolify/applications/f8kxqoahu0hwlwimhktgjp7t/docker-compose.yaml down
docker compose -f /data/coolify/applications/f8kxqoahu0hwlwimhktgjp7t/docker-compose.yaml up -d
```

---

## Estructura del contenedor

| Campo | Valor |
|-------|-------|
| **Contenedor** | `f8kxqoahu0hwlwimhktgjp7t-210522962219` (nombre varía por deploy) |
| **Puerto interno** | `3000` → expuesto en `0.0.0.0:4284` |
| **Red** | `coolify` (bridge 10.0.1.0/24) |
| **DB** | PostgreSQL en `postgres:5432`, base `test_viral`, user `testviral_app` |
| **Imagen** | `f8kxqoahu0hwlwimhktgjp7t:{commit_sha}` (built por Coolify) |

### Volumen persistente
```
/data/test-viral/images  →  /app/public/assets/visual/tests
```

Las imágenes generadas por los tests se guardan en este volumen y sobreviven redeploys.

**Watchdog**: si Coolify borra el volumen en un redeploy, un script lo restaura en ≤2 min:
- Script: `/opt/scripts/testviral-volume-fix.sh`
- Cron: `*/2 * * * *`

---

## Variables de entorno (.env — gestionado desde Coolify UI)

| Variable | Descripción |
|----------|-------------|
| `SESSION_SECRET` | Secret para sesiones/cookies |
| `DATABASE_URL` | `postgresql://testviral_app:***@postgres:5432/test_viral` |
| `OPENAI_API_KEY` | OpenAI para IA |
| `TAVILY_API_KEY` | Tavily search |
| `JINA_API_KEY` | Jina AI |
| `S3_REGION` | `us-east-1` |
| `S3_ACCESS_KEY` | AWS Access Key |
| `S3_SECRET_KEY` | AWS Secret Key |
| `S3_BUCKET` | `testviral-app` |
| `PORT` | `3000` |
| `HOST` | `0.0.0.0` |

---

## Servicios relacionados

| Servicio | URL | Puerto interno |
|----------|-----|---------------|
| Test Viral web | `https://test.chitaraagenteia.com` | `127.0.0.1:4284` |
| PostgreSQL | `postgres:5432` | DB `test_viral` |
| S3 bucket | `testviral-app` (us-east-1) | — |

---

## Monitoreo

```bash
# Ver logs del contenedor
ssh root@5.252.52.190 "docker logs f8kxqoahu0hwlwimhktgjp7t-210522962219 --tail 50"

# Ver estado (buscar por parte del nombre)
ssh root@5.252.52.190 "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep f8kxqoahu0hwlwimhktgjp7t"

# Ver logs en tiempo real
ssh root@5.252.52.190 "docker logs -f f8kxqoahu0hwlwimhktgjp7t-210522962219"

# Verificar volumen de imágenes
ssh root@5.252.52.190 "ls -la /data/test-viral/images/"
```

---

## Repos clonados en VPS

| Path | Repo | Nota |
|------|------|------|
| `/data/test-viral/tmp_repo/` | `jairopinilla/test_viral` | Clon manual (para leer código) |
| `/data/coolify/applications/f8kxqoahu0hwlwimhktgjp7t/` | — | Archivos generados por Coolify |

El deploy real lo maneja Coolify desde el repo en GitHub. El clon en `tmp_repo` es solo para consulta. Si hacés cambios en `tmp_repo`, NO afectan el deploy a menos que los pushees a GitHub primero.

---

## Notas

- El deploy es **automático vía Coolify + GitHub**. No requiere SSH.
- Si el deploy automático falla, usar el Dashboard de Coolify.
- El volumen de imágenes tiene un watchdog (cron cada 2 min). No tocar.
- El contenedor se crea con nombre variable (hash + timestamp). Buscar por UUID `f8kxqoahu0hwlwimhktgjp7t`.
- Los variables de entorno se gestionan desde la UI de Coolify (no desde el .env del repo).
