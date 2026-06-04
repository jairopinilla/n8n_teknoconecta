# AGENTS.md — SandiegoApart

> Fuente canonica de instrucciones para cualquier asistente de IA que trabaje en este repositorio.
> Version: 2026-06-03

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

## 🔐 REGLA #2 — ENCRIPTACION DE CREDENCIALES EN CADA PUSH

## 🔐 REGLA #0 — PROTOCOLO DE ENCRIPTACION / DESENCRIPTACION (MAXIMA PRIORIDAD)

> **Esta seccion debe ser leida y ejecutada ANTES que cualquier otra accion del agente.**

### Principio fundamental

Todos los archivos que contienen tokens, API keys, passwords o secretos deben estar **encriptados con AES-256-CBC** usando la **clave maestra `5486`**. Los archivos encriptados (`.enc`) se versionan en git. Los archivos desencriptados (sin `.enc`) **estan en `.gitignore` y NUNCA deben borrarse despues de desencriptar**.

### Al iniciar SIEMPRE

```bash
bash decrypt.sh
```

Esto desencripta todos los archivos `.enc`. Si los archivos ya existen (ya fueron desencriptados), los salta.

### Archivos encriptados (commiteados) vs desencriptados (gitignored)

| Archivo encriptado (en git) | Archivo desencriptado (gitignored) | Contenido |
|------------------------------|-------------------------------------|-----------|
| `opencode.jsonc.enc` | `opencode.jsonc` | Config MCPs: 26 servidores, API tokens, GitHub PAT |
| `documentacion/credenciales.enc` | `documentacion/credenciales` | Passwords de servicios: n8n, Directus, Coolify, DB |

### Modo de uso

```bash
# Desencriptar todo
bash decrypt.sh

# Desencriptar un archivo especifico
bash decrypt.sh opencode.jsonc

# Re-encriptar despues de modificar
cat opencode.jsonc | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass pass:5486 -base64 -A > opencode.jsonc.enc
```

### `opencode.jsonc` — Archivo CRITICO de MCPs

**Este es EL archivo de configuracion de MCPs.** Sin el, el agente no tiene acceso a ninguna herramienta externa.

Define **26 servidores MCP** que conectan con: Cloudflare, Clerk, OpenAI, Coolify, MercadoPago, Neon, Vercel, Google Maps, Jina, Perplexity, Scrapling, Supabase, Directus, Stays, PriceLabs, AWS (6 modulos), n8n-chitara, directus-chitara, supabase-chitara.

**Ubicacion:** `opencode.jsonc` (raiz del workspace).  
**NO hay otro archivo de configuracion MCP.**

### Si el agente detecta un secreto en texto plano

1. Marcarlo como `🔴 CRITICO`
2. Verificar que este en `.gitignore`
3. Encriptarlo y guardar el `.enc`
4. Reportarlo al usuario

### En cada commit/push

1. Verificar que `opencode.jsonc` NO este en los archivos staged (esta en `.gitignore`)
2. Verificar que `opencode.jsonc.enc` SI este actualizado
3. Si se modifico `opencode.jsonc`, re-encriptar ANTES del commit:
   ```bash
   cat opencode.jsonc | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass pass:5486 -base64 -A > opencode.jsonc.enc
   ```
4. **NUNCA** commitear `opencode.jsonc` u otro archivo con credenciales en texto plano

---

## Proposito

Este repositorio es la base de conocimiento y accion para **SandiegoApart**, operador de renta corta en Santiago Centro, Chile.

Los asistentes deben usar este repo para:
- crear y optimizar anuncios (ES/EN/PT-BR)
- generar mensajes a huespedes
- revisar reglas operativas
- analizar pricing y ocupacion
- trabajar con Stays.net y PriceLabs
- crear contenido para Instagram
- disenar automatizaciones n8n
- mantener documentacion limpia y trazable

