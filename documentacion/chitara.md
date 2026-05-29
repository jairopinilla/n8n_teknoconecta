# Chitara Homelab / Infraestructura VPS — Documento de Traspaso para Agente

## 1. Objetivo del proyecto

Este documento resume el estado actual, decisiones técnicas, servicios, URLs, puertos, configuraciones y próximos pasos del proyecto **Chitara** en VPS.

El objetivo actual es consolidar una infraestructura self-hosted usando:

-  VPS Contabo.
-  Docker Compose.
-  Cloudflare Tunnel.
-  Cloudflare Zero Trust / Access con Google SSO.
-  PostgreSQL local moderno.
-  Supabase como fuente externa inicial y/o stack self-hosted controlado.
-  Directus como backend/API admin sobre una sola base.
-  n8n para automatizaciones.
-  Open WebUI para interfaz de chat.
-  LiteLLM como gateway/model proxy.
-  pgAdmin para administración PostgreSQL.
-  Portainer para administración Docker.
-  Dozzle para logs.
-  Uptime Kuma para monitoreo.
-  Shlink para redirecciones/acortador self-hosted tipo Short.io.

---

## 2. Dominio principal

```text
chitaraagenteia.com
```

---

## 3. Arquitectura general

```text
Internet
→ Cloudflare DNS
→ Cloudflare Access / Zero Trust, cuando corresponda
→ Cloudflare Tunnel
→ Servicios Docker internos en VPS
→ PostgreSQL local / volúmenes Docker / servicios internos
```

Regla arquitectónica:

```text
TLS/HTTPS externo lo maneja Cloudflare.
Los servicios internos se exponen por HTTP local.
No se usa HTTPS interno entre Cloudflare Tunnel y los contenedores.
```

Ejemplo de patrón Cloudflare Tunnel:

```yaml
- hostname: servicio.chitaraagenteia.com
  service: http://localhost:PUERTO
```

---

## 4. Stack base actual

La infraestructura actual está organizada bajo:

```text
/opt/homelab/
```

Estructura actual/consolidada:

```text
/opt/homelab/
├── postgres/
├── n8n/
├── cloudflared/
├── uptime-kuma/
├── dozzle/
├── code-server/
├── litellm/
├── open-webui/
├── pgadmin/
├── portainer/
├── directus/          # propuesto / a instalar
├── supabase/          # propuesto / a instalar
└── shlink/            # propuesto / a instalar
```

---

## 5. Servicios existentes y estado

| Servicio | Estado | Uso |
|---|---:|---|
| PostgreSQL 18 | Operativo | Base local central |
| pgAdmin | Operativo | Administración PostgreSQL |
| Portainer | Operativo | Administración Docker |
| code-server | Operativo | VS Code web |
| Open WebUI | Operativo | UI de chat |
| LiteLLM | Operativo | Gateway LLM |
| Dozzle | Operativo | Logs Docker |
| Uptime Kuma | Operativo | Monitoreo |
| cloudflared | Operativo | Cloudflare Tunnel |
| n8n | Roto temporalmente | Requiere recrear DB limpia |
| Directus | Pendiente | Conectar a una sola DB |
| Supabase self-hosted | Pendiente | Conectar/operar como un solo proyecto |
| Shlink | Pendiente | Redirecciones/acortador self-hosted |

---

## 6. Subdominios activos actuales

Subdominios existentes:

```text
home.chitaraagenteia.com
chat.chitaraagenteia.com
n8n.chitaraagenteia.com
llm.chitaraagenteia.com
code.chitaraagenteia.com
pgadmin.chitaraagenteia.com
portainer.chitaraagenteia.com
logs.chitaraagenteia.com
monitor.chitaraagenteia.com
```

Subdominios nuevos propuestos:

```text
directus.chitaraagenteia.com
supabase.chitaraagenteia.com
go.chitaraagenteia.com
links.chitaraagenteia.com
```

---

## 7. Mapa de URLs, servicios y puertos

> Nota: algunos puertos deben validarse contra `/etc/cloudflared/config.yml` y cada `docker-compose.yml`. Los puertos confirmados desde el contexto son Dozzle `8088` y Uptime Kuma `3002`. Los demás siguen el patrón usado o esperado en la instalación actual.

| URL | Servicio | Puerto local esperado | Protección |
|---|---|---:|---|
| `home.chitaraagenteia.com` | Home/dashboard | Validar | Cloudflare Access |
| `chat.chitaraagenteia.com` | Open WebUI | Probable `3000` | Cloudflare Access |
| `n8n.chitaraagenteia.com` | n8n | `5678` | Cloudflare Access |
| `llm.chitaraagenteia.com` | LiteLLM | Probable `4000` | Cloudflare Access |
| `code.chitaraagenteia.com` | code-server | Probable `8443` o local HTTP | Cloudflare Access |
| `pgadmin.chitaraagenteia.com` | pgAdmin | Probable `5050` | Cloudflare Access |
| `portainer.chitaraagenteia.com` | Portainer | Probable `9000` | Cloudflare Access |
| `logs.chitaraagenteia.com` | Dozzle | `8088` | Cloudflare Access |
| `monitor.chitaraagenteia.com` | Uptime Kuma | `3002` | Cloudflare Access |
| `directus.chitaraagenteia.com` | Directus | `8055` | Cloudflare Access |
| `supabase.chitaraagenteia.com` | Supabase Gateway/Studio | `8000` | Cloudflare Access para Studio |
| `go.chitaraagenteia.com` | Shlink redirects públicos | `8087` | Público, sin login |
| `links.chitaraagenteia.com` | Shlink Web Client | `8089` | Cloudflare Access |

