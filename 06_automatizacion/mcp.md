# Servidores MCP

Configurados en `.vscode/mcp.json` (ignorado por git).

## Servidores

| Servidor | Tipo | URL / Comando |
|----------|------|---------------|
| airroi | HTTP | https://mcp.airroi.com |
| clerk | HTTP | https://mcp.clerk.com/mcp |
| neon | STDIO | npx @neondatabase/mcp-server-neon |
| vercel | HTTP | https://mcp.vercel.com |
| openai | STDIO | npx @mzxrai/mcp-openai |
| jina | HTTP | https://mcp.jina.ai/v1 |
| perplexity | STDIO | npx perplexity-mcp |
| google-maps | HTTP | https://mapstools.googleapis.com/mcp |
| mercadopago | HTTP | https://mcp.mercadopago.com/mcp |
| n8n-mcp | STDIO | supergateway → n8n MCP server |
| supabase | HTTP | https://mcp.supabase.com/mcp |
| directus | HTTP | https://directus.teknoconectapp.com/mcp |
| stays-docs | STDIO | uv run mcp-servers/stays-docs/server.py |
| scrapling | STDIO | /home/jairo/.local/bin/scrapling mcp |
| pricelabs-docs | STDIO | uv run mcp-servers/pricelabs-docs/server.py |

## Nota sobre Scrapling

Las tools HTTP (get, bulk_get) funcionan correctamente.
Las tools de browser (fetch, stealthy_fetch) requieren Chromium con LD_LIBRARY_PATH configurado.
Bug conocido: el proceso MCP no hereda LD_LIBRARY_PATH al lanzar Playwright.
Workaround: usar Python+Playwright directamente desde bash.
