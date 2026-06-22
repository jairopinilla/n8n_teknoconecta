# AGENTS.md — SandiegoApart

> Fuente canonica de instrucciones para cualquier asistente de IA que trabaje en este repositorio.
> Version: 2026-06-07
>
> **🔴 REGLA ABSOLUTA**: El agente NUNCA debe tomar decisiones de cambios sin preguntarle al usuario primero. Cualquier modificacion — por mas pequena que sea — requiere aprobacion explicita. Si el agente detecta un problema, debe reportarlo y esperar instrucciones.

---

## 🤖 REGLA #3 — CHITARA (HERMES AGENT): CERO CAMBIOS SIN APROBACION

> **Esta regla es especifica para Chitara. Refuerza la REGLA ABSOLUTA.**

Chitara (Hermes Agent) es el asistente autonomo mas poderoso del ecosistema. **Por su nivel de acceso, cualquier cambio en su configuracion requiere aprobacion explicita y documentada del usuario.**

### Que requiere aprobacion explicita (lista no exhaustiva):

| Tipo de cambio | Ejemplos |
|---------------|----------|
| Configuracion (`config.yaml`) | `max_turns`, `compression.threshold`, `gateway_timeout`, modelo, provider |
| Personalidad (`SOUL.md`) | Tono, identidad, limites, reglas por usuario |
| Instrucciones (`AGENTS.md` de obsidian/) | Reglas de vault, comportamiento |
| Docker compose | Puertos, variables de entorno, volumenes, recursos |
| MCP servers | Agregar, quitar, modificar tools |
| Gateway/Telegram | `TELEGRAM_ALLOWED_USERS`, `TELEGRAM_BOT_TOKEN` |
| Cualquier `hermes config set` | Sin excepcion |

### Flujo correcto:

1. **Detectar** el problema
2. **Reportar** al usuario con explicacion clara
3. **Proponer** solucion(es) con pros/contras
4. **Esperar** aprobacion explicita
5. **Ejecutar** solo lo aprobado
6. **Documentar** el cambio

### INCUMPLIR ESTA REGLA ES UN ERROR CRITICO.

---

## 🩺 PROTOCOLO DIAGNOSTIC FIRST — OBLIGATORIO PARA TODOS LOS AGENTES

> Todo agente que opere en este repositorio DEBE seguir este protocolo. Sin excepciones.

**Principio**: Diagnosticar antes de actuar. Entender antes de proponer. Proponer antes de ejecutar.

### Reglas del protocolo