> **🔴 PROTOCOLO OBLIGATORIO PARA CAMBIOS DE PRECIOS EN PRICE LABS**
>
> **NINGUN cambio de precio en PriceLabs puede ejecutarse sin seguir estos 10 pasos en orden.**
>
> ### Paso 1: Obtener situacion actual
> - Revisar ocupacion proximos 7 dias, 30 dias y 60 dias por unidad
> - Revisar precios actuales (base, min, max) por unidad
> - Revisar ocupacion del mercado (market occupancy) para contexto
> - Revisar fechas proximas importantes (feriados, eventos, temporada)
>
> ### Paso 2: Revisar know-how interno
> - Leer `documentacion/playbook_renta_corta.md` — playbook consolidado (diagnostico, pricing, casos de uso, respuesta LLM, checklist)
> - Leer `01_source_of_truth/pricelabs/pricing_rules.md` — reglas activas
> - Leer `05_finanzas_y_pricing/revenue_management.md` — estrategia actual
> - Revisar lecciones aprendidas en este archivo (seccion "Lecciones aprendidas")
>
> ### Paso 3: Verificar fechas relevantes
> - Consultar calendario de eventos Santiago Centro
> - Identificar feriados, ferias, conciertos, eventos deportivos
> - Evaluar si las fechas justifican cambio de precio (ver "Principio 1: El mercado manda, no el evento" en playbook_renta_corta.md)
>
> ### Paso 4: Buscar informacion complementaria
> - Usar Jina (`jina_search_web`) para buscar eventos, temporada, demanda en Santiago Centro
> - Buscar ocupacion hotelera Santiago, ferias, eventos confirmados
> - Complementar analisis con datos externos cuando aplique
>
> ### Paso 5: Elaborar propuesta
> - La propuesta SIEMPRE debe estar aplicada a un periodo especifico
> - El periodo mas urgente es: **proximos 7 dias**
> - Luego: **proximos 30 dias**
> - La propuesta debe incluir:
>   - Precio base actual y propuesto por unidad
>   - Precio minimo y maximo propuesto
>   - Justificacion basada en datos (ocupacion, mercado, competencia)
>   - Periodo de aplicacion especifico
>
> ### Paso 6: Presentar propuesta con explicacion
> - Explicar POR QUE se sugiere cada cambio
> - Mostrar datos que respaldan la decision
> - Indicar riesgos de NO hacer el cambio
> - Indicar riesgos de hacer el cambio
> - Presentar alternativas si aplica
>
> ### Paso 7: Esperar confirmacion del usuario
> - NUNCA aplicar cambios sin aprobacion explicita
> - El usuario debe confirmar con "si, aplicar" o similar
> - Si hay dudas, aclarar antes de ejecutar
>
> ### Paso 8: Aplicar cambios con confirmacion
> - Usar `pricelabs_update_listings` con `confirmed=True`
> - Documentar que cambios se aplicaron y cuando
> - Guardar snapshot de precios antes y despues
>
> ### Paso 9: Verificar cambios aplicados
> - Consultar API de PriceLabs para confirmar que los cambios se reflejaron
> - Revisar que no se aplicaron cambios en periodos no autorizados
> - Verificar proximos 30-60 dias para detectar cambios indebidos
>
> ### Paso 10: Confirmar y documentar
> - Informar al usuario que cambios fueron aplicados exitosamente
> - Actualizar `memory-bank/activeContext.md` con los cambios
> - Actualizar `memory-bank/progress.md` si corresponde
> - Documentar fecha, unidades afectadas, precios anteriores y nuevos
>
> **INCUMPLIR ESTE PROTOCOLO ES UN ERROR CRITICO.**

## Orden de lectura obligatorio

Antes de proponer cambios, leer en este orden:

1. `00_contexto_negocio/` — quien es SandiegoApart, que unidades opera, donde esta ubicado
2. `01_source_of_truth/` — fuentes de verdad (Stays, PriceLabs)
3. `02_operacion/` — reglas operativas, check-in/out, edificio
4. `03_marketing_y_ads/` — marca, tono, anuncios
5. `04_mensajeria/` — mensajes a huespedes, plantillas
6. `05_finanzas_y_pricing/` — KPIs, revenue management
7. `06_automatizacion/` — n8n, MCP, workflows
8. `08_playbooks/` — guias paso a paso
9. `documentacion/playbook_renta_corta.md` — **LECTURA OBLIGATORIA**: playbook consolidado de renta corta (diagnostico, pricing, casos de uso, checklist, respuesta LLM)
10. `documentacion/` — resto de documentacion existente (legacy)
11. `seguimiento.md` — estado actual y cambios recientes
12. `tecnologias.md` — stack tecnologico
13. `APIStaysDoc.md` — si el cambio toca Stays.net
14. `pricelabs-academy/` — si el cambio toca PriceLabs

## Datos fijos vs datos que se buscan dinamicamente

