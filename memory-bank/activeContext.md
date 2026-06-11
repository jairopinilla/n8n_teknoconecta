# Active Context — TeknoConecta

> Ultima actualizacion: 2026-06-11
>
> 🔴 **Directus cloud y Supabase cloud YA NO SE USAN.** Todo en chitara (VPS 5.252.52.190).
> Para operar usar SIEMPRE los MCPs chitara (`n8n-chitara`, `directus-chitara`, `supabase-chitara`).
>
> 🔵 **Este repo (n8n_teknoconecta) es el hub central.** Coordina infra, MCPs, Hermes, Coolify y los otros repos.
> Los repos de proyectos (`gestion_gastos`, `kiosko_laflorida`) tienen su propio AGENTS.md y contexto.

## Estado del sistema

| Componente | Estado | Detalle |
|-----------|--------|---------|
| OpenCode Web | ✅ | `https://opencode.chitaraagenteia.com`, Google SSO |
| OpenCode Bridge | ✅ | `127.0.0.1:4097`, Bearer auth, para Telegram/n8n |
| **Hermes Agent** | ✅ | `https://hermes.chitaraagenteia.com`, OpenRouter+DeepSeek V4 Pro |
| **Coolify** | ✅ | 4 proyectos, 4 apps desplegadas con auto-deploy |
| n8n | ✅ | 25 workflows, `n8n.teknoconectapp.com` |
| 20 servicios web | ✅ | Todos con HTTPS via Cloudflare Tunnel |
| Seguridad | ✅ | Solo puertos 22/80/443 expuestos, resto iptables + 127.0.0.1 |

## Coolify — Apps desplegadas (auto-deploy via GitHub App)

| App | UUID | Dominio | Puerto host | Repo | Watch paths |
|-----|------|---------|-------------|------|-------------|
| kiosko-front | `tjsxn4ds3u6o8onl37fvxctn` | `https://kiosko.chitaraagenteia.com` | 127.0.0.1:4281 | jairopinilla/kiosko_laflorida | `apps/front/**` |
| kiosko-back | `nojhn2t0uvtfbhf39f7w4jky` | `https://api-kiosko.chitaraagenteia.com` | 127.0.0.1:4282 | jairopinilla/kiosko_laflorida | `apps/back/**` |
| saldito-frontend | `v5p0g5emcti9ej4a8ot7ct08` | `https://saldito.chitaraagenteia.com` | 127.0.0.1:4280 | jairopinilla/gestion_gastos | `frontend/*` |
| saldito-api | `p33rw7wj1i4duba954v3d727` | `https://api-saldito.chitaraagenteia.com` | 127.0.0.1:4283 | jairopinilla/gestion_gastos | `backend/*` |

**Deploy:** Push a `main` → Coolify redeploy automatico (GitHub App + watch_paths).
**APIs publicas:** HTTPS via Cloudflare Tunnel. Auth es responsabilidad del desarrollador de cada proyecto.
**Coolify API:** `http://localhost:8000/api/v1/` con token `1|GP1qcJjN3Hyi9HmEvyPDfXAoLp0LomhB1Bgul5DEaf517cae`
**Nota:** El MCP `coolify_list_apps` y `coolify_deploy_app` fallan. Usar API REST via SSH como fallback.

## Hermes Agent (Chitara en Telegram)

| Campo | Valor |
|-------|-------|
| Dashboard | `https://hermes.chitaraagenteia.com` |
| Modelo | DeepSeek V4 Pro via OpenRouter |
| Config | `/opt/hermes-workspace/obsidian/.hermes/config.yaml` |
| SOUL.md | `/opt/hermes-workspace/obsidian/.hermes/SOUL.md` |
| Workspace | `/opt/hermes-workspace` (repo clonado en VPS) |
| Sync | Cron cada 1 hora: `git pull` |

### Usuarios Telegram autorizados

