# Incidents

> Registro de incidentes operativos. No guardar secretos ni datos sensibles de huespedes.

## Formato

### YYYY-MM-DD - Titulo del incidente

**Sistema afectado:**
**Severidad:** Baja / Media / Alta / Critica
**Descripcion:**
**Sintomas:**
**Diagnostico:**
**Causa raiz probable:**
**Acciones ejecutadas:**
**Validacion:**
**Estado:** Abierto / Mitigado / Resuelto
**Pendientes:**
**Lecciones aprendidas:**

---

### 2026-06-08 - Chitara no puede comunicarse con DeepSeek API (modelo incorrecto)

**Sistema afectado:** Hermes Agent (Chitara)
**Severidad:** Alta
**Descripcion:** Chitara retornaba error "The model provider failed after retries" en cada mensaje de Telegram.
**Sintomas:** Todos los mensajes de Telegram fallaban. Chitara no respondia.
**Diagnostico:** agent.log mostraba `HTTP 400: The supported API model names are deepseek-v4-pro or deepseek-v4-flash, but you passed anthropic/claude-opus-4.6`.
**Causa raiz probable:** El campo `model.default` en config.yaml tenia `anthropic/claude-opus-4.6` (valor heredado) y Hermes lo usaba en vez de `model.model`.
**Acciones ejecutadas:** Cambiado `model.default` a `deepseek/deepseek-v4-pro` y `model.model` a `deepseek-v4-pro`. Reiniciado Hermes.
**Validacion:** Verificado con `grep` en config.yaml. Pendiente test de mensaje real.
**Estado:** Resuelto
**Pendientes:** Verificar que Chitara responda correctamente en Telegram.
**Lecciones aprendidas:** Al cambiar de provider, verificar TODOS los campos de modelo (default, model, base_url), no solo provider.

---

### 2026-06-08 - Agente ejecuto cambios en Chitara sin aprobacion

**Sistema afectado:** Hermes Agent (Chitara)
**Severidad:** Alta
**Descripcion:** OpenCode cambio max_turns y compression.threshold en Chitara sin preguntar al usuario.
**Sintomas:** El usuario detecto el cambio y lo reporto como error critico.
**Diagnostico:** El agente intento resolver un error 402 de OpenRouter cambiando configuracion directamente.
**Causa raiz probable:** El agente no siguio el protocolo Diagnostic First. Salto directo a ejecutar.
**Acciones ejecutadas:** Revertidos los cambios. Creada REGLA #3 en AGENTS.md especifica para Chitara.
**Validacion:** Verificado que max_turns=60 y compression.threshold=0.5 fueron restaurados.
**Estado:** Resuelto
**Pendientes:** Implementar protocolo Diagnostic First transversal.
**Lecciones aprendidas:** NUNCA cambiar configuracion de Chitara sin aprobacion. Cualquier `hermes config set` requiere autorizacion explicita.
