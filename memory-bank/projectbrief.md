# Project Brief — SandiegoApart / TeknoConecta

## Proposito

Automatizar y optimizar la operacion de **SandiegoApart** (renta corta en Santiago Centro, Chile) usando n8n, Directus, Supabase, PriceLabs, Stays.net, Clerk, e IA.

## Alcance

- 4 unidades en Tarapaca 1140, Santiago Centro: 901, 902, 709, 702
- Gestion de precios dinamicos via **PriceLabs**
- Reservas via **Stays.net** + canales (Airbnb, Booking)
- Automatizaciones con **n8n** (25 workflows)
- CMS con **Directus** (146 colecciones)
- Base de datos con **PostgreSQL** (sandiegoapart, 155 tablas)
- Auth con **Clerk** (gestion_gastos)
- Infraestructura en **VPS chitara** (5.252.52.190)
- Seguridad via **Cloudflare Tunnel + Access** (Google SSO)

## Servicios principales

| Servicio | URL |
|----------|-----|
| n8n | `https://n8n.teknoconectapp.com` |
| Directus | `https://directus.chitaraagenteia.com` |
| Supabase | `https://supabase.chitaraagenteia.com` |
| Coolify | `https://coolify.chitaraagenteia.com` |
| Saldito | `https://saldito.chitaraagenteia.com` |
| OpenCode Web | `https://opencode.chitaraagenteia.com` |

## Repositorios

| Repo | Proposito |
|------|-----------|
| `jairopinilla/n8n_teknoconecta` | Workspace principal, docs, workflows, MCPs |
| `jairopinilla/gestion_gastos` | App gestor de gastos (saldito) |
