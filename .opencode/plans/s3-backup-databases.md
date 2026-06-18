# Plan: Backups PostgreSQL + Qdrant → S3

**Estado**: Pendiente de aprobacion
**Fecha**: 2026-06-18

---

## Datos de diagnostico

| DB | Tamano | Backups locales existentes | Problemas |
|----|--------|---------------------------|-----------|
| PostgreSQL (main) | 575 MB (12 DBs) | Diario 03:00 Berlin, 7d retencion | Solo local, inconsistente (40 MB vs 350 MB) |
| PostgreSQL (coolify) | 17 MB | **NINGUNO** | Sin respaldo |
| Qdrant | 459 MB | Diario 03:30 Berlin, 7d retencion | Solo local, metodo tar podria ser fragil |

**Timezones**:
- VPS: Europe/Berlin (CEST, UTC+2)
- Chile: UTC-4 (invierno junio)
- 3 AM Chile = 9 AM Berlin

---

## Plan

### Paso 1 — Crear bucket S3 `chitara-backups`

- Nombre: `chitara-backups` (si no esta disponible, `chitara-backups-app`)
- Region: `us-east-1`
- Credenciales: mismas AKIA3YML6NV3RJER6N66
- Config: versioning ON, public access blocked, lifecycle 30d
- Estructura de carpetas:
  ```
  s3://chitara-backups/
    postgres/
      daily/    → pg_dumpall + pg_dump por DB
      weekly/   → copia del domingo
    qdrant/
      daily/    → snapshots
      weekly/   → copia del domingo
    coolify/
      daily/    → pg_dumpall de coolify-db
  ```

### Paso 2 — Instalar AWS CLI en el VPS

```bash
apt install -y awscli
```
(o usar boto3 via contenedor Python si apt falla)

### Paso 3 — Reescribir backup-postgres.sh

Archivo: `/opt/scripts/backup-postgres.sh`