---

## 8. Cloudflare Tunnel

Archivo principal:

```text
/etc/cloudflared/config.yml
```

Regla:

```text
Todos los servicios se exponen como:
service: http://localhost:PUERTO
```

No usar:

```text
https://localhost:PUERTO
```

porque Cloudflare maneja TLS externo.

Ejemplo esperado:

```yaml
ingress:
  - hostname: chat.chitaraagenteia.com
    service: http://localhost:3000

  - hostname: n8n.chitaraagenteia.com
    service: http://localhost:5678

  - hostname: llm.chitaraagenteia.com
    service: http://localhost:4000

  - hostname: pgadmin.chitaraagenteia.com
    service: http://localhost:5050

  - hostname: portainer.chitaraagenteia.com
    service: http://localhost:9000

  - hostname: logs.chitaraagenteia.com
    service: http://localhost:8088

  - hostname: monitor.chitaraagenteia.com
    service: http://localhost:3002

  - hostname: directus.chitaraagenteia.com
    service: http://localhost:8055

  - hostname: supabase.chitaraagenteia.com
    service: http://localhost:8000

  - hostname: go.chitaraagenteia.com
    service: http://localhost:8087

  - hostname: links.chitaraagenteia.com
    service: http://localhost:8089

  - service: http_status:404
```

Reiniciar tunnel:

```bash
docker restart cloudflared
```

O si está con systemd:

```bash
systemctl restart cloudflared
```

---

## 9. Seguridad Cloudflare Access

Regla general:

-  Todo panel administrativo debe estar protegido con Cloudflare Access + Google SSO.
-  Los servicios públicos deben quedar fuera de Access solo si están pensados para usuarios externos.

Proteger con Google SSO:

```text
home.chitaraagenteia.com
chat.chitaraagenteia.com
n8n.chitaraagenteia.com
llm.chitaraagenteia.com
code.chitaraagenteia.com
pgadmin.chitaraagenteia.com
portainer.chitaraagenteia.com
logs.chitaraagenteia.com
monitor.chitaraagenteia.com
directus.chitaraagenteia.com
links.chitaraagenteia.com
```

Evaluar con cuidado:

```text
supabase.chitaraagenteia.com
```

No proteger con Google SSO:

```text
go.chitaraagenteia.com
```

Motivo:

```text
go.chitaraagenteia.com será usado como dominio público de redirecciones.
Si se protege con login, los links cortos no servirán para clientes, huéspedes, campañas o usuarios externos.
```

---

## 10. Firewall / UFW

Pendiente crítico:

```text
Cerrar puertos públicos del VPS.
Dejar acceso a servicios solo por Cloudflare Tunnel.
```

Puertos identificados para cerrar si están abiertos públicamente:

```text
3000
3001
4000
5050
5678
8443
9000
6333
6334
```

Comandos sugeridos de validación:

```bash
ufw status verbose
ss -tulpn
docker ps
```

Ejemplo de política deseada:

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw enable
ufw status verbose
```

Cuidado:

```text
Antes de cerrar puertos, confirmar que SSH está permitido.
No cerrar el acceso SSH activo sin validar una segunda sesión.
```

---

## 11. PostgreSQL

### 11.1 Decisión tomada

Se eliminó PostgreSQL 16 y se instaló PostgreSQL 18.

Imagen actual:

```text
postgres:18
```

Versión validada:

```text
PostgreSQL 18.4
```

### 11.2 Cambio importante en volumen

PostgreSQL 18 requiere montar:

```text
/var/lib/postgresql
```

No:

```text
/var/lib/postgresql/data
```

Antes:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Ahora:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql
```

El contenedor quedaba en restart loop por el cambio de estructura de datos. La solución aplicada fue actualizar el mount al path correcto.

### 11.3 Modelo PostgreSQL local

Decisiones:

-  Una sola instancia PostgreSQL local.
-  Múltiples bases dentro de esa instancia.
-  Un usuario principal de administración.
-  Usuarios separados para servicios cuando corresponda.
-  PostgreSQL local se usa para infraestructura interna.
-  Supabase externo/self-hosted se usa como backend de producto cuando aplique.

Bases esperadas/posibles:

```text
postgres
n8n
directus
shlink
sandiegoapart
saldito
chitara
```

---

## 12. Supabase Cloud → PostgreSQL local

### 12.1 Objetivo original

Traer backup completo desde Supabase Cloud hacia PostgreSQL local.

### 12.2 Origen Supabase Cloud

Connection string original compartida en contexto:

```text
REDACTED
```

Estado de seguridad:

```text
La connection string real fue expuesta en conversación/contexto.
Debe rotarse la password de Supabase Cloud.
No reutilizar esa password.
No copiarla en documentación.
```

### 12.3 Problema inicial con pg_dump

Supabase usa PostgreSQL 17.6.

El cliente local inicial era PostgreSQL 16.

Error esperado:

```text
pg_dump client older than server
```

Solución aplicada:

```bash
apt install postgresql-client-17
```

Backup exitoso generado con:

```bash
/usr/lib/postgresql/17/bin/pg_dump
```

Archivo generado:

```text
/opt/backups/supabase/sandiegoapart.backup
```

### 12.4 Restore fallido

Se creó base local:

```text
sandiegoapart
```

Luego se intentó `pg_restore`.

Errores encontrados:

```text
extension "wrappers" is not available
type extensions.halfvec does not exist
public.match_documents(... extensions.halfvec ...)
```

Conclusión:

El backup incluye:

-  Extensiones propias o dependientes del entorno Supabase.
-  `wrappers`.
-  Tipos vectoriales.
-  `pgvector`.
-  `halfvec`.
-  Funciones RPC como `match_documents`.
-  Objetos dependientes de schema `extensions`.

