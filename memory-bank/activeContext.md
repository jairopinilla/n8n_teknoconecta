# Active Context — TeknoConecta

## Current Focus

Servidor chitara (5.252.52.190): Directus instalado con S3 storage. Pendiente migrar 155 archivos de Supabase S3 → AWS S3 y agregar nuevos MCPs AWS.

## Recent Changes

### Instalacion Directus + S3 storage (2026-05-26)
- **Directus instalado en chitara** (`/opt/homelab/directus/`), imagen `directus/directus:latest`
- **Conectado a sandiegoapart** via red `postgres_default`, 152 tablas visibles como colecciones
- **Storage configurado en AWS S3:**
  - Bucket: `sandiegoapart-directus` (us-east-1)
  - Driver: `s3` (mismo nombre que usaba Supabase → registros existentes compatibles)
  - Upload verificado: archivo de prueba subido exitosamente via API
- **URL:** `https://directus.chitaraagenteia.com` (Cloudflare tunnel + DNS)
- **Login:** `contacto@teknoconecta.com` / `ChitaraAdmin2026!`
- **Problema login inicial:** DB ya tenia tablas Directus del Supabase anterior → bootstrap no creo nuevo admin → contrasena reseteada directamente en PostgreSQL con argon2
- **155 archivos en DB** todos con `storage=s3` — metadata existe pero archivos fisicos estan en Supabase S3 bucket `supabase.teknoconecta` (privado)

### MCPs chitara expandidos a gestion completa (2026-05-26)
- **n8n-chitara:** 12 herramientas (list/get/create/update/delete/activate/deactivate/execute/export workflows, list/get executions, server info). Gestiona via psql directo + n8n CLI.
- **directus-chitara:** 25 herramientas (CRUD completo: collections, items, fields, files, flows, relations + server info). Usa API via auth token.
- **supabase-chitara:** 13 herramientas (schemas, tables, columns, query, exec_sql, migrations, extensions, functions, indexes, policies, roles, server info).
- **n8n API key resuelto:** generado JWT firmado con `N8N_ENCRYPTION_KEY` del contenedor. Insertado en `user_api_keys` con full scopes. `N8N_API_KEY` env var set en `.env`.
- **n8n ejecucion:** activate workflow + trigger via webhook HTTP. n8n CLI no funciona con instancia corriendo (puerto 5679 en uso).

### AWS MCPs agregados a opencode.jsonc (2026-05-26)
- 6 nuevos MCPs: `awsKnowledge`, `awsApi`, `awsServerless`, `awsSnsSqs`, `awsCloudWatch`, `awsIam`
- Region: `us-east-1`, credenciales de IAM configuradas como env vars
- **Requiere reinicio de opencode para activarse**

### Regla critica #1 — Actualizacion obligatoria del memory-bank (2026-05-26)
- **Agregada en `AGENTS.md`** como REGLA #1 con advertencia de error critico
- Despues de CADA accion individual (no al final de la sesion), el agente DEBE actualizar `activeContext.md` y `progress.md`

### Supabase CLI actualizado (2026-05-26)
- `CURRENT_CLI_VERSION` cambiado de `2.53.6` → `2.101.0` en docker-compose de supabase-studio

### Auth keys de Supabase Studio (2026-05-26)
- JWT secret configurado en PostgreSQL (`app.settings.jwt_secret`)
- `SUPABASE_ANON_KEY` y `SUPABASE_SERVICE_KEY` configurados en docker-compose
- Sin gotrue no hay login/signup por user/pass — **reemplazado por Cloudflare Access**

### Cloudflare Access Google SSO (2026-05-26)
- **n8n**, **Directus**, **Supabase Studio** y **Shlink Web** protegidos con Google SSO via Cloudflare Access
- Verificado funcionando en n8n y Directus
- `go.chitaraagenteia.com` es publico (sin login, solo redirects)

### Shlink instalado (2026-05-26)
- **Shlink server** (`go.chitaraagenteia.com`, puerto 8087): motor de redireccion publico
- **Shlink web client** (`links.chitaraagenteia.com`, puerto 8089 → contenedor 8080): panel admin protegido con Google SSO
- Base de datos: `shlink` en PostgreSQL local
- API Key: `4-lAyPFN9VSVUmWmkSiHwfJKWoM-exENAuFMamWqyks`
- Version: 5.0.2, short URL de prueba funcional
- **Fix:** nginx interno escucha en 8080, mapeo corregido de `8089:80` a `8089:8080`

