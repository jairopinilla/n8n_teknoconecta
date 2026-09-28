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

### 2026-09-28 - Criptominero perfctl en contenedor postgres (webhook aseos-v3 caido)

**Sistema afectado:** VPS chitara (5.252.52.190) — contenedor `postgres` (postgres:18), n8n, y servicios dependientes de la DB.
**Severidad:** Critica
**Descripcion:** `https://n8n.teknoconectapp.com/webhook/aseos-v3` devolvia 503. n8n registraba `Database connection timed out` en bucle. El contenedor `postgres` estaba comprometido con un kit tipo **perfctl**: minero de Monero, rootkit de ocultacion en `/dev/shm` (`libfsnldev.so`, `libpprocps.so`), clientes proxy de trafico (`ip_royal_paws`, `pawns-cli`, `traffmonetizer`), cliente Tor, y respawner con nombres impostores (`postgres`, `sleepvacuumlo`, `pg_createclusterzstdless`).
**Sintomas:** load average 15-17 (12 CPUs), procesos `postgres` falsos consumiendo 600-700% CPU, n8n con timeouts de DB cada 7s, postgres reiniciandose cada ~2 min.
**Diagnostico:** Puerto 5432 publicado en `0.0.0.0` en el compose (violaba REGLA #1). El malware persistia en el volumen `postgres_postgres_data` en `/var/lib/postgresql/.config/cron/perfcc`, `.local/bin/{ldd,top}` (troyanos), `.atmp/tmp/.applocal.xdiag/`, `.cache/go/imports` — todos creados el 2026-09-04 (fecha del compromiso).
**Causa raiz probable:** Puerto 5432 expuesto a internet sin bind local; acceso a la DB (rol postgres superuser / pg_hba con `trust` en localhost) permitio ejecucion de codigo en el contenedor. Llave SSH desconocida (sin comentario) en `/root/.ssh/authorized_keys`.
**Acciones ejecutadas:** (1) Matados mineros e impostores desde el host. (2) Bloqueado 5432 en iptables DOCKER-USER. (3) Retirada la 4ta llave SSH sin comentario. (4) Guardada evidencia forense en `/root/forensics_malware_20260928/`. (5) Eliminada persistencia del volumen (`.cache .config .atmp .local`). (6) Compose `/opt/homelab/postgres/docker-compose.yml` corregido: `0.0.0.0:5432` → `127.0.0.1:5432` (backup `.bak.20260928`). (7) Recreado contenedor postgres desde imagen limpia. (8) Reiniciado n8n. (9) **Rotacion de passwords** de roles DB: `chitara`, `n8n`, `wog`, `priv_esc`, `authenticator` (hex 48 chars, aplicadas a `.env` y composes de postgres/n8n/directus/shlink/supabase; postgrest recreado con URI nueva). (10) **DROP rol backdoor** `"postgres "` (superuser con espacio al final, oid 241205). (11) **Endurecimiento pg_hba.conf**: host TCP 127.0.0.1/::1 de `trust` → `scram-sha-256` (socket local sigue `trust` para docker exec); backup `pg_hba.conf.bak.20260928`. (12) **Imagen permanente** `postgres:18-chitara` (Dockerfile en `/opt/homelab/postgres/image/`) con pgvector + postgis 3 via apt, para no perder extensiones al recrear. (13) Extensiones actualizadas: `vector` 0.8.2→0.8.6 via `ALTER EXTENSION UPDATE`. (14) **Reparado Directus**: migraciones `20260204A`/`20260211A` estaban registradas pero sus tablas fueron borradas por el atacante → eliminadas del registro para re-ejecutar (backup en tabla `backup_migrations_deployment_20260928`). (15) **Backup script** reescrito para leer `POSTGRES_PASSWORD` del `.env`. (16) **Puertos expuestos restantes** (3030 topic-front, 4284 test-viral, 5555 flower, 6001-6002, 9000, 9443, 5434) bloqueados en INPUT + DOCKER-USER (v4) y DOCKER-USER (v6), persistidos en `/etc/iptables/rules.v{4,6}`. (17) Credenciales del repo actualizadas y re-encriptadas.
**Validacion:** 5432 cerrado desde internet. Procesos postgres limpios. Load 3.8. Webhook `aseos-v3` **HTTP 200**. n8n/directus/postgrest/gotrue/meta/supabase OK. `pg_dumpall` funcional (DUMP_OK). `.enc` desencripta con `decrypt.sh`.
**Estado:** Mitigado
**Pendientes:** (1) Verificar no respawn 24-48h. (2) Rotar passwords de roles de apps restantes: `procesadoc_app` (usada en rag/.env, procesadoc-web/.env, nocodb compose y MCP local), `topic_system_app`, `kiosko_app`, `kioskomunicipio`, `testviral_app`, `nocodb_app`, `n8n_pati`. (3) Rotar passwords de UI no rotadas: n8n admin, code-server (aun usan la antigua). (4) Considerar reconstruir volumen desde backup previo a 2026-09-04 y comparar. (5) Revisar backups S3 por si el malware se copio. (6) Quitar `trust` del socket local (requiere migrar MCPs locales a PGPASSWORD).
**Lecciones aprendidas:** (1) Un puerto publicado en `0.0.0.0` es la puerta de entrada mas comun; SIEMPRE `127.0.0.1`. (2) La vision del host (`docker top` + readlink /proc) es confiable; la vision dentro del contenedor comprometido NO (rootkit oculta procesos). (3) La persistencia de malware en contenedores suele estar en el VOLUMEN (home del usuario), no en la capa del contenedor. (4) Matar el proceso no basta: hay que borrar cron, dotfiles, .local/bin y .cache del home en el volumen, y recrear el contenedor. (5) iptables INPUT no bloquea puertos publicados por Docker; la cadena correcta es DOCKER-USER (y tambien ip6tables). (6) Test de puerto desde el propio VPS da falso positivo (hairpin); testear desde fuera. (7) Las extensiones de Postgres instaladas por apt dentro del contenedor se pierden al recrear → usar imagen propia con Dockerfile. (8) Los roles con nombre con espacio al final son indicio de backdoor SQL.

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