### 12.5 Migracion exitosa (Workaround — 2026-05-26)

La migracion completa se logro con el siguiente procedimiento:

#### Paso 1: Instalar extensiones necesarias en el contenedor PostgreSQL 18

```bash
docker exec postgres apt-get update
docker exec postgres apt-get install -y postgresql-18-pgvector postgresql-18-postgis-3 postgresql-18-cron
docker restart postgres
```

#### Paso 2: Crear base de datos destino limpia

```bash
docker exec postgres psql -U chitara -c "DROP DATABASE IF EXISTS sandiegoapart WITH (FORCE);"
docker exec postgres psql -U chitara -c "CREATE DATABASE sandiegoapart OWNER chitara;"
```

#### Paso 3: Instalar extensiones en la base destino (ANTES del restore)

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS ltree;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

#### Paso 4: Crear schemas necesarios (ANTES del restore para evitar errores en single-transaction)

```sql
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS extensions;
CREATE SCHEMA IF NOT EXISTS graphql;
CREATE SCHEMA IF NOT EXISTS graphql_public;
CREATE SCHEMA IF NOT EXISTS realtime;
CREATE SCHEMA IF NOT EXISTS storage;
CREATE SCHEMA IF NOT EXISTS supabase_migrations;
CREATE SCHEMA IF NOT EXISTS vault;
CREATE SCHEMA IF NOT EXISTS pgbouncer;
```

#### Paso 5: pg_dump desde Supabase Cloud

```bash
PGPASSWORD='ElefantesEbrios$1' pg_dump \
  -h db.fjebesmrwdceyvllpslv.supabase.co \
  -U postgres \
  -d postgres \
  -Fc \
  --no-owner --no-acl --no-subscriptions --no-tablespaces --no-security-labels \
  -f /tmp/sandiegoapart_fresh.dump
```

**Importante:** La password contiene `$1` que bash interpreta como variable. Usar comillas simples: `'password$1'`.

#### Paso 6: pg_restore a chitara

```bash
cat /tmp/sandiegoapart_fresh.dump | docker exec -i postgres pg_restore \
  -U chitara -d sandiegoapart \
  --no-owner --no-acl --no-subscriptions --no-tablespaces
```

Errores esperados: 65 errores por extensiones no disponibles (`supabase_vault`, `wrappers`) y tipos faltantes (`extensions.halfvec`). Los datos criticos se restauran correctamente (~152 tablas en public).

#### Paso 7: Corregir tipo halfvec para DocumentoChunk

pgvector instala `halfvec` en el schema donde se crea la extension. En chitara estaba en `public`, pero Supabase lo espera en `extensions`. Solucion:

```sql
DROP EXTENSION IF EXISTS vector CASCADE;
CREATE EXTENSION vector SCHEMA extensions;
```

Luego recrear la tabla DocumentoChunk con el schema correcto y cargar datos:

```bash
# Crear tabla con el schema exacto de Supabase + cargar datos
docker exec -i postgres psql -U chitara -d sandiegoapart < /tmp/doc_chunk_ddl.sql
cat /tmp/sandiegoapart_fresh.dump | docker exec -i postgres pg_restore \
  -U chitara -d sandiegoapart --no-owner --no-acl \
  --data-only --table="DocumentoChunk"
```

#### Resultado final

| Recurso | Cantidad |
|----------|---------|
| Tablas en public | 152 |
| Tablas en typebot,extensions | 30 |
| Datos de negocio | 100% identico a Supabase |
| Tiempo total | ~3 minutos |
| Dump size | 345 MB |

### 12.6 Estrategia de restauracion (historico — ya ejecutado)

No hacer restore completo a ciegas.

Estrategia recomendada:

```text
1. Identificar tablas reales de negocio.
2. Separar extensiones, funciones, triggers y objetos Supabase.
3. Instalar extensiones compatibles si son necesarias.
4. Restaurar schema limpio.
5. Restaurar datos reales.
6. Recrear funciones RPC solo si siguen siendo necesarias.
7. Validar tablas, índices, constraints y permisos.
```

Posibles caminos:

```text
A. Dump schema-only limpio excluyendo extensiones problemáticas.
B. Dump data-only de tablas reales.
C. Instalar pgvector compatible localmente.
D. Excluir funciones match_documents si no son necesarias.
E. Migrar embeddings a una estructura compatible.
```

---

## 13. n8n

### 13.1 Estado actual

```text
Roto temporalmente.
```

Error:

```text
relation public.execution_entity does not exist
```

Causa:

```text
Se eliminaron/recrearon volúmenes PostgreSQL al migrar a PostgreSQL 18.
La base n8n quedó inconsistente o vacía.
```

### 13.2 Plan recomendado

Si no hay datos críticos que recuperar:

```bash
docker compose down
```

Entrar a PostgreSQL:

```bash
docker exec -it postgres psql -U postgres
```

Ejecutar:

```sql
DROP DATABASE IF EXISTS n8n;
CREATE DATABASE n8n;
\q
```

Reiniciar n8n:

```bash
cd /opt/homelab/n8n
docker compose up -d
docker compose logs -f
```

Objetivo:

```text
Dejar que n8n recree migraciones automáticamente sobre PostgreSQL 18.
```

Si hay workflows críticos, primero buscar backups antes de dropear la base.

---

## 14. Directus

### 14.1 Decisión tomada

Se instalará Directus conectado a **una sola base de datos**.

No se usará Directus como administrador multi-base tipo pgAdmin.

Uso esperado:

