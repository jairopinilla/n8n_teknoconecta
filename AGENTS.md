# AGENTS.md

Este archivo es la fuente canónica de instrucciones para cualquier asistente de código que trabaje en este repositorio. El contenido debe mantenerse neutral respecto de un proveedor concreto; los archivos `CLAUDE.md`, `OPENCODE.md` y `.github/copilot-instructions.md` existen solo como puntos de entrada compatibles y no deben divergir de este documento.

## Orden de lectura obligatorio

Antes de proponer o aplicar cambios, leer en este orden:

1. `README.md`
2. `documentacion/guia-repositorio.md`
3. `documentacion/seguimiento.md`
4. `documentacion/tecnologias.md`
5. `documentacion/APIStaysDoc.md` si el cambio toca Stays.net

## Contexto del proyecto

El repositorio contiene exportaciones de workflows de n8n y documentación operativa para una plataforma de automatización de renta corta. La plataforma opera múltiples departamentos con mínima intervención humana, principalmente mediante n8n, PostgreSQL, Directus, integraciones externas y LLMs.

## Estructura relevante del repositorio

- `workflows/`: exportaciones JSON de workflows de n8n.
- `documentacion/APIStaysDoc.md`: referencia manual de la API de Stays.net.
- `documentacion/tecnologias.md`: inventario tecnológico y credenciales por nombre o ubicación, nunca por secreto.
- `documentacion/guia-repositorio.md`: guía operativa detallada del repositorio.
- `documentacion/seguimiento.md`: bitácora viva de estado, cambios recientes y próximos pasos.
- `sync_workflows.sh`: script para descargar workflows desde n8n usando `secrets.json` local.
- `.vscode/mcp.json`: configuración local de MCP del workspace. Es local, está ignorada por git y debe preferirse sobre configuraciones globales del usuario.
- `secrets.json`: credenciales locales para automatizaciones del repo. Está ignorado por git.

## Reglas operativas no negociables

- La zona horaria operativa es `America/Santiago`.
- Las fechas operativas deben obtenerse desde PostgreSQL con `now() AT TIME ZONE 'America/Santiago'`; no se deben recalcular en nodos JavaScript cuando el dato puede venir de SQL.
- Stays.net no tiene servidor MCP en este proyecto. Si el cambio toca reservas, pagos, checkout, promo codes o disponibilidad, se debe consultar `documentacion/APIStaysDoc.md` antes de proponer endpoints o payloads.
- Airbnb no tiene API pública dentro de esta arquitectura; los flujos relacionados se apoyan en correo y parsing con LLM.
- Los workflows deben seguir referenciando credenciales por nombre o por tipo de credencial de n8n. Nunca se deben agregar tokens, API keys o secretos en archivos versionados.
- Nunca usar ni documentar el `mcp.json` global del usuario para este repo. La referencia válida es el `.vscode/mcp.json` local del workspace.
- Toda documentación nueva o modificada debe mantener el mismo nivel de detalle entre recursos y componentes relacionados.
- Toda modificación sustantiva del repo debe actualizar `documentacion/seguimiento.md` con dos cosas: qué se hizo y cuál es el siguiente paso recomendado.

## Protocolo para cambios en workflows

1. Identificar el workflow exacto y revisar su exportación JSON en `workflows/`.
2. Verificar el disparador real del workflow y las integraciones que usa.
3. Si el cambio impacta Stays.net, contrastar el endpoint y la autenticación contra `documentacion/APIStaysDoc.md`.
4. Mantener nombres de credenciales, IDs funcionales y convenciones del proyecto; nunca introducir secretos en texto plano.
5. Si cambian responsabilidades, integraciones, estados o convenciones, actualizar `README.md`, `documentacion/guia-repositorio.md`, `documentacion/tecnologias.md` y `documentacion/seguimiento.md` según corresponda.

## Protocolo para documentación

- `README.md`: puerta de entrada del repositorio.
- `documentacion/guia-repositorio.md`: operación, estructura, flujos y reglas de mantenimiento.
- `documentacion/tecnologias.md`: stack, integraciones y fuentes de credenciales sin exponer secretos.
- `documentacion/seguimiento.md`: historial vivo, estado actual y rumbo inmediato.
- Si una nueva documentación cambia la forma de trabajar con el repo, enlazarla desde `README.md` y desde esta instrucción si aplica.

## Validación mínima esperada

- Para JSON de workflows: validar sintaxis con `jq '.' workflows/<archivo>.json` o equivalente.
- Para shell scripts: validar con `bash -n sync_workflows.sh` si el script fue tocado.
- Para documentación sensible: buscar tokens o secretos residuales antes de commit.
- Antes de commit: revisar `git diff --stat` y `git status --short`.

## Compatibilidad multi-agente

- `AGENTS.md` es la referencia principal.
- `CLAUDE.md`, `OPENCODE.md` y `.github/copilot-instructions.md` deben ser archivos delgados que redirigen a este documento y no deben introducir reglas contradictorias.
- Si se agrega soporte para otro asistente, el patrón esperado es crear solo un archivo de entrada mínimo que apunte a `AGENTS.md` y a la documentación operativa existente.