### MCPs chitara locales (2026-05-26)
- **n8n-chitara:** `mcp-servers/n8n-chitara/server.py` — lista workflows, ejecuciones, get workflow/ejecucion. Usa SSH → localhost:5678. API key nueva generada (vence 2027)
- **directus-chitara:** `mcp-servers/directus-chitara/server.py` — lista colecciones, get items, files, server info. Usa SSH → localhost:8055
- **supabase-chitara:** `mcp-servers/supabase-chitara/server.py` — lista schemas, tablas, columnas, SQL queries/exec via meta + direct psql. Usa SSH
- Registrados en `opencode.jsonc` — requieren reinicio para activarse
- **Verificado:** n8n-chitara funcional (25 workflows detectados)

### Fix Supabase Studio — schemas no cargaban (2026-05-26)
- **Error:** `Failed to load schemas` + Zod validation error `formattedError: expected string, received undefined`
- **Causa raiz:** `supabase-meta` solo estaba en `supabase_net`, no en `postgres_default`. No podia resolver hostname `postgres`
- **Solucion:** Agregar `postgres_default` como red adicional al servicio `meta` en `/opt/homelab/supabase/docker-compose.yml`
- **Verificacion:** `docker exec supabase-meta node -e "..."` confirma 11 schemas retornados correctamente
- **Documentado en:** `chitara.md` seccion 28.8 (leccion de redes Docker)

### Conexion SSH al VPS documentada (2026-05-26)
- **Setup de llaves SSH** documentado en `AGENTS.md` y `chitara.md` seccion 28
- Procedimiento: generar llave local → compartir pubkey → usuario agrega al VPS → probar conexion
- Patron obligatorio: `ssh root@5.252.52.190 "COMANDO"`
- Comandos de diagnostico Docker documentados

### Migracion Supabase Cloud → chitara (2026-05-26)
- **Base sandiegoapart en chitara recreada** desde cero con dump fresco de Supabase Cloud
- **Datos verificados:** 152 tablas en public, datos de negocio 100% identicos
- **Workaround documentado en `chitara.md` seccion 12.5:** instalacion de extensiones (pgvector, postgis, ltree, pgcrypto, etc.), manejo de halfvec en schema extensions, pg_dump/pg_restore con flags correctos
- **Extensiones instaladas en postgres:18:** vector (0.8.2), postgis, ltree, pgcrypto, unaccent, uuid-ossp, pg_stat_statements
- **Problema resuelto:** halfvec debia estar en schema `extensions` no en `public` → `DROP EXTENSION vector CASCADE; CREATE EXTENSION vector SCHEMA extensions;`
- **Conexion SSH:** root@5.252.52.190 establecida via paramiko
- **Credenciales PostgreSQL chitara:** usuario=chitara, db=chitara, password en .env del servidor

### Ajuste de precios — 25 mayo 2026 (diagnostico completo + aplicacion)
- **Diagnostico completo** de las 4 unidades con datos de PriceLabs + Stays (reservas)
- **Cambios aplicados y pushed a Stays:**
  - **902:** base $25,000 → **$27,000** (+8%). Recuperacion confirmada: de 0% a 67% en 7 dias.
  - **702:** base $32,303 → **$28,000** (-13%), min $22,424 → **$20,000**. 30% ocup a 30d, solo 2 reservas.
  - **709:** base $33,331 → **$28,000** (-16%), min $25,125 → **$20,000**. Solo 1 reserva, 23 noches vacias consecutivas.
  - **901:** sin cambios ($28,227). 93% ocup a 30d, casi lleno.
- **Pendiente manual en dashboard PriceLabs:** descuento -20% desde 3 noches (todas), ultimo minuto -15% a 7d (702+709)

### Consolidacion del playbook de renta corta (2026-05-25)
- **Creado `documentacion/playbook_renta_corta.md`** que fusiona `asesorias.md` + `Asesoria_personal.md`
- **Fuentes:** Pack Maestro Airbnb (Bonos 1-6 + EBook) + transcripciones de asesorias pagadas 1-on-1
- **Archivos legacy marcados:** `asesorias.md` y `Asesoria_personal.md` ahora tienen aviso de LEGACY
- **AGENTS.md actualizado** con seccion de Harness Engineering: hooks de verificacion, reglas anti-error, verificacion en capas, limpieza periodica
- **Nuevas secciones clave agregadas:**
  - Glosario operativo completo (ADR, RevPAR, ventana de reserva, dias huerfanos, evento unicornio)
  - Marco general de diagnostico (12 puntos)
  - 13 casos de uso con diagnostico, accion, que NO hacer y senal de mejora
  - 8 casos ejemplo abstraidos de situaciones reales (A-H)
  - Playbook de respuesta para LLM (9 escenarios con respuestas exactas)
  - Checklist maestro de diagnostico (22 preguntas)
  - 15 errores frecuentes documentados