| Usuario | Chat ID | Acceso |
|---------|---------|--------|
| Jairo | 7570257625 | Total, sin limites |
| Valentina Camus Toro | 8516014121 | Reservas, aseos, mensajes huespedes. Sin finanzas ni infra. Tono carinoso. |
| Jorge Jocelin | PENDIENTE | Proyecto EAS/IA La Florida. ZERO negocio arriendos. Grupo "Beers and AI". |

### Grupo Telegram: "Beers and AI"

| Campo | Valor |
|-------|-------|
| Miembros | Jairo + Jorge Jocelin + @ChitaraAIBot |
| Proposito | Proyecto Ecosistema IA + Envejecimiento Activo en La Florida |
| Contexto | `chitara-jorge/` (4 archivos: perfil, proyecto consolidado, chat, config grupo) |
| Tono Chitara | Jocosa, directa, humor inteligente. ZERO kawai/tierno |
| Research stack | Tavily + Jina + OpenAlex + o4-mini (OpenAI) |
| Estado | PENDIENTE: obtener Telegram ID de Jorge, configurar BotFather, agregar env vars VPS |

### MCP servers de Hermes (5)

| Servidor | Tools | Proposito |
|----------|-------|-----------|
| chitara | 16 | n8n, Directus, Supabase, Stays, PriceLabs, Docker |
| jina | 21 | Busqueda web, lectura URLs, clasificacion |
| tavily | 5 | Investigacion profunda |
| openalex | 3 | Papers academicos, autores, instituciones (250M+ papers) |
| pubmed | 10 | Papers biomedicos, full-text, MeSH, citas (36M+ papers) |

## MCPs de investigacion academica

| MCP | Donde | Token | Cobertura |
|-----|-------|-------|-----------|
| **OpenAlex** | Este repo + Chitara | Premium (`ofWS9byNgmkbR5u68cDB0N`) | 250M+ papers, todas las disciplinas |
| **PubMed** | Este repo + Chitara | NCBI API key (`223ce...dd09`) | 36M+ papers biomedicos, full-text via PMC/EuropePMC/Unpaywall |

**OpenAlex MCP:** Clonado de `drAbreu/alex-mcp` a `mcp-servers/openalex/`, con soporte API key agregado (2 lineas).
**PubMed MCP:** `@cyanheads/pubmed-mcp-server` via npx, sin codigo local.

## Infraestructura VPS chitara (5.252.52.190)

### Recursos (2026-06-11)
- **RAM:** 47GB total, ~10GB usado, 36GB libre
- **CPU:** 12 cores AMD EPYC
- **Disco:** 484GB total, 59GB usado, 425GB libre

### Capas de seguridad

| Capa | Mecanismo |
|------|-----------|
| Cloudflare Tunnel | `*.chitaraagenteia.com` → localhost |
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

## Comandos clave

```bash
# Desencriptar
bash decrypt.sh

# Re-encriptar opencode.jsonc
cat opencode.jsonc | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass pass:5486 -base64 -A > opencode.jsonc.enc

# Coolify: restart app via API
ssh root@5.252.52.190 "curl -s -X POST 'http://localhost:8000/api/v1/applications/<UUID>/restart' -H 'Authorization: Bearer 1|GP1qcJjN3Hyi9HmEvyPDfXAoLp0LomhB1Bgul5DEaf517cae' -H 'Content-Type: application/json'"

# Hermes: reiniciar
ssh root@5.252.52.190 "docker restart hermes"

# Hermes: logs
ssh root@5.252.52.190 "docker logs hermes --tail 50"

# Cloudflared: config
ssh root@5.252.52.190 "cat /etc/cloudflared/config.yml"
```

## Blockers

- Coolify MCP: `list_apps` y `deploy_app` fallan por UUID → usar API REST via SSH
- Coolify proxy Traefik no activo (conflicta con Nginx en 80/443) → todo via Cloudflare Tunnel
- OpenCode CLI `run`: inestable con modelo deepseek-v4-pro (funciona via web)