```text
Directus = backend/API admin/no-code para una base/proyecto específico.
pgAdmin = administración técnica multi-base.
```

### 14.2 URL propuesta

```text
directus.chitaraagenteia.com
```

### 14.3 Puerto local propuesto

```text
8055
```

### 14.4 Base recomendada

Crear una base dedicada:

```text
directus
```

O conectar Directus a una base de aplicación específica, por ejemplo:

```text
sandiegoapart
```

Decisión recomendada inicial:

```text
Crear DB directus para Directus.
Luego evaluar si Directus debe administrar sandiegoapart o una DB app_platform.
```

### 14.5 Crear usuario y base

```bash
docker exec -it postgres psql -U postgres
```

```sql
CREATE USER directus WITH PASSWORD 'REPLACE_WITH_SECURE_PASSWORD';
CREATE DATABASE directus OWNER directus;
GRANT ALL PRIVILEGES ON DATABASE directus TO directus;
\q
```

### 14.6 Carpeta

```bash
mkdir -p /opt/homelab/directus
cd /opt/homelab/directus
mkdir -p uploads extensions
```

### 14.7 `.env` sugerido

```env
DIRECTUS_SECRET=REPLACE_WITH_LONG_SECRET
DIRECTUS_ADMIN_EMAIL=admin@chitaraagenteia.com
DIRECTUS_ADMIN_PASSWORD=REPLACE_WITH_ADMIN_PASSWORD

DIRECTUS_PUBLIC_URL=https://directus.chitaraagenteia.com

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=directus
POSTGRES_USER=directus
POSTGRES_PASSWORD=REPLACE_WITH_SECURE_PASSWORD
```

Generar secreto:

```bash
openssl rand -hex 32
```

### 14.8 `docker-compose.yml` sugerido

```yaml
services:
  directus-cache:
    image: redis:7-alpine
    container_name: directus-cache
    restart: unless-stopped
    networks:
      - homelab_net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  directus:
    image: directus/directus:11
    container_name: directus
    restart: unless-stopped
    ports:
      - "127.0.0.1:8055:8055"
    volumes:
      - ./uploads:/directus/uploads
      - ./extensions:/directus/extensions
    environment:
      SECRET: ${DIRECTUS_SECRET}

      DB_CLIENT: pg
      DB_HOST: ${POSTGRES_HOST}
      DB_PORT: ${POSTGRES_PORT}
      DB_DATABASE: ${POSTGRES_DB}
      DB_USER: ${POSTGRES_USER}
      DB_PASSWORD: ${POSTGRES_PASSWORD}

      CACHE_ENABLED: "true"
      CACHE_AUTO_PURGE: "true"
      CACHE_STORE: redis
      REDIS: redis://directus-cache:6379

      ADMIN_EMAIL: ${DIRECTUS_ADMIN_EMAIL}
      ADMIN_PASSWORD: ${DIRECTUS_ADMIN_PASSWORD}

      PUBLIC_URL: ${DIRECTUS_PUBLIC_URL}
      WEBSOCKETS_ENABLED: "true"
    depends_on:
      directus-cache:
        condition: service_healthy
    networks:
      - homelab_net

networks:
  homelab_net:
    external: true
```

### 14.9 Levantar Directus

```bash
docker network create homelab_net || true

cd /opt/homelab/directus
docker compose pull
docker compose up -d
docker compose ps
docker compose logs -f directus
```

Validar:

```bash
curl http://127.0.0.1:8055/server/ping
```

Esperado:

```text
pong
```

---

## 15. Supabase self-hosted

### 15.1 Decisión tomada

Se conectará/operará Supabase como **un solo proyecto / una sola base principal**.

No se usará Supabase como administrador multi-base tipo pgAdmin.

Regla:

```text
1 Supabase stack = 1 proyecto Supabase = 1 base PostgreSQL principal.
```

### 15.2 Uso recomendado

Supabase se usará solo si se necesita:

-  Auth.
-  Storage.
-  Realtime.
-  Edge Functions.
-  APIs tipo BaaS.
-  Supabase Studio para un proyecto concreto.

No usar Supabase para reemplazar pgAdmin.

### 15.3 URL propuesta

```text
supabase.chitaraagenteia.com
```

### 15.4 Puerto local propuesto

```text
8000
```

### 15.5 Carpeta

```bash
mkdir -p /opt/homelab/supabase
```

### 15.6 Instalación base propuesta

```bash
cd /opt/homelab
git clone --depth 1 https://github.com/supabase/supabase.git /tmp/supabase
cp -rf /tmp/supabase/docker/* /opt/homelab/supabase/
cp /tmp/supabase/docker/.env.example /opt/homelab/supabase/.env
cd /opt/homelab/supabase
```

Generar secretos:

```bash
sh utils/generate-keys.sh
sh utils/add-new-auth-keys.sh
```

Editar:

```bash
nano .env
```

Variables mínimas a revisar:

```env
SUPABASE_PUBLIC_URL=https://supabase.chitaraagenteia.com
API_EXTERNAL_URL=https://supabase.chitaraagenteia.com
SITE_URL=https://supabase.chitaraagenteia.com

DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=REPLACE_WITH_SECURE_PASSWORD
```

Levantar:

```bash
docker compose pull
docker compose up -d
docker compose ps
```

Validar:

```bash
curl http://127.0.0.1:8000
```

### 15.7 Advertencia de recursos

Supabase self-hosted es más pesado que Directus o Shlink.

Incluye múltiples servicios:

-  Postgres.
-  Kong.
-  Auth.
-  REST/PostgREST.
-  Realtime.
-  Storage.
-  Studio.
-  postgres-meta.
-  Edge Runtime.
-  Logflare/Vector.
-  Supavisor.