- **AGENTS.md actualizado** para referenciar el nuevo playbook en Protocolo Paso 2 y Orden de Lectura

### Protocolo de cambios de precios en PriceLabs (2026-05-18)
- **Creado protocolo formal de 10 pasos** obligatorio para cualquier cambio de precio en PriceLabs
- **Agregado a `AGENTS.md`** en seccion prominente con advertencia de error critico si se incumple
- **Los 10 pasos incluyen:** obtener situacion, revisar know-how, verificar fechas, buscar info complementaria, elaborar propuesta, presentar explicacion, esperar confirmacion, aplicar cambios, verificar aplicados, confirmar y documentar
- **Primera aplicacion del protocolo:** Unidad 902 ejecutada exitosamente
- **Bugs MCP encontrados y corregidos:**
  - `pricelabs_update_listings`: remapeo de `base_price`/`min_price`/`max_price` → `base`/`min`/`max` (la API usa nombres sin `_price`)
  - `pricelabs_push_prices`: corregido `listing` → `listing_id` (la API espera `listing_id`)
  - Auto-append `pms: "stays"` si no se especifica

### Aplicación de precios — Unidad 902 (2026-05-18)
- **Precio base:** $28,000 → **$25,000** (-10.7%)
- **Precio mínimo:** $25,000 → **$23,000** (-8%)
- **Precio máximo:** no definido → **$50,000** (nuevo límite)
- **Push a Stays:** ejecutado exitosamente
- **Impacto inmediato:** ocupación 7d pasó de 0% a 14% (proyección)
- **Origen:** Unidad en crisis con 0% ocupación próximos 7 días (vs 20% mercado)
- **Revisión programada:** 25 mayo 2026 — evaluar si mantener o revertir

### Descripciones de anuncios (2026-05-18)
- **Decisión:** Todas las unidades (901, 902, 702, 709) comparten las mismas descripciones.
- **Capacidad unificada:** Hasta 3 huéspedes (cama king + sofá cama) en las 4 unidades.
- **Archivo único creado:** `03_marketing_y_ads/anuncios_mejorados/anuncio_todas_unidades_stays.md` — versión limpia lista para copiar y pegar en Stays.
- **Contenido actualizado en Stays:** La unidad 702 ya refleja las nuevas descripciones en el sitio público.
- **Sin emoticones** en campos de texto (Stays no los acepta en títulos).
- **Campo "Lo que ofrece este lugar":** ≤500 caracteres, con ubicación, amenities y perfil del huésped.
- **Reglas Adicionales:** Nuevo campo separado con capacidad, fumar (multa 100 USD), terraza, bicicletas, early/late check-in.

### Verificación API Stays.net (2026-05-18) — ACTUALIZADO
- **Endpoints de escritura probados (todos devuelven 404):**
  - `POST /external/checkout/initiate`
  - `POST /external/promocodes/create-promo-code`
  - `POST /reservations/booking/reservations/export`
  - `POST /sell-price-rules`
  - `PATCH /v1/parameters/content/properties/{id}`
  - `PATCH /parameters/v1/setting/listing/{id}/house-rules`
  - `GET /v1/parameters/content/properties/{id}`
  - `GET /parameters/v1/setting/listing/{id}/house-rules`
  - `GET /adminmasters/price-groups`
  - `GET /external/settings/app-listing-custom-fields`
  - `POST /external/book-request`
  - `GET /external/v1/listings`
  - `GET /external/v1/properties`
- **Endpoints FUNCIONALES:** Solo lectura de reservas (`GET /external/v1/booking/reservations`, `GET /external/v1/booking/reservations/{id}`) y búsqueda de listings (`POST /external/v1/booking/search-listings`)
- **Conclusión:** Nuestra instancia de Stays.net tiene una API extremadamente limitada. **Ningún endpoint de escritura funciona.** Todo debe hacerse manualmente desde el CMS de Stays.
- **MCP stays-docs modificado:** Ahora soporta POST/PUT/PATCH con `confirmed=True` (aunque los endpoints fallen). DELETE bloqueado por seguridad.

