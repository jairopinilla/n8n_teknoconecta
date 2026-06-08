# Changes Log

> Registro de cambios funcionales relevantes. No guardar secretos ni credenciales.

## Formato

### YYYY-MM-DD - Titulo del cambio

**Tipo:** Codigo / Configuracion / Infraestructura / Workflow / Base de datos / Documentacion / Otro
**Motivo:**
**Archivos o servicios afectados:**
**Cambio realizado:**
**Validacion:**
**Rollback:**
**Aprobado por:** Jairo
**Estado:** Implementado / Revertido / Pendiente

---

### 2026-06-08 - Instalacion de Hermes Agent (Chitara)

**Tipo:** Infraestructura
**Motivo:** Agente IA autonomo para operacion de SandiegoApart.
**Archivos o servicios afectados:** /opt/homelab/hermes/, Cloudflare Tunnel, obsidian/, mcp-servers/hermes-chitara/
**Cambio realizado:** Docker container hermes con DeepSeek V4 Pro, Telegram gateway, 45 tools MCP, dashboard con Google SSO.
**Validacion:** `docker ps`, `curl localhost:9119`, test Telegram, MCP tools loaded.
**Rollback:** `docker compose down` en /opt/homelab/hermes/
**Aprobado por:** Jairo
**Estado:** Implementado

---

### 2026-06-08 - Pipeline de correos Airbnb (BandejaRentaAirbnb + MensajeAirbnb)

**Tipo:** Workflow + Base de datos
**Motivo:** Capturar correos de Airbnb y procesarlos con AI para extraer mensajes de huespedes.
**Archivos o servicios afectados:** n8n workflows (N8n_ProcesaAirbnb, N8n_ProcesaAirbnb_AI), tablas BandejaRentaAirbnb y MensajeAirbnb en sandiegoapart.
**Cambio realizado:** Webhook para recibir correos raw, workflow AI cada 15min para clasificar y extraer datos.
**Validacion:** Webhook responde con auth, tabla creada, workflow importado.
**Rollback:** Desactivar workflows, DROP tablas.
**Aprobado por:** Jairo
**Estado:** Implementado

---

### 2026-06-08 - Cambio de OpenRouter a DeepSeek directo

**Tipo:** Configuracion
**Motivo:** Error 402 creditos insuficientes en OpenRouter.
**Archivos o servicios afectados:** /opt/homelab/hermes/docker-compose.yml, config.yaml de Hermes
**Cambio realizado:** Provider cambiado de openrouter a deepseek, base_url a api.deepseek.com/v1, modelo a deepseek-v4-pro.
**Validacion:** Config verificada con grep, gateway running.
**Rollback:** Cambiar provider a openrouter y restaurar OPENROUTER_API_KEY.
**Aprobado por:** Jairo
**Estado:** Implementado