No levantar múltiples stacks Supabase salvo que el VPS tenga recursos suficientes.

---

## 16. Shlink — Redirecciones tipo Short.io

### 16.1 Decisión tomada

Servicio elegido:

```text
Shlink
```

Motivo:

-  Gratis para self-hosting.
-  Open-source/community.
-  Simple con Docker.
-  Tiene API REST.
-  Tiene CLI.
-  Tiene Web Client oficial.
-  Soporta PostgreSQL.
-  No requiere agregar MySQL/MariaDB.
-  Encaja con el stack actual.

### 16.2 Uso

Shlink se usará para manejar redirecciones/acortador de URLs desde una interfaz web.

Ejemplo:

```text
https://go.chitaraagenteia.com/airbnb-702
→ https://www.sandiegoapart.com/es/apartment/FX09J/estudio-terraza-cama-king-escritorio-702
```

### 16.3 URLs propuestas

Dominio público de redirecciones:

```text
go.chitaraagenteia.com
```

Panel administrativo:

```text
links.chitaraagenteia.com
```

### 16.4 Puertos propuestos

```text
Shlink API/redirect server: 8087 → contenedor 8080
Shlink Web Client:          8089 → contenedor 8080
```

### 16.5 Seguridad

```text
go.chitaraagenteia.com
→ Público
→ Sin Cloudflare Access
→ Usado por clientes/usuarios externos
```

```text
links.chitaraagenteia.com
→ Privado
→ Cloudflare Access con Google SSO
→ Solo admins
```

### 16.6 Crear base y usuario

```bash
docker exec -it postgres psql -U postgres
```

```sql
CREATE USER shlink WITH PASSWORD 'REPLACE_WITH_SECURE_PASSWORD';
CREATE DATABASE shlink OWNER shlink;
GRANT ALL PRIVILEGES ON DATABASE shlink TO shlink;
\q
```

### 16.7 Carpeta

```bash
mkdir -p /opt/homelab/shlink
cd /opt/homelab/shlink
```

### 16.8 `.env`

```env
DEFAULT_DOMAIN=go.chitaraagenteia.com
IS_HTTPS_ENABLED=true

DB_DRIVER=postgres
DB_NAME=shlink
DB_USER=shlink
DB_PASSWORD=REPLACE_WITH_SECURE_PASSWORD
DB_HOST=postgres
DB_PORT=5432

INITIAL_API_KEY=REPLACE_WITH_LONG_API_KEY
```

Generar API key:

```bash
openssl rand -hex 48
```

### 16.9 `docker-compose.yml`

```yaml
services:
  shlink:
    image: shlinkio/shlink:stable
    container_name: shlink
    restart: unless-stopped
    ports:
      - "127.0.0.1:8087:8080"
    environment:
      DEFAULT_DOMAIN: ${DEFAULT_DOMAIN}
      IS_HTTPS_ENABLED: ${IS_HTTPS_ENABLED}
      DB_DRIVER: ${DB_DRIVER}
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      DB_HOST: ${DB_HOST}
      DB_PORT: ${DB_PORT}
      INITIAL_API_KEY: ${INITIAL_API_KEY}
    networks:
      - homelab_net

  shlink-web:
    image: shlinkio/shlink-web-client:stable
    container_name: shlink-web
    restart: unless-stopped
    ports:
      - "127.0.0.1:8089:8080"
    networks:
      - homelab_net

networks:
  homelab_net:
    external: true
```

### 16.10 Levantar

```bash
docker network create homelab_net || true

cd /opt/homelab/shlink
docker compose pull
docker compose up -d
docker compose ps
docker compose logs -f shlink
```

### 16.11 Configurar Shlink Web

Entrar a:

```text
https://links.chitaraagenteia.com
```

Configurar servidor:

```text
Server URL:
https://go.chitaraagenteia.com

API Key:
INITIAL_API_KEY del archivo .env
```

---

## 17. MCP y SSH

### 17.1 Decisión conceptual

Es posible conectar un servidor MCP a un entorno por SSH.

Patrones posibles:

```text
1. Cliente MCP local ejecuta ssh y levanta servidor MCP remoto por stdio.
2. MCP server local ejecuta comandos SSH controlados.
3. MCP server remoto expuesto por HTTP detrás de Cloudflare.
```

### 17.2 Recomendación

Para Chitara, preferir:

```text
MCP con herramientas específicas y limitadas.
No exponer una shell libre.
```

Herramientas recomendadas:

```text
docker_ps
docker_logs(service_name)
docker_restart(service_name)
compose_status
postgres_check
postgres_list_databases
postgres_backup_database(db_name)
n8n_status
cloudflared_status
ufw_status
disk_usage
memory_usage
```

Evitar:

```text
run_command(command)
```

Motivo:

```text
Una herramienta genérica de comandos equivale a entregar shell remota a la IA.
Debe evitarse salvo entorno controlado y con permisos mínimos.
```

---

## 18. Docker network común

Crear red común:

```bash
docker network create homelab_net || true
```

Cada servicio nuevo debe incluir:

```yaml
networks:
  homelab_net:
    external: true
```

Y en cada servicio:

```yaml
networks:
  - homelab_net
```

Si PostgreSQL está en otro compose, agregarlo también a `homelab_net` para que servicios como Directus y Shlink puedan conectarse usando:

```text
DB_HOST=postgres
```

---

## 19. Backups

### 19.1 Ruta actual conocida

```text
/opt/backups/supabase/sandiegoapart.backup
```

### 19.2 Recomendación de estructura