**Datos fijos en este repo** (no cambiar sin aprobacion):
- Contexto del negocio (`00_contexto_negocio/`)
- Reglas operativas (`02_operacion/`)
- Marca y tono (`03_marketing_y_ads/`)
- Plantillas de mensajes (`04_mensajeria/`)
- KPIs y finanzas (`05_finanzas_y_pricing/`)
- Playbooks (`08_playbooks/`)

**Datos que deben buscarse dinamicamente** (NO estan en este repo; consultar la fuente indicada):
| Que buscas | Donde consultarlo |
|------------|------------------|
| Descripciones de anuncios, titulos, amenities activos por unidad | Stays API o sitio publico sandiegoapart.com |
| Precios actuales, tarifas, restricciones de estadia | PriceLabs |
| Disponibilidad, calendario | Stays |
| Reservas activas, huespedes actuales | Stays API |
| Reglas de pricing dinamico | PriceLabs |
| Fotos de unidades | Stays / repositorio de imagenes |

**Importante**: Las descripciones de anuncios NO estan en PriceLabs. PriceLabs es solo pricing.
Si necesitas el contenido de un anuncio (descripcion, titulo, amenities), consulta Stays directamente.

## Fuente de verdad (jerarquia obligatoria)

1. **Stays**: calendario, tarifas, disponibilidad, contenido publicado, amenities, reglas activas, IDs
2. **Manuales oficiales Tarapaca 1140 y artefactos**: reglas del edificio, mantenciones, espacios comunes, restricciones
3. **Exportaciones actuales**: analisis operativo y financiero con fecha de corte
4. **PriceLabs**: pricing, reglas tarifarias, revenue management cuando este actualizado
5. **Asesorias y ebooks**: buenas practicas, marketing, comunicacion, pricing
6. **Memoria del repo**: contexto auxiliar, no fuente final

## Reglas criticas

> **🔴 REGLA #1 — ACTUALIZACION OBLIGATORIA DEL MEMORY BANK**
>
> **DESPUES DE CADA ACCION** (no al final de la sesion, no al final de la tarea — CADA accion individual), el agente DEBE actualizar:
> - `memory-bank/activeContext.md` — reflejar el estado REAL actual, cambios recientes, next steps y blockers
> - `memory-bank/progress.md` — marcar completados, agregar nuevos items en progreso
>
> **SIN EXCEPCIONES.** Si el agente ejecuto un comando en el VPS, creo un archivo, modifico una configuracion, instalo un servicio — documenta INMEDIATAMENTE. No acumular cambios para documentar despues.
>
> **INCUMPLIR ESTA REGLA ES UN ERROR CRITICO.**

- No inventar amenities — si no esta en Stays o en un archivo, no existe
- No inventar politicas — no asumir reglas del edificio sin fuente
- No exponer claves, tokens, codigos de acceso, Wi-Fi, passwords
- No prometer estacionamiento — no hay
- No prometer espacios comunes — sin confirmacion, no se mencionan
- No decir "a pasos" si no esta medido
- No usar claims exagerados (lujo, unico, imperdible, espectacular, increible)
- Mantener coherencia anuncio ↔ realidad
- Si falta un dato, dejar placeholder o pedir confirmacion
- Si hay conflicto entre documentos, usar formato de conflicto (abajo)
- En respuestas a huespedes: tono claro, amable y directo
- En contenido comercial: tono urbano, sobrio y confiable

## Contexto comercial

SandiegoApart: **Estudios modernos con terraza en Santiago Centro, pensados para trabajar y descansar.**

Ubicacion: Tarapaca 1140, Santiago Centro, Chile.

Unidades (4 estudios):
- 901 (piso 9)
- 902 (piso 9)
- 709 (piso 7)
- 702 (piso 7)

Atributos base (todas las unidades):
- Terraza privada
- Cama king
- Escritorio + silla
- Mesa alta para 2
- TV 50"
- Wi-Fi rapido
- A/C frio-calor
- Cocinha equipada
- Bano privado

No incluir sillon cama como amenity general — solo si la unidad lo tiene habilitado en Stays.
No hay estacionamiento.
No hay piscina, gimnasio, quincho, cowork ni terraza comun confirmados.

## Idiomas

- Espanol (ES)
- English (EN)
- Portugues do Brasil (PT-BR)

No traducir literal. Localizar segun cultura del huesped.