1. **Read-only automatico**: Leer archivos, logs, configs, docs, buscar en el repo → permitido sin aprobacion.
2. **Cambios funcionales**: Codigo, config, infra, workflows, DB, servicios, Docker → requieren aprobacion explicita.
3. **Negocio de arriendo (alto riesgo)**: Reservas, huespedes, check-in/out, aseos, pricing, Stays, PriceLabs, mensajes a huespedes, codigos de acceso, pagos → aprobacion explicita reforzada.
4. **Dividir en pasos**: Toda solucion se divide en pasos medianos. Ejecutar solo los aprobados.
5. **Validar cada paso**: Despues de ejecutar, verificar que funciono.
6. **Reportar y esperar**: Reportar resultado, esperar autorizacion para continuar.
7. **Registrar en memory-bank/**: Diagnosticos relevantes, decisiones, cambios, incidentes.
8. **Nunca guardar secretos**: Tokens, passwords, .env, credenciales, datos sensibles de huespedes → prohibido en documentacion y memory-bank.
9. **Ante la duda, detenerse y preguntar**.

### Referencia completa: `agent-rules/diagnostic-first.md`

---

## 🏗️ INFRAESTRUCTURA — DONDE ESTA CADA COSA

> **Directus cloud y Supabase cloud YA NO SE USAN.** Todo migro a chitara (VPS 5.252.52.190).

| Servicio | Antes (cloud) | Ahora (chitara) |
|----------|---------------|-----------------|
| **n8n** | n8n.cloud (1 workflow) | VPS Docker, 25 workflows, `https://n8n.teknoconectapp.com` |
| **Directus** | Directus Cloud | VPS Docker, `https://directus.chitaraagenteia.com` |
| **Supabase** | Supabase Cloud | VPS Docker, `https://supabase.chitaraagenteia.com`, DB local `sandiegoapart` |
| **Gestor Gastos** | — | VPS Docker + Coolify, `https://saldito.chitaraagenteia.com` |

### MCPs cloud vs MCPs chitara

| Tipo | Conexion | Servicios | Estado |
|------|----------|-----------|--------|
| **MCPs cloud** (`n8n-mcp`, `directus`, `supabase`) | `*.teknoconectapp.com` | Solo 1 workflow en n8n cloud | ⚠️ Legacy, en desuso |
| **MCPs chitara** (`n8n-chitara`, `directus-chitara`, `supabase-chitara`) | SSH → VPS 5.252.52.190 | 25 workflows, 146 colecciones, 155 tablas | ✅ Produccion |

> **🔴 REGLA**: Para operar sobre el negocio real, usar SIEMPRE los MCPs chitara. Los MCPs cloud son legacy y apuntan a servicios ya migrados.

---

## 🛡️ REGLA #1 — SEGURIDAD DE EXPOSICION DE SERVICIOS (ARQUITECTURA ESQUELETICA)

> **Esta regla es estructural. Ningun agente puede violarla.**

### Principio fundamental

**NINGUN servicio en chitara (5.252.52.190) puede quedar expuesto a internet sin algun mecanismo de autenticacion.** No importa si es un dashboard, una API, un panel de logs, o una app interna. Si se accede desde una IP publica, DEBE tener al menos uno de estos:

1. **Cloudflare Access** (Google SSO) — para servicios web
2. **Token / API Key** (Bearer, header) — para APIs
3. **Password / Login** — como minimo
4. **127.0.0.1 bind** — si no necesita acceso externo directo

### Estado actual (2026-06-04)

Todos los puertos estan asegurados via **iptables** + **bind 127.0.0.1** + **Cloudflare Tunnel**:

| Capa | Mecanismo |
|------|-----------|
| **Cloudflare Tunnel** | `*.chitaraagenteia.com` → Google SSO → `localhost:PUERTO` |
| **iptables DOCKER-USER** | Bloquea acceso externo a puertos Docker |
| **iptables INPUT** | Bloquea acceso externo a puertos de host |
| **Docker compose** | Servicios bindeados a `127.0.0.1` |
| **Nginx** | Solo expone 80/443 con dominios configurados |

### Puertos permitidos (solo estos)

| Puerto | Servicio | Motivo |
|--------|----------|--------|
| 22 | SSH | Acceso administrativo |
| 80 | Nginx | Web (redirige a 443) |
| 443 | Nginx | Web + SSL |

### Si se instala un servicio nuevo

1. **SIEMPRE** bindear a `127.0.0.1` en docker-compose
2. Si necesita acceso externo → Cloudflare Tunnel (`/etc/cloudflared/config.yml`)
3. Si es API → agregar autenticacion (token/password)
4. **VERIFICAR** con `curl http://5.252.52.190:PUERTO` desde fuera del VPS que no responda

### Si se detecta un puerto expuesto sin auth

1. Marcarlo como `🔴 CRITICO`
2. Cerrarlo inmediatamente (iptables o recompose)
3. Reportarlo al usuario

---

## 🔐 REGLA #0 — ENCRIPTACION DE CREDENCIALES EN CADA PUSH (MAXIMA PRIORIDAD)

> **Esta seccion debe ser leida y ejecutada ANTES que cualquier otra accion del agente.**

### Principio fundamental

Todos los archivos que contienen tokens, API keys, passwords o secretos deben estar **encriptados con AES-256-CBC**. La **clave maestra** esta definida en `decrypt.sh`. Los archivos encriptados (`.enc`) se versionan en git. Los archivos desencriptados (sin `.enc`) **estan en `.gitignore` y NUNCA deben borrarse despues de desencriptar**.

### Al iniciar SIEMPRE

```bash
bash decrypt.sh
```

Esto desencripta todos los archivos `.enc`. Si los archivos ya existen (ya fueron desencriptados), los salta.

### Archivos encriptados (commiteados) vs desencriptados (gitignored)

| Archivo encriptado (en git) | Archivo desencriptado (gitignored) | Contenido |
|------------------------------|-------------------------------------|-----------|
| `opencode.jsonc.enc` | `opencode.jsonc` | Config MCPs: 27 servidores, API tokens, GitHub PAT |
| `documentacion/credenciales.enc` | `documentacion/credenciales` | Passwords de servicios: n8n, Directus, Coolify, DB |
| `documentacion/credenciales_infraestructura.txt.enc` | `documentacion/credenciales_infraestructura.txt` | **TODAS** las claves, tokens, API keys ordenadas por categoria |

### `opencode.jsonc` — Archivo CRITICO de MCPs

**Este es EL archivo de configuracion de MCPs.** Sin el, el agente no tiene acceso a ninguna herramienta externa.

Define **27 servidores MCP**: clerk, neon, vercel, openai, jina, perplexity, google-maps, mercadopago, n8n-mcp, supabase, directus, stays-docs, scrapling, pricelabs-docs, cloudflare, cloudflare-dns, interactive-terminal, awsKnowledge, awsApi, awsServerless, awsSnsSqs, awsCloudWatch, awsIam, n8n-chitara, directus-chitara, supabase-chitara, coolify-mcp.

**Ubicacion:** `opencode.jsonc` (raiz del workspace).  
**NO hay otro archivo de configuracion MCP.**

### En cada commit/push

1. Verificar que `opencode.jsonc` y `documentacion/credenciales_infraestructura.txt` NO esten en los archivos staged (estan en `.gitignore`)
2. Verificar que sus `.enc` SI esten actualizados
3. Si se modificaron, re-encriptar ANTES del commit:
   ```bash
   cat opencode.jsonc | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass pass:5486 -base64 -A > opencode.jsonc.enc
   ```
4. **NUNCA** commitear archivos con credenciales en texto plano

### Si el agente detecta un secreto en texto plano

1. Marcarlo como `🔴 CRITICO`
2. Verificar que este en `.gitignore`
3. Encriptarlo y guardar el `.enc`
4. Reportarlo al usuario

---

## 📝 REGLA #2 — ACTUALIZACION OBLIGATORIA DEL MEMORY BANK

> **DESPUES DE CADA ACCION**, el agente DEBE actualizar:
> - `memory-bank/activeContext.md` — estado REAL actual, cambios recientes, blockers
> - `memory-bank/progress.md` — marcar completados, agregar nuevos items
>
> **SIN EXCEPCIONES.** No acumular cambios para documentar despues.

---

## Proposito

Este repositorio es la base de conocimiento y accion para **SandiegoApart**, operador de renta corta en Santiago Centro, Chile, y **TeknoConecta**, plataforma de automatizacion.

---

## Orden de lectura obligatorio

1. `memory-bank/` — estado actual, progreso, contexto tecnico
2. `00_contexto_negocio/` — quien es SandiegoApart, unidades, ubicacion
3. `01_source_of_truth/` — fuentes de verdad (Stays, PriceLabs)
4. `02_operacion/` — reglas operativas, check-in/out, edificio
5. `03_marketing_y_ads/` — marca, tono, anuncios
6. `04_mensajeria/` — mensajes a huespedes, plantillas
7. `05_finanzas_y_pricing/` — KPIs, revenue management
8. `06_automatizacion/` — n8n, MCP, workflows
9. `08_playbooks/` — guias paso a paso
10. `documentacion/playbook_renta_corta.md` — **LECTURA OBLIGATORIA**: consolidado de renta corta
11. `documentacion/` — resto de documentacion
12. `documentacion/APIStaysDoc.md` — si el cambio toca Stays.net
13. `documentacion/pricelabs-academy/` — si el cambio toca PriceLabs

---

## Datos fijos vs datos que se buscan dinamicamente

**Datos fijos** (no cambiar sin aprobacion): contexto del negocio, reglas operativas, marca y tono, plantillas de mensajes, KPIs, playbooks.

**Datos dinamicos** (consultar la fuente indicada):

| Que buscas | Donde consultarlo |
|------------|------------------|
| Descripciones, titulos, amenities | Stays API o sandiegoapart.com |
| Precios, tarifas, restricciones | PriceLabs |
| Disponibilidad, calendario | Stays |
| Reservas activas, huespedes | Stays API |
| Fotos de unidades | Stays / repositorio de imagenes |

---

## Fuente de verdad (jerarquia)

1. **Stays**: calendario, tarifas, disponibilidad, contenido, IDs
2. **Manuales Tarapaca 1140**: reglas del edificio, mantenciones
3. **Exportaciones actuales**: analisis operativo/financiero
4. **PriceLabs**: pricing, revenue management
5. **Asesorias y ebooks**: buenas practicas
6. **Memoria del repo**: contexto auxiliar, no fuente final

---

## Contexto comercial

SandiegoApart: **Estudios modernos con terraza en Santiago Centro, pensados para trabajar y descansar.**

Ubicacion: Tarapaca 1140, Santiago Centro, Chile.  
Unidades: 901, 902, 709, 702 (4 estudios).

Atributos base: terraza privada, cama king, escritorio + silla, mesa alta para 2, TV 50", Wi-Fi rapido, A/C frio-calor, cocina equipada, bano privado.  
Espacios comunes del edificio (residentes, sujeto a disponibilidad y coordinacion con administracion): sala cowork, gimnasio al aire libre (rooftop), quinchos / sala gourmet, lavanderia de autoservicio.
**No**: estacionamiento propio (hay publico pago a una cuadra, Saba Paseo Bulnes) ni piscina.

### Reglas criticas de contenido
- No inventar amenities, politicas, ni claims exagerados
- No prometer estacionamiento propio ni piscina; los espacios comunes existen pero su acceso esta sujeto a disponibilidad y coordinacion con administracion
- No decir "a pasos" si no esta medido
- Mantener coherencia anuncio ↔ realidad
- Huespedes: tono claro, amable y directo
- Comercial: tono urbano, sobrio y confiable

### Idiomas
ES / EN / PT-BR. No traducir literal — localizar.

### Entregables esperados
Copy de anuncio, mensajes a huesped, checklist operativo, contenido Instagram, instrucciones n8n. Todo en ES/EN/PT-BR cuando aplique.

---

## 🔴 PROTOCOLO DE CAMBIOS DE PRECIOS EN PRICE LABS

**NINGUN cambio de precio puede ejecutarse sin seguir estos 10 pasos:**

1. **Obtener situacion actual**: ocupacion 7d/30d/60d, precios base/min/max, ocupacion mercado, fechas importantes
2. **Revisar know-how**: `playbook_renta_corta.md`, `pricing_rules.md`, `revenue_management.md`, lecciones aprendidas
3. **Verificar fechas**: calendario eventos Santiago Centro, feriados, ferias, conciertos
4. **Buscar info complementaria**: Jina search para eventos, demanda, ocupacion hotelera
5. **Elaborar propuesta**: periodo especifico (7d urgente, luego 30d), precios propuestos con justificacion
6. **Presentar con explicacion**: por que, datos, riesgos de hacer/no hacer, alternativas
7. **Esperar confirmacion**: NUNCA aplicar sin aprobacion explicita del usuario
8. **Aplicar con confirmacion**: `pricelabs_update_listings` con `confirmed=True`
9. **Verificar cambios**: consultar API para confirmar, revisar periodos no autorizados
10. **Documentar**: `memory-bank/activeContext.md` y `memory-bank/progress.md`

**INCUMPLIR ESTE PROTOCOLO ES UN ERROR CRITICO.**

### Verificacion en capas (pricing)
1. **Pre-ejecucion**: `confirmed=True`, 4 unidades, valores coherentes
2. **Post-ejecucion**: `pricelabs_get_listing` confirmar cada unidad
3. **Post-push**: verificar `last_date_pushed` y `push_enabled`

---

## 🛡️ Harness Engineering — prevencion de errores

### Hooks de verificacion obligatorios

| Operacion | Verificacion |
|-----------|-------------|
| `pricelabs_update_listings` | `pricelabs_get_listing` |
| `pricelabs_push_prices` | `pricelabs_get_listing` (status + fecha) |
| Cambio de precio | Actualizar activeContext |
| Diagnostico unidades | Cross-check PriceLabs + Stays |

**Regla:** Si una operacion de escritura no se verifica, el cambio se considera NO APLICADO.

### Reglas anti-error (derivadas de errores reales)

| # | Error | Prevencion |
|---|-------|-----------|
| 1 | `base_price` vs `base` | Verificar nombres de campo contra docs de API |
| 2 | Push a Stays sin feedback | Mostrar status y `last_date_pushed` |
| 3 | Asumir descuentos activos | Leer datos reales de la API, nunca asumir |
| 4 | Diagnostico solo PriceLabs | Cross-check obligatorio con Stays reservas |
| 5 | Cambios sin ocupacion mercado | Comparar ocupacion propia vs mercado |
| 6 | Memory-bank desactualizado | Actualizar INMEDIATAMENTE |
| 7 | Archivos huerfanos en AGENTS.md | Actualizar referencias al crear/renombrar |
| 8 | Cambios en chitara sin documentar | Registrar en `documentacion/chitara.md` y memory-bank |
| 9 | MCPs chitara no cargan (.venv) | `rm -rf .venv && uv venv && uv pip install mcp` |

### Limpieza periodica (fin de sesion)
- [ ] `activeContext.md` refleja estado REAL?
- [ ] `progress.md` tiene ultimos cambios?
- [ ] Archivos nuevos referenciados en AGENTS.md?
- [ ] `playbook_renta_corta.md` es la fuente unica de renta corta (sin archivos legacy paralelos)?

---

## 🔧 Conexion al VPS chitara (5.252.52.190)

**Setup inicial (una vez por sesion):**
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "opencode@teknoconecta"
cat ~/.ssh/id_ed25519.pub
# Pedir al usuario que agregue la llave al VPS
ssh -o StrictHostKeyChecking=accept-new root@5.252.52.190 "echo OK"
```

**Operaciones:**
```bash
ssh root@5.252.52.190 "COMANDO"
docker ps --format '{{.Names}} → {{.Networks}}'
docker network inspect NOMBRE_RED
```

Documentacion completa: `documentacion/chitara.md`

---

## 🔌 Stays.net API

**Endpoints funcionales (solo 3):**
- ✅ `GET /external/v1/booking/reservations`
- ✅ `GET /external/v1/booking/reservations/{id}`
- ✅ `POST /external/v1/booking/search-listings` (requiere `rooms` como array)

**NO funcionales (404):** `checkout/initiate`, `promocodes`, `sell-price-rules`, `properties`, `house-rules`.  
**Consecuencia:** solo lectura de reservas y busqueda de listings. Contenido de anuncios desde sandiegoapart.com.

**Mapeo IDs:** `_idlisting` (MongoDB ObjectId) ↔ `AlojamientoStayslistingIdLargo` (Directus)

---

## 🐳 MCPs chitara — VPS via SSH

**Arquitectura:** `OpenCode → MCP server (local) → SSH → VPS → contenedor Docker`

| MCP | DB | Contenedor | Funcion |
|-----|-----|-----------|---------|
| `n8n-chitara` | PostgreSQL `n8n` | `postgres` + `n8n` | CRUD workflows, ejecuciones |
| `directus-chitara` | Interna | `directus` | CRUD colecciones, items, files |
| `supabase-chitara` | PostgreSQL `sandiegoapart` | `postgres` + `supabase-*` | SQL, tablas, RLS |

**Dependencia critica:**
```bash
uv venv && uv pip install mcp
```

**Verificar al iniciar sesion:**
```
n8n_chitara_list_workflows → 25 workflows
directus_chitara_list_collections → ~146 colecciones
supabase_chitara_list_tables → ~155 tablas
```

---

## 📋 MCPs locales con APIs externas

Se usan servidores MCP propios que envuelven APIs externas (stays-docs, pricelabs-docs, cloudflare). Ventajas: documentacion embebida, validacion de entrada, escritura con confirmacion.

Estructura: `./mcp-servers/{nombre}/server.py` (Python + `mcp` SDK)

---

## 🩺 SALUD PROACTIVA DEL SISTEMA

> **Al iniciar CADA sesion, el agente DEBE verificar la salud de estos servicios criticos sin que el usuario lo pida.**

### Checklist de salud (ejecutar al inicio)

```bash
# 1. n8n — el mas fragil (depende de DB + encryption key + volumen)
curl -s -o /dev/null -w '%{http_code}' https://n8n.teknoconectapp.com/
# Esperado: 200. Si no: revisar docker logs n8n, encryption key, DB connection

# 2. Saldito
curl -s https://saldito.chitaraagenteia.com/health
# Esperado: {"status":"ok","database":"ok"}

# 3. OpenCode Web
curl -s -o /dev/null -w '%{http_code}' https://opencode.chitaraagenteia.com/
# Esperado: 302 (redirect Google SSO) o 200

# 4. SSH a chitara
ssh -o ConnectTimeout=5 root@5.252.52.190 "echo OK"
```

### n8n — puntos criticos que requieren verificacion proactiva

| Que verificar | Comando | Por que |
|--------------|---------|---------|
| **Encryption key** | `grep ENCRYPTION /opt/homelab/n8n/.env` debe coincidir con `docker run --rm -v n8n_n8n_data:/data alpine cat /data/config` | Si no coinciden, n8n no arranca |
| **DB connection** | `docker exec postgres psql -U n8n -d n8n -c 'SELECT 1'` | Sin DB, n8n no funciona |
| **Contenedor corriendo** | `docker ps --format '{{.Names}} {{.Status}}' | grep n8n` | Debe mostrar "Up" no "Restarting" |
| **Credenciales** | `docker exec postgres psql -U n8n -d n8n -c 'SELECT count(*) FROM credentials_entity'` | Debe ser 24 |
| **Workflows activos** | `n8n_chitara_list_workflows` → contar los `active: true` | Monitorear fallos de activacion |

### Errores conocidos de n8n y sus soluciones

| Error | Causa | Solucion |
|-------|-------|----------|
| `Mismatching encryption keys` | .env ≠ volume config | `docker compose down -v && docker compose up -d` (recrea volumen con key del .env) |
| `password authentication failed for user "n8n"` | Rol no existe en DB | `docker exec postgres psql -U postgres -c "CREATE ROLE n8n WITH LOGIN PASSWORD 'ElefantesEbrios1Renca'"` |
| `Unrecognized node type: @tavily/...` | Falta paquete comunitario | `docker exec n8n npm install @tavily/n8n-nodes-tavily` |
| Container en loop "Restarting (1)" | Error de config | `docker logs n8n --tail 20` para diagnosticar |

### n8n webhooks — acceso publico seguro

Los webhooks de n8n son accesibles publicamente desde internet (ej: `https://n8n.chitaraagenteia.com/webhook-test/aseos-v3`). Esto es seguro porque son endpoints especificos que solo ejecutan el workflow asociado, sin exponer el panel de administracion (que requiere user/password).

### Workflows versionados

Todos los workflows exportados como JSON estan en `n8n/workflows/`. Son 16 workflows (25 en total en el servidor, los activos y relevantes estan versionados aca).

---

## ⚠️ Problemas conocidos

| Problema | Impacto | Estado |
|----------|---------|--------|
| API Stays.net limitada (3 endpoints) | No se modifica contenido | Solo lectura |
| Directus app.js parcheado | Se pierde al actualizar imagen | Re-aplicar patch |
| Coolify frontend: nixpacks falla Angular 20 | Frontend via docker-compose | Workaround estable |
| OpenCode CLI `run` inestable con DeepSeek | Solo funciona con `--model` explicito | Web funciona OK |
| `exportadata/` contiene PII + tokens | Riesgo seguridad | Pendiente limpiar git history |
| `09_archive/` para contenido deprecated | No confundir con docs activos | Estable |