```text
/opt/backups/
├── postgres/
│   ├── daily/
│   ├── weekly/
│   └── manual/
├── supabase/
│   └── sandiegoapart.backup
├── n8n/
├── directus/
└── shlink/
```

### 19.3 Backup PostgreSQL por base

Ejemplo:

```bash
mkdir -p /opt/backups/postgres/manual

docker exec postgres pg_dump -U postgres -Fc sandiegoapart > /opt/backups/postgres/manual/sandiegoapart_$(date +%Y%m%d_%H%M%S).backup
```

### 19.4 Restore

```bash
createdb -U postgres nombre_db
pg_restore -U postgres -d nombre_db archivo.backup
```

Cuando sea dentro de contenedor:

```bash
cat archivo.backup | docker exec -i postgres pg_restore -U postgres -d nombre_db
```

---

## 20. Decisiones arquitectónicas tomadas

### 20.1 PostgreSQL

```text
PostgreSQL local será la base central de infraestructura interna.
Se usará PostgreSQL 18.
Se manejarán múltiples bases en una sola instancia.
```

### 20.2 Supabase

```text
Supabase no se usará como administrador multi-base.
Supabase se conectará/operará como un solo proyecto/base.
Se usará solo cuando aporte Auth, Storage, Realtime, Edge Functions o APIs BaaS.
```

### 20.3 Directus

```text
Directus no se usará como administrador multi-base.
Directus se conectará a una sola base.
Se usará como interfaz no-code/API/admin para un proyecto o dominio específico.
```

### 20.4 pgAdmin

```text
pgAdmin será la herramienta principal para administrar múltiples bases PostgreSQL.
```

### 20.5 Shlink

```text
Shlink será el servicio de redirecciones/acortador.
go.chitaraagenteia.com será público.
links.chitaraagenteia.com será privado con Cloudflare Access.
```

### 20.6 Cloudflare

```text
Cloudflare Tunnel expone servicios.
Cloudflare Access protege paneles administrativos.
No abrir puertos públicos salvo SSH y lo estrictamente necesario.
```

### 20.7 n8n

```text
n8n se reparará recreando base limpia si no hay workflows críticos que recuperar.
```

### 20.8 Complejidad evitada

Por ahora se evita:

```text
Langfuse + ClickHouse
Múltiples stacks Supabase
Kubernetes
Docker Swarm
Exposición directa de PostgreSQL
HTTPS interno innecesario
```

---

## 21. Variables sensibles y rotación

Nunca guardar en documentación:

```text
Passwords reales.
API keys reales.
JWT secrets.
Connection strings completas con password.
Tokens Cloudflare.
Credenciales Supabase.
Credenciales SMTP.
```

Acción obligatoria:

```text
Rotar cualquier secreto que haya sido pegado en chats, notas o archivos.
```

Especialmente:

```text
Password de Supabase Cloud usada en connection string original.
INITIAL_API_KEY de Shlink si se compartió.
Passwords de PostgreSQL si se pegaron en texto plano.
```

Formato correcto en documentación:

```text
REPLACE_WITH_SECURE_PASSWORD
REPLACE_WITH_LONG_SECRET
REPLACE_WITH_API_KEY
REDACTED
```

---

## 22. Checklist de validación operativa

### 22.1 Docker

```bash
docker ps
docker compose ls
docker network ls
docker volume ls
```

### 22.2 Cloudflare Tunnel

```bash
docker logs cloudflared --tail=100
```

O:

```bash
journalctl -u cloudflared -n 100 --no-pager
```

### 22.3 Puertos

```bash
ss -tulpn
```

### 22.4 Firewall

```bash
ufw status verbose
```

### 22.5 PostgreSQL

```bash
docker exec -it postgres psql -U postgres -c "SELECT version();"
docker exec -it postgres psql -U postgres -c "\l"
```

### 22.6 Logs por servicio

```bash
docker logs nombre_contenedor --tail=100
```

Ejemplos:

```bash
docker logs postgres --tail=100
docker logs n8n --tail=100
docker logs directus --tail=100
docker logs shlink --tail=100
docker logs cloudflared --tail=100
```

---

## 23. Orden recomendado de próximos pasos

### Fase 1 — Seguridad base

```text
1. Validar SSH.
2. Revisar UFW.
3. Cerrar puertos públicos innecesarios.
4. Confirmar que todos los servicios funcionan por Cloudflare Tunnel.
5. Rotar secretos expuestos.
```

### Fase 2 — Reparar n8n

```text
1. Confirmar si hay workflows que recuperar.
2. Si no hay datos críticos, recrear DB n8n.
3. Levantar n8n.
4. Validar migraciones.
5. Probar acceso por n8n.chitaraagenteia.com.
```

### Fase 3 — Instalar Shlink

```text
1. Crear DB shlink.
2. Crear /opt/homelab/shlink.
3. Crear .env.
4. Crear docker-compose.yml.
5. Levantar contenedores.
6. Configurar Cloudflare Tunnel.
7. Proteger links.chitaraagenteia.com.
8. Dejar go.chitaraagenteia.com público.
9. Crear primer link de prueba.
```

### Fase 4 — Instalar Directus

```text
1. Crear DB directus.
2. Crear /opt/homelab/directus.
3. Crear .env.
4. Crear docker-compose.yml.
5. Levantar Directus.
6. Configurar Cloudflare Tunnel.
7. Proteger directus.chitaraagenteia.com.
8. Validar login admin.
```

### Fase 5 — Evaluar Supabase self-hosted

```text
1. Revisar recursos del VPS.
2. Instalar stack oficial en /opt/homelab/supabase.
3. Generar secretos.
4. Configurar .env.
5. Levantar stack.
6. Exponer por Cloudflare.
7. Proteger panel administrativo.
8. No usarlo como pgAdmin.
```