Glosario trilingue:
| ES | EN | PT-BR |
|----|----|-------|
| terraza | terrace/balcony (segun contexto) | varanda/terraco |
| cama king | king bed | cama king |
| sofa cama | sofa bed | sofa-cama |
| Wi-Fi rapido | fast Wi-Fi | Wi-Fi rapido |
| A/C frio-calor | hot/cold A/C | ar-condicionado quente/frio |
| escritorio | desk/workspace | mesa de trabalho |
| Santiago Centro | Downtown Santiago | Santiago Centro |
| Metro Moneda | Moneda metro station | metro Moneda |

## Entregables esperados

Cuando generes contenido, entregar:
- Copy de anuncio completo (titulo, subtitulo, bullets, FAQ, CTA)
- Mensajes a huesped listos para enviar
- Checklist operativo
- Contenido Instagram (copy + descripcion)
- Instrucciones para automatizacion n8n
- Todo en ES/EN/PT-BR cuando aplique

## Seguridad

**Jamas exponer en este repo:**
- Claves Wi-Fi
- Codigos de cerradura
- Codigos de caja fuerte
- Tokens API
- Passwords
- Datos de huespedes (nombres, telefonos, emails personales)
- Credenciales de plataformas
- URLs privadas con secretos
- Numeros de telefono operativos internos

Los secretos reales deben vivir en:
- Variables de entorno
- Gestor de secretos
- `.vscode/mcp.json` (ignorado por git)
- `secrets.json` (ignorado por git)

Si detectas un secreto en un archivo versionado, marcalo como CRITICAL y reportalo.

## Credenciales encriptadas

Las credenciales de todos los servicios (MCPs, APIs, bases de datos, servidores) estan encriptadas en:
- `documentacion/credenciales.enc` — archivo encriptado con AES-256-CBC
- `documentacion/decrypt.sh` — script para desencriptar

**Protocolo de desencriptado:**
1. Si el usuario pide credenciales, NO las busques en tu contexto ni en archivos planos
2. Pidele al usuario la clave de desencriptado: *"¿Cuál es la clave para desencriptar las credenciales?"*
3. Ejecuta: `echo "CLAVE" | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -d -pass pass:CLAVE -base64 -A -in documentacion/credenciales.enc`
4. NUNCA almacenes la clave en el contexto ni en el repo

## Resolucion de conflictos

Cuando haya conflicto entre documentos, usar:

> CONFLICTO DETECTADO
> Tema:
> Archivo A:
> Archivo B:
> Diferencia:
> Fuente recomendada:
> Accion sugerida:

## Lecciones aprendidas (memoria persistente)

### Protocolo de cambios de precios en PriceLabs
- **Obligatorio seguir los 10 pasos** definidos en la seccion "🔴 PROTOCOLO OBLIGATORIO PARA CAMBIOS DE PRECIOS EN PRICE LABS" (arriba en este documento)
- **Nunca aplicar cambios sin confirmacion explicita del usuario**
- **Siempre verificar cambios aplicados** via API despues de ejecutar
- **Documentar todo** en `memory-bank/activeContext.md` y `memory-bank/progress.md`

---

## 🛡️ Harness Engineering — verificacion y prevencion de errores

> *"Cada vez que un agente comete un error, disenas una solucion para que ese error no vuelva a ocurrir."* — Mitchell Hashimoto

Este proyecto implementa principios de harness engineering. El modelo es el motor; el harness (AGENTS.md, MCPs, memoria, reglas, verificaciones) es el auto.

### Hooks de verificacion obligatorios

Despues de cada operacion critica, el agente DEBE ejecutar verificacion:

| Operacion | Verificacion requerida | Tool a usar |
|-----------|----------------------|-------------|
| `pricelabs_update_listings` | Confirmar que precios se reflejan en API | `pricelabs_get_listing` |
| `pricelabs_push_prices` | Confirmar push exitoso (status + fecha) | `pricelabs_get_listing` |
| `stays_api_call` (POST/PUT) | Verificar resultado con GET correspondiente | `stays_get_reservations` |
| Cambio de precio aplicado | Actualizar tabla de ocupacion en activeContext | `edit` en memory-bank |
| Diagnostico de unidades | Validar que se consultaron AMBAS fuentes (PriceLabs + Stays) | Self-check |

**Regla:** Si una operacion de escritura no se verifica, el cambio se considera NO APLICADO.

### Reglas anti-error (derivadas de errores reales)

Estas reglas existen porque el error YA ocurrio al menos una vez:

