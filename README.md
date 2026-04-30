# Plataforma de Automatizacion de Renta Corta

Este repositorio almacena exportaciones de workflows de n8n y la documentación operativa de una plataforma de automatización para renta corta. Su objetivo es centralizar el comportamiento de los flujos, las integraciones externas y las convenciones de operación para que cualquier persona o asistente de código pueda entender el sistema sin depender de contexto implícito.

## Leer primero

- `AGENTS.md`: instrucciones canónicas para asistentes de código.
- `documentacion/guia-repositorio.md`: guía detallada del repositorio y de su operación.
- `documentacion/seguimiento.md`: estado actual, cambios recientes y próximos pasos.
- `documentacion/tecnologias.md`: stack tecnológico e inventario de integraciones.
- `documentacion/APIStaysDoc.md`: referencia completa de la API de Stays.net.

## Qué contiene el repositorio

- `workflows/`: 12 exportaciones JSON de workflows de n8n.
- `documentacion/`: documentación funcional, técnica y operativa.
- `sync_workflows.sh`: script de sincronización con la instancia n8n.
- `.github/copilot-instructions.md`: puente de compatibilidad para GitHub Copilot.
- `CLAUDE.md` y `OPENCODE.md`: puentes de compatibilidad para otros asistentes.

## Resumen operativo

- Orquestador principal: n8n self-hosted.
- Persistencia: PostgreSQL en Neon, con pgvector para capacidades semánticas.
- Backend operacional: Directus.
- Reservas: Stays.net vía API HTTP documentada localmente.
- Mensajería: WhatsApp vía Twilio y correo vía Gmail.
- Formularios: Tally.so.
- IA: OpenAI, Google Gemini y herramientas externas de búsqueda en flujos puntuales.

## Inventario actual de workflows

Estado basado en los JSON exportados actualmente en `workflows/`.

| Workflow | Estado | Disparador | Propósito principal |
|----------|--------|------------|---------------------|
| `N8n_Update_Reservas` | Activo | Scheduler | Sincronizar reservas y huéspedes desde Stays.net hacia PostgreSQL |
| `N8n_EnviarCorreosReserva` | Activo | Scheduler | Enviar correos programados a huéspedes |
| `N8n_ProcesaWhatsapp` | Activo | Scheduler | Enviar mensajes WhatsApp programados |
| `N8n_NotificacionWhats_Aseo` | Inactivo | Scheduler | Flujo legado o alternativo para notificaciones de aseo por WhatsApp |
| `N8n_Procesa_Formularios` | Activo | Webhook | Recibir formularios de Tally.so |
| `N8n_SandiegoChatbot` | Activo | Webhook | Resolver consultas del departamento San Diego con RAG y LLM |
| `N8n_getAseosHtml` | Activo | Webhook | Generar reporte HTML de aseos |
| `N8n_getAseosHtml_v2` | Inactivo | Webhook | Variante v2 del reporte de aseos |
| `N8n_interpreta_email_conserjeria` | Activo | Scheduler | Interpretar correos de conserjería con LLM |
| `N8n_procesa_tarapaca_conserjeria` | Activo | Webhook | Procesar mensajes de conserjería para Tarapacá |
| `N8n_procesar_email_isaias` | Activo | Webhook | Procesar correos entrantes del buzón Isaías |
| `N8n_procesar_email_tekno` | Activo | Webhook | Procesar correos entrantes del buzón TeknoConect |

## Reglas del repositorio

- La fuente canónica de instrucciones es `AGENTS.md`.
- Para Stays.net siempre se debe consultar `documentacion/APIStaysDoc.md`.
- La zona horaria operativa es `America/Santiago` y las fechas deben salir de PostgreSQL cuando aplique.
- Los secretos viven solo en archivos locales ignorados por git como `.vscode/mcp.json` y `secrets.json`.
- Toda modificación sustantiva debe dejar actualizado `documentacion/seguimiento.md`.

## Sincronización de workflows

`sync_workflows.sh` lee `secrets.json`, consulta la API de n8n y escribe los JSON exportados en `workflows/`. La guía detallada, incluyendo limitaciones conocidas del script, está en `documentacion/guia-repositorio.md`.

## Estado y rumbo

El seguimiento vivo del repositorio, incluyendo qué se hizo y qué viene después, se mantiene en `documentacion/seguimiento.md`.