### Análisis PriceLabs (2026-05-25) — ACTUALIZADO post-cambios
| Unidad | Ocup. 7d | Ocup. 30d | Ocup. 60d | Base | Min | Estado |
|--------|----------|-----------|-----------|------|-----|--------|
| 901 | 86% | 93% | 67% | $28,227 | $20,480 | 🟢 Fuerte |
| 902 | 57% | 67% | 72% | **$27,000** | $23,000 | 🟢 Recuperado |
| 702 | 57% | 30% | 15% | **$28,000** | **$20,000** | 🟡 Bajo |
| 709 | 86% | 33% | 17% | **$28,000** | **$20,000** | 🔴 Critico |

### Modificación MCP pricelabs-docs (2026-05-18)
- **Archivo modificado:** `mcp-servers/pricelabs-docs/server.py`
- **Cambio:** El tool `pricelabs_api_call` ahora acepta `POST`, `PUT`, `PATCH` (además de `GET`).
- **Bug corregido:** Se cambió `data=body` por `content=body.encode("utf-8")` en POST/PUT/PATCH para enviar JSON correctamente.
- **Nuevos wrappers de escritura:**
  - `pricelabs_update_listings(listings, confirmed=True)` → POST /v1/listings
  - `pricelabs_push_prices(listing_id, pms, confirmed=True)` → POST /v1/push_prices
  - `pricelabs_add_listings_data(listing_id, pms, confirmed=True)` → POST /v1/add_listings_data
  - `pricelabs_fetch_prices(listing_id, pms)` → POST /v1/fetch_prices (lectura)
- **Seguridad:** Operaciones de escritura requieren parámetro `confirmed=True`. Sin confirmación, devuelve mensaje pidiendo aprobación.
- **`DELETE` permanente bloqueado.**
- **Estado:** Cambio guardado en disco. **Requiere reinicio de opencode para activarse.**

## Inconsistencias detectadas en Stays (configuración del listing)

Estos campos **NO** vienen de las descripciones de texto sino de la configuración del listing en Stays. Deben corregirse manualmente desde el panel de Stays:

| Problema | Unidades | Corrección en Stays |
|----------|----------|---------------------|
| Camas muestran "Cama Queen" | 702, 709 | Cambiar a **"Cama King"** |
| "Gimnasio (privado)" en amenities | Todas | Cambiar a **"Gimnasio (área común)"** o quitar |
| Mascotas: "bajo pedido" | Todas | Cambiar a **"no"** |
| Tiempo de descanso 23:00-16:00 | 901, 902, 709 | Unificar a horario de silencio real (20:00/24:00) |
| Parrilla en amenities | Todas | Confirmar si está disponible en terraza |
| Early/late check-out | Todas | Configurar como "bajo petición" |

## Next Steps (al reiniciar opencode)

1. **🔴 CRITICO: Migrar 155 archivos** de Supabase S3 → AWS S3 (`sandiegoapart-directus`)
   - Necesita service role key de Supabase (JWT `eyJ...`)
   - Archivos en bucket `supabase.teknoconecta` bajo prefijo `directus-server/`
   - Registros en `directus_files` ya apuntan a `storage=s3` — no requieren cambios
2. **Usar nuevos MCPs AWS** (awsApi, awsServerless, etc.) para gestionar S3
3. **Reparar n8n en chitara** — requiere recrear DB limpia
4. **Corregir configuraciones manuales en Stays** (camas, mascotas, gimnasio, tiempo de descanso)
5. **Configurar Cloudflare Access** para directus.chitaraagenteia.com

## Blockers

- **MCPs AWS requieren reinicio** de opencode para activarse (ya en opencode.jsonc)
- **Supabase service role key** necesaria para descargar archivos del bucket privado
- ~~Supabase Studio no carga schemas~~ → RESUELTO (2026-05-26)
- Push falla por autenticacion HTTPS (commits locales pendientes)
- API Stays no permite escritura de propiedades/descripciones

## Active Decisions

- **¿Storage Directus?** ✅ AWS S3 (`sandiegoapart-directus`, us-east-1)
- **¿Unificar todas las unidades con mismas descripciones?** ✅ Si
- **¿API para actualizar Stays?** ❌ No existe. Todo manual desde CMS
- **¿PriceLabs base price para 902?** 🟢 $27,000 (recuperado de crisis a 67% ocup 7d)

## Blockers

~~Supabase Studio no carga schemas~~ → RESUELTO (2026-05-26): meta ahora en postgres_default

- **Push falla por autenticacion HTTPS** (commits locales pendientes).
- **API Stays no permite escritura** de propiedades/descripciones.

## Notas

- Las descripciones de texto actualizadas ya están publicadas en Stays para la unidad 702.
- PriceLabs recalcula precios 24-48h después de cambios.
- El campo "Reglas Adicionales" en Stays solo sincroniza un idioma con Airbnb.