| # | Error cometido | Regla para prevenirlo |
|---|---|---|
| 1 | MCP pricelabs-docs usaba `base_price` pero API espera `base` | **Siempre verificar nombres de campo contra documentacion real de la API** |
| 2 | Push a Stays fallaba sin feedback claro | **Siempre mostrar el status del push y `last_date_pushed` despues de aplicar** |
| 3 | Se asumian descuentos activos que no existian | **Nunca asumir configuracion. Siempre leer datos reales de la API** |
| 4 | Diagnostico solo con PriceLabs sin cruzar con reservas reales de Stays | **Cross-check obligatorio: PriceLabs + Stays reservas antes de diagnosticar** |
| 5 | Se recomendaban cambios sin verificar ocupacion del mercado | **Siempre comparar ocupacion propia vs mercado antes de sugerir precio** |
| 6 | Memory-bank desactualizado despues de cambios | **Actualizar activeContext.md y progress.md INMEDIATAMENTE despues de cada cambio** |
| 7 | AGENTS.md referenciaba archivos que ya no eran la fuente primaria | **Al crear/renombrar archivos clave, actualizar todas las referencias en AGENTS.md** |
| 8 | Cambios en chitara no quedaban documentados | **TODO cambio en el servidor chitara DEBE registrarse en `documentacion/chitara.md` (comandos, workarounds, decisiones) y en `memory-bank/`** |
| 9 | MCPs chitara no cargaban por `.venv` corrupto (falta `bin/python3`) | **Si los MCPs chitara no aparecen como tools, verificar `.venv` y reinstalar `mcp`: `rm -rf .venv && uv venv && uv pip install mcp`** |

### Verificacion en capas (para cambios de pricing)

Los cambios de precio deben pasar por 3 capas de verificacion:

1. **Pre-ejecucion (1-2 seg):** validar que `confirmed=True`, que las 4 unidades estan en el request, que los valores tienen sentido (min < base < max, no negativos)
2. **Post-ejecucion inmediata (5-10 seg):** `pricelabs_get_listing` para confirmar que cada unidad refleja los nuevos valores
3. **Post-push (30-60 seg):** verificar `last_date_pushed` actualizado y `push_enabled: true` para cada unidad

### Conexion al VPS chitara (5.252.52.190)

**Setup inicial (una sola vez por sesion de agente):**

1. Generar llave SSH: `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "opencode@teknoconecta"`
2. Imprimir llave publica: `cat ~/.ssh/id_ed25519.pub`
3. Pedir al usuario que la agregue al VPS con `ssh root@5.252.52.190 "mkdir -p ~/.ssh && echo 'LLAVE' >> ~/.ssh/authorized_keys"`
4. Probar: `ssh -o StrictHostKeyChecking=accept-new root@5.252.52.190 "echo OK"`

**Ejecutar comandos en VPS:**

```bash
ssh root@5.252.52.190 "COMANDO"
```

**Editar archivos en VPS:**

```bash
ssh root@5.252.52.190 "cat > /ruta/archivo << 'EOF'
...contenido...
EOF"
```

**Diagnostico de redes Docker en VPS:**

```bash
ssh root@5.252.52.190 "docker ps --format '{{.Names}} → {{.Networks}}'"
ssh root@5.252.52.190 "docker network inspect NOMBRE_RED"
ssh root@5.252.52.190 "docker exec CONTENEDOR node -e \"fetch('http://servicio:puerto/health').then(r=>r.text()).then(console.log)\""
```

**Documentacion completa:** `documentacion/chitara.md` seccion 28.

### Limpieza periodica del harness

Al final de cada sesion de cambios, ejecutar este checklist:

- [ ] ¿`memory-bank/activeContext.md` refleja el estado REAL actual?
- [ ] ¿`memory-bank/progress.md` tiene los ultimos cambios marcados como completados?
- [ ] ¿`AGENTS.md` tiene reglas para errores que ocurrieron en esta sesion?
- [ ] ¿Hay archivos nuevos creados que deban referenciarse en `AGENTS.md`?
- [ ] ¿Los archivos `documentacion/asesorias.md` y `Asesoria_personal.md` estan marcados como legacy y `playbook_renta_corta.md` como fuente primaria?

### Stays.net API
**Endpoints FUNCIONALES (2026-05-18):**
- ✅ `GET /external/v1/booking/reservations` — lista de reservas
- ✅ `GET /external/v1/booking/reservations/{id}` — detalle de reserva
- ✅ `POST /external/v1/booking/search-listings` — buscar listings disponibles (requiere `rooms` como array)

