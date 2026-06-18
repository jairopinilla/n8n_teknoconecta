#!/bin/bash
# backup_snapshot.sh — Crear snapshot de colecciones Qdrant via API REST.
#
# Uso:
#   bash backup_snapshot.sh
#
# Requiere:
#   - QDRANT_API_KEY seteado en entorno
#   - curl
#   - Qdrant accesible en QDRANT_HOST:QDRANT_REST_PORT

set -euo pipefail

HOST="${QDRANT_HOST:-localhost}"
PORT="${QDRANT_REST_PORT:-6333}"
API_KEY="${QDRANT_API_KEY:-}"
BACKUP_DIR="${QDRANT_BACKUP_DIR:-./snapshots}"

if [ -z "$API_KEY" ]; then
    echo "❌ ERROR: QDRANT_API_KEY no está seteado."
    exit 1
fi

mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
echo "📦 Qdrant Backup — $TIMESTAMP"
echo "   Host: $HOST:$PORT"
echo "   Destino: $BACKUP_DIR"
echo ""

# Listar colecciones
COLLECTIONS=$(curl -s -H "api-key: $API_KEY" "http://${HOST}:${PORT}/collections" | python3 -c "import sys,json; print(' '.join([c['name'] for c in json.load(sys.stdin)['result']['collections']]))" 2>/dev/null)

if [ -z "$COLLECTIONS" ]; then
    echo "⚠️  No se encontraron colecciones. Nada que respaldar."
    exit 0
fi

for col in $COLLECTIONS; do
    echo "📸 Snapshot de '$col'..."

    # Crear snapshot
    RESP=$(curl -s -X POST -H "api-key: $API_KEY" "http://${HOST}:${PORT}/collections/${col}/snapshots")
    echo "   $RESP"

    # Esperar y descargar (Qdrant expone snapshots como archivos)
    SNAP_FILE="${BACKUP_DIR}/${col}_${TIMESTAMP}.snapshot"
    curl -s -H "api-key: $API_KEY" "http://${HOST}:${PORT}/collections/${col}/snapshots" \
        -o "${SNAP_FILE}.json"

    echo "   ✅ Metadata guardada en ${SNAP_FILE}.json"
done

echo ""
echo "🎉 Backup completado. Archivos en $BACKUP_DIR/"
ls -lh "$BACKUP_DIR/"