```bash
#!/bin/bash
set -euo pipefail
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DAY=$(date +"%Y%m%d")
DOW=$(date +"%u")  # 1=Mon, 7=Sun
BACKUP_DIR="/opt/backups/postgres"
S3_BUCKET="chitara-backups"
S3_PREFIX="postgres/daily"
LOG_FILE="/var/log/backup-postgres.log"
MIN_SIZE_MB=50

# Funciones de log
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }
alert() { log "ALERT: $1"; }

log "=== Iniciando backup PostgreSQL ==="

# 1. pg_dumpall completo (todas las DBs)
log "Ejecutando pg_dumpall..."
docker exec postgres pg_dumpall -U chitara | gzip > "$BACKUP_DIR/postgres_${TIMESTAMP}.sql.gz"

SIZE=$(stat -c%s "$BACKUP_DIR/postgres_${TIMESTAMP}.sql.gz")
log "pg_dumpall: $SIZE bytes"

if [ "$SIZE" -lt $((MIN_SIZE_MB * 1024 * 1024)) ]; then
    alert "pg_dumpall sospechosamente pequeno: $(du -h "$BACKUP_DIR/postgres_${TIMESTAMP}.sql.gz" | cut -f1)"
fi

# 2. pg_dump por base de datos individual
DBS=$(docker exec postgres psql -U chitara -t -c "SELECT datname FROM pg_database WHERE datistemplate = false AND datname != 'postgres'")
mkdir -p "$BACKUP_DIR/databases/$DAY"
for DB in $DBS; do
    DB_CLEAN=$(echo $DB | tr -d ' ')
    log "  Backup $DB_CLEAN..."
    docker exec postgres pg_dump -U chitara --no-owner --no-acl -d "$DB_CLEAN" | gzip > "$BACKUP_DIR/databases/$DAY/${DB_CLEAN}.sql.gz"
done

# 3. Backup coolify-db
log "Backup coolify-db..."
docker exec coolify-db pg_dumpall -U coolify | gzip > "$BACKUP_DIR/coolify_${TIMESTAMP}.sql.gz"

# 4. Verificar integridad
log "Verificando integridad..."
for f in "$BACKUP_DIR/postgres_${TIMESTAMP}.sql.gz" "$BACKUP_DIR/coolify_${TIMESTAMP}.sql.gz"; do
    if ! gzip -t "$f"; then
        alert "ARCHIVO CORRUPTO: $f"
    fi
done

# 5. Upload a S3
log "Subiendo a S3..."
aws s3 cp "$BACKUP_DIR/postgres_${TIMESTAMP}.sql.gz" "s3://${S3_BUCKET}/${S3_PREFIX}/postgres_${TIMESTAMP}.sql.gz" --no-progress
aws s3 cp "$BACKUP_DIR/coolify_${TIMESTAMP}.sql.gz" "s3://${S3_BUCKET}/coolify/daily/coolify_${TIMESTAMP}.sql.gz" --no-progress
aws s3 sync "$BACKUP_DIR/databases/$DAY" "s3://${S3_BUCKET}/postgres/databases/$DAY/" --no-progress

RESULT=$?
if [ $RESULT -eq 0 ]; then
    log "Upload S3 exitoso"
else
    alert "Fallo upload S3 (exit code: $RESULT)"
fi

# 6. Backup semanal (domingo = 7)
if [ "$DOW" == "7" ]; then
    log "Creando backup semanal..."
    aws s3 cp "s3://${S3_BUCKET}/${S3_PREFIX}/postgres_${TIMESTAMP}.sql.gz" "s3://${S3_BUCKET}/postgres/weekly/postgres_${TIMESTAMP}.sql.gz" --no-progress
    aws s3 cp "s3://${S3_BUCKET}/coolify/daily/coolify_${TIMESTAMP}.sql.gz" "s3://${S3_BUCKET}/coolify/weekly/coolify_${TIMESTAMP}.sql.gz" --no-progress
fi

# 7. Rotacion local (7 dias)
find "$BACKUP_DIR" -name "postgres_*.sql.gz" -type f -mtime +7 -delete
find "$BACKUP_DIR/databases" -type d -mtime +7 -exec rm -rf {} \;
find "$BACKUP_DIR" -name "coolify_*.sql.gz" -type f -mtime +7 -delete

log "=== Backup PostgreSQL completado ==="
```

### Paso 4 — Reescribir backup-qdrant.sh

Archivo: `/opt/scripts/backup-qdrant.sh`

