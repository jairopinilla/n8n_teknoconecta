# Tech Context — TeknoConecta

## Stack tecnologico

| Capa | Tecnologia |
|------|-----------|
| Frontend apps | Angular 20 + Ionic 8 (saldito), HTML/CSS (aseos) |
| Backend API | Node.js ESM, @clerk/backend, @neondatabase/serverless |
| Base de datos operativa | PostgreSQL 18 (VPS Docker, DB `sandiegoapart`) |
| Base de datos gastos | Neon PostgreSQL (`old-lab-07457522`, schema `gestiongastos`) |
| Auth | Clerk (development, `charmed-lionfish-65`) |
| Automatizacion | n8n (25 workflows, VPS Docker) |
| CMS | Directus (VPS Docker, `directus.chitaraagenteia.com`) |
| Supabase | VPS Docker (Studio + GoTrue + Meta + PostgREST) |
| Proxy inverso | Nginx host + Cloudflare Tunnel |
| SSL | Let's Encrypt (certbot) + Cloudflare |
| DNS | Cloudflare (zone: `chitaraagenteia.com`) |
| Seguridad | Cloudflare Access (Google SSO, 16 apps), iptables |
| Deploy | Docker Compose (/opt/homelab/*), Coolify (saldito) |
| AI | OpenCode Web (DeepSeek V4 Pro via OpenRouter BYOK), Litellm, Open WebUI |
| Monitoreo | Uptime Kuma, Healthchecks, Dozzle |

## MCP Servers (27)

Todos definidos en `opencode.jsonc` (desencriptar con `bash decrypt.sh`).

**Chitara (SSH directo):** n8n-chitara, directus-chitara, supabase-chitara  
**Cloudflare:** cloudflare, cloudflare-dns  
**APIs externas:** clerk, neon, vercel, openai, jina, perplexity, google-maps, mercadopago, supabase, directus  
**Locales con API externa:** stays-docs, pricelabs-docs, coolify-mcp, scrapling  
**AWS (6):** awsKnowledge, awsApi, awsServerless, awsSnsSqs, awsCloudWatch, awsIam  
**Otros:** interactive-terminal

## Credenciales

Todas las claves, tokens y passwords en `documentacion/credenciales_infraestructura.txt` (encriptado como `.enc`, clave 5486).

Para desencriptar: `bash decrypt.sh`

## Conexiones

| Destino | Como |
|---------|------|
| VPS chitara | SSH root@5.252.52.190 |
| Neon (gestion_gastos) | Pooled URL |
| Stays.net API | Solo GET: reservas, listings |
| PriceLabs API | GET/POST listings y precios |
| Clerk API | REST v1 |

## Skills instaladas

- Cloudflare Skills (`.agents/skills/cloudflare/`) — 8 skills para Workers, Tunnel, Access, WAF
