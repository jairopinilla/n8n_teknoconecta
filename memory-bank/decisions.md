# Decisions

> Registro de decisiones arquitectonicas y operativas. Formato ADR simplificado.
> No guardar secretos, tokens ni credenciales aqui.

## Formato

### YYYY-MM-DD - Titulo de la decision

**Contexto:**
_(Que problema o necesidad motivo la decision)_

**Decision:**
_(Que se decidio hacer)_

**Alternativas consideradas:**
_(Otras opciones evaluadas)_

**Motivo:**
_(Por que se eligio esta opcion)_

**Impacto:**
_(Que sistemas, procesos o personas se ven afectados)_

**Riesgos:**
_(Que podria salir mal)_

**Rollback o reversibilidad:**
_(Como revertir si falla)_

**Estado:** Propuesta / Aprobada / Implementada / Revertida

---

### 2026-06-08 - Instalar Hermes Agent (Chitara) en VPS chitara

**Contexto:** Se necesitaba un agente IA autonomo con capacidad de aprendizaje para asistir en la operacion de SandiegoApart.

**Decision:** Instalar Hermes Agent (NousResearch) como contenedor Docker en el VPS chitara, con DeepSeek V4 Pro como modelo, gateway Telegram, y vault en obsidian/.

**Alternativas consideradas:** OpenClaw, agente custom con LangChain, usar solo OpenCode.

**Motivo:** Hermes tiene learning loop, skills automaticas, soporte MCP nativo, y corre en Docker.

**Impacto:** Nuevo contenedor en VPS, nuevo subdominio, nuevo bot de Telegram, 45 tools MCP.

**Riesgos:** Consumo de recursos, costos de API, cambios no autorizados (mitigado con REGLA #3).

**Rollback o reversibilidad:** `docker compose down` en /opt/homelab/hermes/

**Estado:** Implementada

---

### 2026-06-08 - Cambiar de OpenRouter a DeepSeek directo

**Contexto:** OpenRouter retornaba error 402 (creditos insuficientes) con DeepSeek V4 Pro.

**Decision:** Conectar Chitara directamente a la API de DeepSeek (api.deepseek.com/v1) sin intermediario.

**Alternativas consideradas:** Agregar creditos a OpenRouter, cambiar a modelo mas barato.

**Motivo:** El usuario ya tiene API key de DeepSeek. Elimina dependencia y costo de intermediario.

**Impacto:** Chitara usa modelo deepseek-v4-pro directo.

**Riesgos:** Si DeepSeek tiene downtime, Chitara no funciona (sin fallback).

**Rollback o reversibilidad:** Cambiar provider a openrouter en config.yaml.

**Estado:** Implementada
