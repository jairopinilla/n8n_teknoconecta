# Guia del Repositorio

## Propósito

Esta guía resume cómo está organizado el repositorio, qué representa cada workflow exportado, qué integraciones aparecen realmente en los JSON versionados y qué reglas deben seguirse para mantener el proyecto consistente y entendible por personas y asistentes de código.

## Documentos fuente

- `AGENTS.md`: reglas canónicas para cualquier asistente de código.
- `README.md`: entrada general al repositorio.
- `documentacion/seguimiento.md`: bitácora de trabajo, estado actual y próximos pasos.
- `documentacion/tecnologias.md`: inventario tecnológico del proyecto.
- `documentacion/APIStaysDoc.md`: referencia obligatoria para cambios en Stays.net.

## Mapa del repositorio

| Ruta | Rol |
|------|-----|
| `workflows/` | Exportaciones versionadas de workflows de n8n |
| `documentacion/APIStaysDoc.md` | Referencia técnica de Stays.net |
| `documentacion/tecnologias.md` | Resumen de servicios, credenciales por nombre y dependencias |
| `documentacion/seguimiento.md` | Registro vivo de cambios recientes y rumbo inmediato |
| `sync_workflows.sh` | Descarga workflows desde n8n usando `secrets.json` local |
| `.vscode/mcp.json` | Configuración MCP local del workspace, ignorada por git |
| `secrets.json` | Secretos locales para automatizaciones, ignorado por git |

## Inventario de workflows

Estado observado en las exportaciones actuales del directorio `workflows/`.

| Archivo | Estado | Disparador | Propósito | Integraciones clave |
|---------|--------|------------|-----------|---------------------|
| `workflows/N8n_Update_Reservas.json` | Activo | `scheduleTrigger` | Sincronizar reservas, huéspedes y eventos desde Stays.net | Stays.net, PostgreSQL |
| `workflows/N8n_EnviarCorreosReserva.json` | Activo | `scheduleTrigger` | Enviar correos programados a huéspedes desde una bandeja | Gmail, PostgreSQL |
| `workflows/N8n_ProcesaWhatsapp.json` | Activo | `scheduleTrigger` | Enviar mensajes WhatsApp programados | HTTP/Twilio, PostgreSQL |
| `workflows/N8n_NotificacionWhats_Aseo.json` | Inactivo | `scheduleTrigger` | Variante o flujo legado de notificación de aseo | HTTP, PostgreSQL |
| `workflows/N8n_Procesa_Formularios.json` | Activo | `webhook` | Recibir formularios de Tally.so y persistirlos | Webhook, Tally.so |
| `workflows/N8n_SandiegoChatbot.json` | Activo | `webhook` + `respondToWebhook` | Atender consultas conversacionales para San Diego | OpenAI, Google Gemini, Tavily, PostgreSQL |
| `workflows/N8n_getAseosHtml.json` | Activo | `webhook` + `respondToWebhook` | Generar reporte HTML de aseos | Webhook, PostgreSQL |
| `workflows/N8n_getAseosHtml_v2.json` | Inactivo | `webhook` + `respondToWebhook` | Variante v2 del reporte de aseos | Webhook, PostgreSQL |
| `workflows/N8n_interpreta_email_conserjeria.json` | Activo | `scheduleTrigger` | Interpretar correos de conserjería con extracción estructurada | LLM, Google Sheets, PostgreSQL |
| `workflows/N8n_procesa_tarapaca_conserjeria.json` | Activo | `webhook` | Procesar mensajes de conserjería para Tarapacá | Webhook |
| `workflows/N8n_procesar_email_isaias.json` | Activo | `webhook` | Procesar correos entrantes del buzón Isaías | Webhook |
| `workflows/N8n_procesar_email_tekno.json` | Activo | `webhook` | Procesar correos entrantes del buzón TeknoConect | Webhook |

## Integraciones observadas en los JSON exportados

El inventario real de tipos de nodos usados actualmente en los workflows exportados incluye:

- PostgreSQL como dependencia más frecuente.
- Nodos `code`, `set`, `if`, `merge`, `splitOut`, `splitInBatches` y `aggregate` para orquestación y transformación.
- `httpRequest` para servicios externos como Stays.net y Twilio.
- `gmail` en el envío programado de correos.
- `googleSheets` en el flujo de interpretación de correos de conserjería.
- OpenAI y Google Gemini en `N8n_SandiegoChatbot.json`.
- Tavily como herramienta externa de búsqueda en `N8n_SandiegoChatbot.json`.

## Convenciones operativas

### Zona horaria

- La zona horaria oficial del proyecto es `America/Santiago`.
- Las fechas operativas deben salir de PostgreSQL con `now() AT TIME ZONE 'America/Santiago'`.
- Evitar cálculos duplicados de fecha en nodos `Code` si el valor ya puede resolverse en SQL.

### Stays.net

- Stays.net no tiene MCP dedicado en este proyecto.
- Toda interacción con Stays.net debe apoyarse en `documentacion/APIStaysDoc.md`.
- La autenticación se documenta por mecanismo o por nombre de credencial, nunca con valores secretos.

### Credenciales y secretos

- `.vscode/mcp.json` y `secrets.json` son archivos locales ignorados por git.
- Documentar nombres de credenciales de n8n, IDs funcionales y endpoints es válido; documentar tokens reales no lo es.
- Si un token aparece en un archivo versionado, debe retirarse antes de commit y registrarse el incidente en `documentacion/seguimiento.md`.

### Documentación

- `README.md` debe seguir siendo la puerta de entrada breve.
- `documentacion/guia-repositorio.md` concentra la explicación extensa.
- `documentacion/tecnologias.md` describe el stack y las integraciones.
- `documentacion/seguimiento.md` debe registrar siempre qué se hizo y qué sigue.
- Los componentes relacionados deben tener el mismo nivel de detalle documental.

## Mantenimiento de workflows exportados

### Uso del script de sincronización

`sync_workflows.sh`:

1. Lee `secrets.json` local.
2. Consulta la API REST de n8n.
3. Descarga workflows exportados hacia `workflows/`.
4. Sanitiza nombres para convertirlos en nombres de archivo válidos.

### Limitación conocida del script

El script actual consulta `active=true`, por lo que solo descarga workflows activos. Sin embargo, el repositorio también versiona workflows inactivos. Esto implica que los archivos inactivos existentes no quedan cubiertos por una sincronización estándar y deben considerarse durante mantenimiento o en una futura mejora del script.

## Validación recomendada para cambios

- Si se tocó un workflow JSON: validar con `jq '.' workflows/<archivo>.json`.
- Si se tocó `sync_workflows.sh`: validar con `bash -n sync_workflows.sh`.
- Si se tocó documentación: revisar que no se hayan agregado secretos y que `documentacion/seguimiento.md` quede actualizado.
- Antes de push: revisar `git status --short` y `git diff --stat`.

## Criterio para cambios futuros

Si el cambio altera flujo de negocio, integración, credencial usada, estado de un workflow o una convención de trabajo, no basta con editar el JSON o el script: también hay que reflejarlo en la documentación y dejar trazabilidad en `documentacion/seguimiento.md`.