**Endpoints NO FUNCIONALES (404 confirmado en jairop.stays.net):**
- ❌ `POST /external/checkout/initiate`
- ❌ `POST /external/promocodes/create-promo-code`
- ❌ `POST /reservations/booking/reservations/export`
- ❌ `POST /sell-price-rules`
- ❌ `PATCH /v1/parameters/content/properties/{id}` — modificar propiedad
- ❌ `PATCH /parameters/v1/setting/listing/{id}/house-rules` — modificar reglas
- ❌ `GET /v1/parameters/content/properties/{id}` — obtener propiedad
- ❌ `GET /parameters/v1/setting/listing/{id}/house-rules` — obtener reglas
- ❌ `GET /adminmasters/price-groups`
- ❌ `GET /external/settings/app-listing-custom-fields`
- ❌ `POST /external/book-request`
- ❌ `GET /external/v1/listings`
- ❌ `GET /external/v1/properties`
- ❌ `GET /external/docs/index/`

**Conclusión:** Nuestra instancia de Stays.net tiene una API muy limitada. Solo permite **lectura de reservas y búsqueda de listings**. Ningún endpoint de escritura funciona para modificar propiedades, precios, reglas o contenido.

**Mapeo IDs:** reservas devuelven `_idlisting` (MongoDB ObjectId). Directus tiene `AlojamientoStayslistingId` (corto) y `AlojamientoStayslistingIdLargo` (ObjectId)

**Descripciones de anuncios:** no accesibles via API. Obtener del sitio publico sandiegoapart.com

### Scrapling / Chromium
- Las tools HTTP de Scrapling (get, bulk_get) funcionan sin Chromium
- Las tools de browser requieren Chromium con deps de sistema en `~/.local/lib/chrome-deps/`
- BUG: el proceso MCP de Scrapling NO hereda LD_LIBRARY_PATH al lanzar Playwright
- Workaround: usar Python+Playwright directamente desde bash con `export LD_LIBRARY_PATH=...`

> **🔴 DONDE SE DEFINEN LOS MCPs — IMPORTANTE**
>
> **TODOS los servidores MCP de este proyecto se definen en el archivo `opencode.jsonc`** (en la raíz del workspace).
>
> - El cliente OpenCode lee esta configuración al iniciar y lanza/conecta cada servidor.
> - **NO hay otro archivo de configuración MCP**. Ni `mcp.json`, ni settings del sistema, ni variables de entorno globales.
> - Si un MCP no aparece en `opencode.jsonc`, no existe para este workspace.
> - Para modificar un MCP (cambiar su código, agregar tools, cambiar credenciales), editar:
>   1. El archivo `server.py` dentro de `./mcp-servers/{nombre}/`
>   2. Y/o las variables de entorno en la sección `"environment"` de `opencode.jsonc`
>
> Ubicación absoluta: `/mnt/c/Users/jairo/OneDrive/Documents/GitHub/n8n_teknoconecta/opencode.jsonc`

### MCPs disponibles
26 servidores MCP configurados en `opencode.jsonc`: clerk, neon, vercel, openai, jina, perplexity, google-maps, mercadopago, n8n-mcp, supabase, directus, stays-docs, scrapling, pricelabs-docs, cloudflare, cloudflare-dns, interactive-terminal, awsKnowledge, awsApi, awsServerless, awsSnsSqs, awsCloudWatch, awsIam, n8n-chitara, directus-chitara, supabase-chitara.

**Tipos de MCP en este proyecto:**
- **Remote**: servidores MCP hospedados por el proveedor (ej. `clerk`, `vercel`, `supabase`). Requieren URL + headers de autenticacion.
- **Local**: servidores MCP ejecutados en la maquina local (ej. `neon`, `openai`, `scrapling`, `n8n-mcp`). Requieren `command` para lanzar el proceso MCP.

### MCPs locales con APIs externas (patron stays-docs / pricelabs-docs)

Algunos MCPs de este proyecto son **locales pero conectan APIs externas**. En vez de llamar directamente a la API desde el agente, se usa un servidor MCP propio que envuelve la API y expone herramientas tipadas.