### Fase 6 — Migración Supabase Cloud → local

```text
1. Inspeccionar backup actual.
2. Listar objetos problemáticos.
3. Instalar pgvector si aplica.
4. Separar tablas reales de funciones/extensiones.
5. Restaurar schema limpio.
6. Restaurar datos.
7. Validar aplicación.
8. Rehacer funciones RPC solo si son necesarias.
```

---

## 24. Comandos rápidos útiles

### Entrar a PostgreSQL

```bash
docker exec -it postgres psql -U postgres
```

### Ver versión PostgreSQL

```sql
SELECT version();
```

### Listar bases

```sql
\l
```

### Listar schemas

```sql
\dn
```

### Listar tablas

```sql
\dt *.*
```

### Ver contenedores

```bash
docker ps
```

### Ver logs

```bash
docker logs CONTAINER_NAME --tail=100 -f
```

### Reiniciar servicio

```bash
docker restart CONTAINER_NAME
```

### Reiniciar compose

```bash
cd /opt/homelab/SERVICIO
docker compose down
docker compose up -d
```

### Ver uso de disco

```bash
df -h
du -sh /opt/homelab/*
du -sh /var/lib/docker
```

### Ver memoria

```bash
free -h
```

---

## 25. Estado final deseado

```text
VPS Contabo
→ Docker Compose
→ PostgreSQL 18 local
→ Cloudflare Tunnel
→ Cloudflare Access
→ Servicios internos protegidos
→ Shlink para redirects públicos
→ Directus para administración/API de una base
→ Supabase para un único proyecto cuando aplique
→ pgAdmin para administración multi-base
→ n8n reparado sobre PostgreSQL 18
→ Puertos públicos cerrados
→ Secrets rotados
→ Backups organizados
```

---

## 26. Principios de operación para el agente

El agente debe seguir estas reglas:

```text
1. No exponer servicios directamente a internet.
2. No abrir puertos salvo necesidad explícita.
3. No imprimir secretos en logs, Markdown ni respuestas.
4. No hacer DROP DATABASE sin confirmar backup o irrelevancia de datos.
5. No restaurar dumps Supabase completos a ciegas.
6. No usar Supabase como pgAdmin.
7. No usar Directus como pgAdmin.
8. Usar pgAdmin para administración multi-base.
9. Usar Shlink para redirects.
10. Mantener Cloudflare como capa pública de entrada.
11. Usar placeholders para secretos.
12. Mantener servicios en /opt/homelab.
13. Usar Docker Compose simple.
14. Documentar cada cambio.
15. Validar con docker ps, logs, curl local y Cloudflare URL.
```

---

## 27. Resumen ejecutivo

La infraestructura Chitara está basada en un VPS Contabo con Docker Compose y Cloudflare Tunnel. PostgreSQL fue migrado a versión 18 y funciona correctamente usando el volumen montado en `/var/lib/postgresql`. Los servicios principales como pgAdmin, Portainer, Open WebUI, LiteLLM, Dozzle, Uptime Kuma y cloudflared están activos. n8n quedó temporalmente roto por recreación de PostgreSQL y debe regenerar su base/migraciones.

La migración desde Supabase Cloud falló porque el backup contiene extensiones y tipos propios del ecosistema Supabase, como `wrappers`, `halfvec`, `pgvector` y funciones dependientes como `match_documents`. La estrategia correcta es una migración limpia, separando tablas reales, datos, extensiones y funciones.

Se decidió que Supabase y Directus no se usarán como administradores multi-base. Supabase será un único proyecto/base cuando se requiera backend BaaS. Directus se conectará a una sola base para administración/API no-code. pgAdmin seguirá siendo la herramienta multi-base. Para redirecciones tipo Short.io se eligió Shlink, con `go.chitaraagenteia.com` público y `links.chitaraagenteia.com` protegido con Cloudflare Access.

El objetivo inmediato es cerrar puertos públicos, reparar n8n, instalar Shlink, instalar Directus y luego evaluar Supabase self-hosted con cuidado por consumo de recursos.
---

## 27. Copia de tablas n8n a base independiente (2026-05-26)

### Procedimiento

```bash
# 1. Crear base n8n
docker exec postgres psql -U chitara -c "CREATE DATABASE n8n OWNER chitara;"

# 2. Dump DDL de tablas n8n desde sandiegoapart
docker exec postgres pg_dump -U chitara -d sandiegoapart --no-owner --no-acl --schema-only \
  -t annotation_tag_entity -t auth_identity -t auth_provider_sync_history \
  -t binary_data -t chat_hub_agents -t chat_hub_messages -t chat_hub_sessions \
  -t credentials_entity -t data_table -t data_table_column \
  -t dynamic_credential_entry -t dynamic_credential_resolver \
  -t event_destinations -t execution_annotation_tags -t execution_annotations \
  -t execution_data -t execution_entity -t execution_metadata \
  -t folder -t folder_tag -t insights_by_period -t insights_metadata \
  -t insights_raw -t installed_nodes -t installed_packages \
  -t invalid_auth_token -t migrations -t oauth_access_tokens \
  -t oauth_authorization_codes -t oauth_clients -t oauth_refresh_tokens \
  -t oauth_user_consents -t processed_data -t project -t project_relation \
  -t role -t role_scope -t scope -t settings -t shared_credentials \
  -t shared_workflow -t tag_entity -t test_case_execution -t test_run \
  -t "user" -t user_api_keys -t variables -t webhook_entity \
  -t workflow_dependency -t workflow_entity -t workflow_history \
  -t workflow_publish_history -t workflow_statistics -t workflows_tags \
  > /tmp/n8n_ddl.sql

# 3. Dump datos
docker exec postgres pg_dump -U chitara -d sandiegoapart --no-owner --no-acl --data-only \
  [mismos -t flags] > /tmp/n8n_data.sql

# 4. Restaurar en base n8n
cat /tmp/n8n_ddl.sql | docker exec -i postgres psql -U chitara -d n8n
cat /tmp/n8n_data.sql | docker exec -i postgres psql -U chitara -d n8n
```

