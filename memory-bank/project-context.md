# Project Context

## Proposito del proyecto

SandiegoApart es un operador de renta corta en Santiago Centro, Chile. Este repositorio es la base de conocimiento, automatizacion y operacion del negocio. TeknoConecta es la plataforma de automatizacion que soporta la operacion.

## Sistemas relacionados

| Sistema | Funcion | URL/Acceso |
|---------|---------|-----------|
| Stays.net | PMS (reservas, calendario, huespedes) | https://jairop.stays.net |
| PriceLabs | Revenue management, pricing dinamico | API |
| n8n | Orquestador de workflows (25 workflows) | https://n8n.teknoconectapp.com |
| Directus | Backend/API admin | https://directus.chitaraagenteia.com |
| Supabase | DB PostgreSQL (sandiegoapart) | https://supabase.chitaraagenteia.com |
| Hermes Agent (Chitara) | Agente IA autonomo | https://hermes.chitaraagenteia.com |
| Saldito | Gestor de gastos | https://saldito.chitaraagenteia.com |

## Servicios involucrados

VPS chitara (5.252.52.190) con Docker Compose, Cloudflare Tunnel + Access, PostgreSQL 18, 23+ contenedores.

## Repositorios relacionados

| Repo | Contenido |
|------|-----------|
| `jairopinilla/n8n_teknoconecta` | Este repo — base de conocimiento y accion |
| `jairopinilla/gestion_gastos` | Saldito — gestor de gastos |

## Ambientes

| Ambiente | Detalle |
|----------|---------|
| Produccion | VPS chitara, todos los servicios, dominio chitaraagenteia.com |
| Desarrollo | Local (WSL2), OpenCode CLI/Web |

## Restricciones importantes

- API Stays.net limitada a 3 endpoints (solo lectura)
- Solo puertos 22/80/443 expuestos al exterior
- Todos los servicios detras de Cloudflare Tunnel + Google SSO
- Credenciales encriptadas con AES-256-CBC
- No guardar secretos en documentacion ni memory-bank

## Convenciones tecnicas

- Docker Compose para todos los servicios
- Bind a 127.0.0.1 para servicios internos
- Cloudflare Tunnel para exposicion externa
- PostgreSQL 18 como DB central
- n8n para automatizaciones
- Hermes Agent para asistente IA autonomo

## Contactos o stakeholders

| Rol | Nombre | Contacto |
|-----|--------|----------|
| Propietario/Operador | Jairo | contacto@teknoconecta.com |
| Aseo/Limpieza | Valentina | _(Telegram)_ |

## Notas relevantes

- 4 unidades en Tarapaca 1140: 901, 902, 709, 702
- Zona horaria: America/Santiago
- Idiomas: ES / EN / PT-BR