**Ventajas de este patron:**
- Documentacion embebida: cada tool tiene descripcion, parametros y ejemplos en el servidor MCP
- Validacion de entrada: el servidor MCP valida parametros antes de llamar la API
- Escritura con confirmacion: los servidores de Stays (read-only) y PriceLabs (POST con `confirmed=True`) protegen contra cambios accidentales
- Reutilizable: cualquier agente conectado al mismo MCP obtiene las mismas herramientas

**Como se define en `opencode.jsonc`:**

```json
"stays-docs": {
  "type": "local",
  "command": [
    "uv",
    "run",
    "--directory",
    "/mnt/c/Users/jairo/OneDrive/Documents/GitHub/n8n_teknoconecta",
    "./mcp-servers/stays-docs/server.py"
  ],
  "environment": {
    "STAYS_API_BASE_URL": "https://jairop.stays.net",
    "STAYS_API_KEY": "..."
  }
}
```

**Estructura del servidor MCP local:**
- Ubicacion: `./mcp-servers/{nombre}/server.py`
- Stack: Python + `mcp` SDK (model context protocol)
- Cada servidor define `tools` con nombre, descripcion, parametros (JSON Schema) y handler
- El handler hace la llamada HTTP a la API externa y retorna el resultado formateado

**Ejemplos en este repo:**
| MCP | API externa | Ubicacion servidor | Funcion |
|-----|-------------|-------------------|---------|
| `stays-docs` | Stays.net API | `./mcp-servers/stays-docs/server.py` | Reservas, listings (lectura). Escritura habilitada con `confirmed=True` pero endpoints de Stays devuelven 404 |
| `pricelabs-docs` | PriceLabs API | `./mcp-servers/pricelabs-docs/server.py` | Listings, precios, update/push precios (POST con confirmacion) |

**Reglas para crear un nuevo MCP local con API externa:**
1. Crear carpeta `./mcp-servers/{nombre}/`
2. Implementar `server.py` usando el SDK de MCP en Python
3. Definir tools con descripcion clara, parametros tipados y ejemplos
4. Usar variables de entorno para credenciales (NO hardcodear en el script)
5. Registrar en `opencode.jsonc` con `"type": "local"` y `"command"` que ejecute `uv run`
6. Preferir operaciones read-only a menos que el caso de uso justifique writes
7. Documentar endpoints funcionales vs no funcionales en este archivo (AGENTS.md)

### MCPs chitara — administracion del VPS via SSH (n8n-chitara, directus-chitara, supabase-chitara)

Estos 3 MCPs son locales (Python + `mcp` SDK) que se conectan al VPS `5.252.52.190` via SSH para administrar servicios directamente.

**Arquitectura:**
```
opencode → MCP server (local) → SSH → VPS chitara → contenedor Docker (n8n / directus / postgres)
```

**Servidores MCP chitara:**

| MCP | Base de datos | Contenedor | Funcion |
|-----|--------------|------------|---------|
| `n8n-chitara` | PostgreSQL `n8n` | `postgres` + `n8n` | CRUD workflows, ejecuciones, activacion, server info |
| `directus-chitara` | Interna (SQLite/API) | `directus` | CRUD colecciones, items, fields, files, flows, relations |
| `supabase-chitara` | PostgreSQL `sandiegoapart` | `postgres` + `supabase-*` | SQL, tablas, migraciones, extensiones, funciones, RLS |

**Dependencia critica:** Los 3 MCPs chitara requieren el paquete Python `mcp` instalado en el `.venv` del proyecto:
```bash
cd /mnt/c/Users/jairo/OneDrive/Documents/GitHub/n8n_teknoconecta
uv venv && uv pip install mcp
```
Si el `.venv` esta corrupto (falta `bin/python3`), eliminarlo primero: `rm -rf .venv`.

**Verificar que los MCPs chitara cargaron en sesion:**
- `n8n_chitara_list_workflows` debe devolver 25 workflows
- `directus_chitara_list_collections` debe devolver ~146 colecciones
- `supabase_chitara_list_tables` (schema=public) debe devolver ~155 tablas

**Nombres de herramientas (prefijo):**
- `n8n-chitara` → `n8n_chitara_*` (12 tools)
- `directus-chitara` → `directus_chitara_*` (22 tools)
- `supabase-chitara` → `supabase_chitara_*` (13 tools)

> **🔴 IMPORTANTE**: Los MCPs chitara NO son lo mismo que los MCPs cloud (`n8n-mcp`, `directus`, `supabase`). Los MCPs cloud apuntan a `*.teknoconectapp.com` (solo 1 workflow en n8n cloud). Los MCPs chitara apuntan al VPS via SSH (25 workflows, 146 colecciones, 155 tablas). Para operar sobre el negocio real, usar SIEMPRE los MCPs chitara.

