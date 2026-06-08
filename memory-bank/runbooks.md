# Runbooks

> Procedimientos operativos paso a paso. No guardar secretos ni credenciales.

## Formato

### Nombre del runbook

**Objetivo:**
**Cuando usarlo:**
**Riesgo:** Bajo / Medio / Alto
**Prerequisitos:**
**Pasos:**
1.
2.
3.

**Validacion:**
**Rollback:**
**Notas:**

---

### Reiniciar Hermes Agent (Chitara)

**Objetivo:** Reiniciar el contenedor de Hermes cuando no responde o tiene errores.
**Cuando usarlo:** Chitara no responde en Telegram, errores de modelo, MCP no carga.
**Riesgo:** Bajo
**Prerequisitos:** Acceso SSH al VPS.
**Pasos:**
1. `ssh root@5.252.52.190 "cd /opt/homelab/hermes && docker compose restart"`
2. Esperar 15 segundos
3. `ssh root@5.252.52.190 "docker exec hermes tail -10 /opt/data/logs/gateway.log"`
4. Verificar "Connected to Telegram" y "MCP: registered X tool(s)"

**Validacion:** Enviar mensaje por Telegram y verificar respuesta.
**Rollback:** `docker compose down && docker compose up -d`
**Notas:** Requiere aprobacion del usuario para ejecutar.

---

### Sincronizar obsidian/ con Hermes

**Objetivo:** Aplicar cambios de personalidad/config de Chitara desde el repo.
**Cuando usarlo:** Despues de editar hermes-soul.md, hermes-config.md, o AGENTS.md en obsidian/.
**Riesgo:** Bajo
**Prerequisitos:** Cambios pusheados a GitHub.
**Pasos:**
1. `ssh root@5.252.52.190 "cd /opt/hermes-workspace && git pull origin main"`
2. `ssh root@5.252.52.190 "bash /opt/hermes-workspace/infra/sync-hermes-config.sh"`
3. Hermes recarga SOUL.md automaticamente en el siguiente mensaje.

**Validacion:** Verificar que SOUL.md fue copiado: `head -5 obsidian/.hermes/SOUL.md`
**Rollback:** Revertir el commit y re-sincronizar.
**Notas:** El cron job ejecuta esto automaticamente cada hora.

---

### Desencriptar credenciales del repo

**Objetivo:** Desencriptar archivos .enc con credenciales.
**Cuando usarlo:** Al iniciar una sesion de trabajo.
**Riesgo:** Bajo
**Prerequisitos:** Estar en la raiz del repo.
**Pasos:**
1. `bash decrypt.sh`

**Validacion:** Verificar que existen: `opencode.jsonc`, `documentacion/credenciales_infraestructura.txt`
**Rollback:** No aplica (los archivos estan en .gitignore).
**Notas:** La clave maestra esta en decrypt.sh. Los archivos desencriptados NUNCA se commitean.