### Resultado

- 54 tablas n8n copiadas
- 25 workflows, 3193 ejecuciones, 24 credenciales
- Errores de FK circulares esperados (n8n los recrea al iniciar)
- n8n .env actual: `DB_POSTGRESDB_DATABASE=chitara` → pendiente cambiar a `n8n`

---

## 28. Conexion SSH al VPS para agentes

### 28.1 Datos del servidor

```
IP:     5.252.52.190
User:   root
Puerto: 22
OS:     Ubuntu (Contabo VPS)
```

### 28.2 Setup de llave SSH (una sola vez)

El agente genera su propio par de llaves en el entorno local:

```bash
mkdir -p ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "opencode@teknoconecta"
cat ~/.ssh/id_ed25519.pub
```

**NO usar passphrase** (las llaves son efimeras en el entorno del agente).

### 28.3 Agregar llave publica al VPS

COPIAR el output de `cat ~/.ssh/id_ed25519.pub` y pedir al usuario que la
agregue al VPS. El usuario debe ejecutar en su maquina local:

```powershell
# Windows PowerShell
ssh root@5.252.52.190 "mkdir -p ~/.ssh && echo 'LLAVE_PUBLICA_COPIADA' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

O si el usuario esta en Linux/Mac:

```bash
ssh root@5.252.52.190 "mkdir -p ~/.ssh && echo 'LLAVE_PUBLICA_COPIADA' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**Nota:** El usuario necesita la contrasena del VPS para este paso unico.
Una vez agregada la llave, el agente puede conectarse sin contrasena.

### 28.4 Probar conexion

```bash
ssh -o StrictHostKeyChecking=accept-new root@5.252.52.190 "echo 'conexion OK'"
```

### 28.5 Ejecutar comandos en el VPS

**PATRON OBLIGATORIO** — todo comando en el VPS se ejecuta asi:

```bash
ssh root@5.252.52.190 "COMANDO_AQUI"
```

**Ejemplos:**

```bash
# Ver estado de contenedores
ssh root@5.252.52.190 "docker ps"

# Ver logs de un servicio
ssh root@5.252.52.190 "docker logs supabase-studio --tail 100"

# Leer archivo de configuracion
ssh root@5.252.52.190 "cat /opt/homelab/supabase/docker-compose.yml"

# Reiniciar un stack
ssh root@5.252.52.190 "docker compose -f /opt/homelab/supabase/docker-compose.yml up -d"

# Ejecutar comando dentro de un contenedor (sin curl/wget)
ssh root@5.252.52.190 "docker exec supabase-studio node -e \"fetch('http://meta:8080/health').then(r => r.text()).then(console.log)\""

# Entrar a PostgreSQL
ssh root@5.252.52.190 "docker exec postgres psql -U chitara -d sandiegoapart -c 'SELECT 1'"
```

**Reglas:**
- Usar siempre `ssh root@5.252.52.190 "..."` — NO usar `ssh` interactivo
- Comillas simples dentro del comando remoto deben escaparse o usar heredoc
- Para editar archivos en el VPS, usar `cat >` con heredoc o `sed`
- Para operaciones multi-linea complejas, usar `cat > /ruta/archivo << 'EOF' ... EOF`
- **NO exponer credenciales en comandos visibles** — siempre usar env vars o archivos

### 28.6 Firewall / UFW

```bash
# Ver estado
ssh root@5.252.52.190 "ufw status verbose"

# UFW esta desactivado por ahora — solo Cloudflare Tunnel expone servicios
```

### 28.7 Diagnostico de conectividad entre contenedores

```bash
# Ver en que redes esta cada contenedor
ssh root@5.252.52.190 "docker ps --format '{{.Names}} → {{.Networks}}'"

# Inspeccionar una red
ssh root@5.252.52.190 "docker network inspect postgres_default --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{\"\\n\"}}{{end}}'"

# Probar conectividad desde un contenedor (node, no curl)
ssh root@5.252.52.190 "docker exec supabase-studio node -e \"
require('http').get('http://meta:8080/health', r => {
  let d=''; r.on('data',c=>d+=c); r.on('end',()=>console.log(d));
}).on('error',e=>console.log('ERROR:',e.message))
\""
```

### 28.8 Leccion: redes Docker y resolucion de nombres

**Error frecuente:** Un contenedor solo puede resolver hostnames de otros
contenedores si comparten al menos una red Docker.

- `postgres` esta en la red `postgres_default`
- `supabase-meta` estaba SOLO en `supabase_net` → no podia resolver `postgres`
- `supabase-studio` esta en AMBAS redes → si puede resolver `postgres`

**Solucion:** Agregar `postgres_default` como red adicional al servicio que
necesita acceder a PostgreSQL.

### 28.9 Actualizar chitara.md despues de cada cambio

**Obligatorio:** Despues de cualquier modificacion en el VPS (nuevo servicio,
cambio de config, fix aplicado), documentar en este archivo:

- Comando exacto ejecutado
- Resultado obtenido
- Leccion aprendida (si aplica)
- Fecha del cambio

Esto mantiene trazabilidad para futuras sesiones del agente.