### Verificacion de inicio de sesion (session startup checklist)

Al iniciar cada sesion nueva de OpenCode, el agente DEBE ejecutar esta verificacion:

```
1. SSH: ssh -o ConnectTimeout=5 root@5.252.52.190 "echo SSH_OK"
2. n8n-chitara: n8n_chitara_list_workflows → debe devolver ~25 workflows
3. directus-chitara: directus_chitara_list_collections → debe devolver ~146 colecciones
4. supabase-chitara: supabase_chitara_list_tables → debe devolver ~155 tablas
5. MCPs cloud funcionales: n8n-mcp, directus, supabase (para operaciones cloud si aplica)
```

Si algun MCP chitara no aparece como herramienta:
1. Verificar que el paquete `mcp` esta instalado: `uv pip list | grep mcp`
2. Si no esta: reinstalar venv con `rm -rf .venv && uv venv && uv pip install mcp`
3. Reiniciar OpenCode para que cargue los MCPs locales

### PriceLabs Academy
- 365 articulos del portal de ayuda PriceLabs en espanol en `documentacion/pricelabs-academy/`
- Organizados en 7 archivos .md por categoria
- URL patron: `https://help.pricelabs.co/portal/es/kb/articles/{slug}`
- El portal es SPA React (Zoho Desk). Requiere browser con JS
- Scripts de scraping: `/tmp/pl_collect_urls.py`, `/tmp/pl_download.py`

### Seguridad detectada en el repo
- CRITICAL: `exportadata/exportar_supabase.ipynb` contiene Supabase anon key + PII de huespedes + direccion personal del host en celdas de output. Debe removerse de git history
- CRITICAL: `exportadata/export_20260504_104837.xlsx` contiene datos de reservas con PII. Debe removerse de git
- HIGH: Varios workflows contienen numeros de telefono y emails hardcodeados. Deben migrarse a credential nodes
- El directorio `09_archive/` existe para contenido deprecated que no debe perderse pero tampoco confundirse con documentacion activa

## Skills / subagentes disponibles

- `sandiegoapart-stays-ops`: operaciones Stays (listings, API, calendarios, reglas)
- `sandiegoapart-brand-ads`: anuncios y marketing trilingue
- `sandiegoapart-guest-messaging`: mensajeria a huespedes
- `sandiegoapart-revenue-pricing`: pricing y finanzas
- `sandiegoapart-building-rules`: reglas del edificio y mantenimiento
- `sandiegoapart-data-curator`: curaduria de conocimiento del repo
- `sandiegoapart-automation-n8n`: automatizacion n8n/MCP
- `graphify`: conocimiento grafico del repo. Mapea todo el proyecto (docs, codigo, datos) en un grafo consultable. Usar `graphify install --platform opencode` para registrar. Output: `graphify-out/graph.html`, `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`.
  - **Usar para**: preguntas cross-dominio (ej: "como se conecta Stays con mensajeria?")
  - **NO usar para**: busqueda de archivos especificos, entender una carpeta, tareas diarias

## Compatibilidad multi-agente

- `AGENTS.md` es la referencia principal
- `CLAUDE.md`, `OPENCODE.md` y `.github/copilot-instructions.md` son archivos delgados que redirigen a este documento sin introducir reglas contradictorias

## graphify

This project has a knowledge graph at `graphify-out/graph.json` (104 nodes, 79 edges).
The graph supplements the directory structure — it does NOT replace it.

**When to use the graph:**
- Cross-module questions: "how does X in operacion connect to Y in automatizacion?"
- Finding unexpected relationships between different domains
- Tracing paths across communities

**When NOT to use the graph (use directory structure instead):**
- Finding specific files (use glob/grep)
- Understanding what a directory contains (read it directly)
- Most day-to-day queries — the directory structure `00_` through `09_` is the primary map

**How to use:**
- `/graphify query "question"` — BFS traversal for broad context
- `/graphify query "question" --dfs` — DFS for specific paths
- `/graphify path "ConceptA" "ConceptB"` — shortest path between concepts
- `/graphify update .` — after code changes (AST-only, no API cost)
- Git hooks installed: auto-rebuilds graph on `git commit` (AST-only, free, no API cost)
