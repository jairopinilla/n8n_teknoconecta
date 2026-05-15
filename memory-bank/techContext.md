# Tech Context — TeknoConecta

## Stack

| Tecnología | Propósito | URL / Acceso |
|-----------|----------|-------------|
| n8n | Orquestador de workflows | `https://n8n.teknoconectapp.com` |
| PostgreSQL (Neon) | Base de datos operativa + pgvector | Neon MCP |
| Directus | CMS / Backend operacional | `https://directus.teknoconectapp.com` |
| Stays.net | Gestión de reservas | `https://jairop.stays.net` |
| OpenAI | LLM + embeddings | API key |
| Google Gemini | LLM alternativo | API key |
| Twilio | WhatsApp Business | `+15559078472` |
| Gmail | Correo entrante/saliente | IMAP/SMTP |
| Tally.so | Formularios | `https://tally.so/r/vGeKkd` |
| MercadoPago | Procesamiento de pagos | API/MCP |
| Jina AI | Búsqueda, lectura web, embeddings | MCP |
| Perplexity | Búsqueda e investigación | MCP |
| Vercel | Hosting/deploy | MCP |
| Supabase | Backend adicional | MCP |
| AirROI | Análisis de mercado Airbnb | MCP |
| Clerk | Autenticación | MCP |
| Google Maps | Geocoding y rutas | MCP |

## Development Setup

```bash
# Clonar repo
git clone <repo-url>
cd n8n_teknoconecta

# Sincronizar workflows desde n8n
./sync_workflows.sh  # requiere secrets.json

# Validar JSON de workflows
jq '.' workflows/*.json

# Validar shell scripts
bash -n sync_workflows.sh
```

## MCP Servers (14)

Configurados en `.vscode/mcp.json` (local, ignorado por git):
airroi, clerk, neon, vercel, openai, jina, perplexity, google-maps, mercadopago, n8n-mcp, supabase, directus, stays-docs, scrapling.

## Dependencies

- **n8n**: self-hosted, requiere node 20+
- **PostgreSQL 16** en Neon con extensión `pgvector`
- **Directus**: auto-hosteado, conectado a PostgreSQL
- **Scrapling**: `uv tool install scrapling[fetchers,ai,shell]`
- **stays-docs MCP**: Python con `uv`, corre en `./mcp-servers/stays-docs/server.py`

## Constraints

- Zona horaria: `America/Santiago`. Fechas desde `now() AT TIME ZONE 'America/Santiago'` en SQL.
- Stays.net API limitada: solo endpoints de reservas y checkout funcionan; propiedades y settings no.
- Airbnb sin API: solo vía correo + parsing LLM.
- Scrapling browser tools requieren `libnspr4.so` y otras deps de Chromium (no instaladas en WSL).
- Las descripciones de anuncios están en el sitio público `sandiegoapart.com`, no en API.
- Sin sudo en WSL para instalar dependencias de sistema.

## Environment

- OS: Linux (WSL)
- Shell: bash
- Git: repositorio versionado
- Editor: VS Code con MCP servers configurados en `.vscode/mcp.json`