```bash
#!/bin/bash
set -euo pipefail
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DOW=$(date +"%u")
BACKUP_DIR="/opt/backups/qdrant"
S3_BUCKET="chitara-backups"
QDRANT_API_KEY="Y_LURdGX9YrqRPMw_pTUZ0-XaKiKzSfACxx01h8Ha7o6YTuYQjQ_pCjODNHwCPJ3"
QDRANT_URL="http://localhost:6333"
COLLECTION="system_procesadoc_openai_3072"
LOG_FILE="/var/log/backup-qdrant.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }
alert() { log "ALERT: $1"; }

log "=== Iniciando backup Qdrant ==="

# 1. Crear snapshot via API
log "Creando snapshot de '$COLLECTION'..."
SNAPSHOT_RESPONSE=$(curl -s -X POST \
    -H "api-key: $QDRANT_API_KEY" \
    "$QDRANT_URL/collections/$COLLECTION/snapshots")

SNAPSHOT_NAME=$(echo "$SNAPSHOT_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['name'])")
log "Snapshot creado: $SNAPSHOT_NAME"

# 2. Esperar a que el snapshot este listo (max 60s)
for i in $(seq 1 12); do
    STATUS=$(curl -s \
        -H "api-key: $QDRANT_API_KEY" \
        "$QDRANT_URL/collections/$COLLECTION/snapshots/$SNAPSHOT_NAME" | \
        python3 -c "import sys,json; print(json.load(sys.stdin)['result']['status'])")
    if [ "$STATUS" == "ready" ]; then
        break
    fi
    log "Esperando snapshot... ($i/12)"
    sleep 5
done

# 3. Descargar snapshot
mkdir -p "$BACKUP_DIR/$TIMESTAMP"
SNAPSHOT_FILE="$BACKUP_DIR/$TIMESTAMP/qdrant_${COLLECTION}_${TIMESTAMP}.snapshot"
curl -s -o "$SNAPSHOT_FILE" \
    -H "api-key: $QDRANT_API_KEY" \
    "$QDRANT_URL/collections/$COLLECTION/snapshots/$SNAPSHOT_NAME/download"

SIZE=$(stat -c%s "$SNAPSHOT_FILE")
log "Snapshot descargado: $SIZE bytes"

# 4. Upload a S3
log "Subiendo a S3..."
aws s3 cp "$SNAPSHOT_FILE" "s3://${S3_BUCKET}/qdrant/daily/qdrant_${COLLECTION}_${TIMESTAMP}.snapshot" --no-progress

RESULT=$?
if [ $RESULT -eq 0 ]; then
    log "Upload S3 exitoso"
else
    alert "Fallo upload S3 (exit code: $RESULT)"
fi

# 5. Backup semanal
if [ "$DOW" == "7" ]; then
    aws s3 cp "s3://${S3_BUCKET}/qdrant/daily/qdrant_${COLLECTION}_${TIMESTAMP}.snapshot" \
              "s3://${S3_BUCKET}/qdrant/weekly/qdrant_${COLLECTION}_${TIMESTAMP}.snapshot" --no-progress
fi

# 6. Rotacion local (7 dias)
find "$BACKUP_DIR" -type d -name "20*" -mtime +7 -exec rm -rf {} \;

log "=== Backup Qdrant completado ==="
```

### Paso 5 — Configurar S3 Lifecycle

Via script Python o AWS CLI:
```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket chitara-backups \
    --lifecycle-configuration '{
        "Rules": [{
            "Id": "expire-old-backups",
            "Status": "Enabled",
            "Expiration": { "Days": 30 },
            "Filter": { "Prefix": "" }
        }]
    }'
```

### Paso 6 — Actualizar cron

```cron
# 3 AM Chile (UTC-4 invierno) = 9 AM Berlin (CEST)
0 9 * * * /opt/scripts/backup-postgres.sh >> /var/log/backup-postgres-cron.log 2>&1
30 9 * * * /opt/scripts/backup-qdrant.sh >> /var/log/backup-qdrant-cron.log 2>&1
```

Los backups de las 03:00/03:30 Berlin actuales se mantienen o se reemplazan.

### Paso 7 — Verificar

- Ejecutar backup manualmente, verificar que los archivos aparecen en S3
- Verificar que los tamaños son coherentes
- Simular restore: descargar un .sql.gz y verificar `gzip -t`

---

## Riesgos

| Riesgo | Mitigacion |
|--------|-----------|
| AWS CLI falla al instalar | Usar boto3 via contenedor Python (ya comprobado que funciona) |
| pg_dumpall inconsistente | Alerta si < 50 MB, log detallado |
| Qdrant snapshot demasiado grande para RAM | Monitorear tamano; si crece mucho, descargar por streaming |
| Credenciales expuestas en scripts | Los scripts están en VPS (no repo); mismo patron que el .env actual |

## Que NO cambia

- Backups locales en `/opt/backups/` se mantienen (7 dias)
- Volumenes Docker intactos
- Cron existente de las 03:00/03:30 Berlin se reemplaza por 09:00/09:30

## Rollback

Si algo falla:
1. Restaurar cron anterior (`0 3 * * *` y `30 3 * * *`)
2. Eliminar bucket `chitara-backups`
3. Los backups locales nunca se dejaron de generar
