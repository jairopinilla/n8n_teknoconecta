# n8n — Orquestador

## Datos del servidor

- URL: https://n8n.teknoconectapp.com
- MCP: https://n8n.teknoconectapp.com/mcp-server/http (JWT Bearer)
- Credencial webhooks: "Key Interna n8n Webhook"

## Workflows activos

| Workflow | Disparador | Proposito |
|----------|------------|-----------|
| N8n_Update_Reservas | Schedule | Sincronizar reservas Stays → PostgreSQL |
| N8n_EnviarCorreosReserva | Schedule | Enviar correos programados a huespedes |
| N8n_ProcesaWhatsapp | Schedule | Enviar WhatsApp programados |
| N8n_Procesa_Formularios | Webhook | Recibir formularios Tally.so |
| N8n_SandiegoChatbot | Webhook | Chatbot RAG con IA |
| N8n_getAseosHtml | Webhook | Reporte HTML de aseos |
| N8n_interpreta_email_conserjeria | Schedule | Interpretar correos conserjeria con LLM |
| N8n_procesa_tarapaca_conserjeria | Webhook | Procesar mensajes conserjeria Tarapaca |
| N8n_procesar_email_isaias | Webhook | Procesar correos buzon Isaias |
| N8n_procesar_email_tekno | Webhook | Procesar correos buzon TeknoConect |

## Sincronizacion

Script: `sync_workflows.sh` (lee `secrets.json`, descarga JSON a `workflows/`)
