# Qdrant — Base vectorial compartida

## ¿Qué es?

Qdrant es una base de datos vectorial que corre en el VPS chitara como servicio
de infraestructura compartido. **No pertenece a ningún sistema específico.**
Múltiples sistemas (topic_system, chitara, sandiegoapart) lo usan como backend
de búsqueda semántica.

## Jerarquía de datos

```
Sistema → Collection (system_{slug}_{model}_{dim})
  └── Workspace → Filtro por payload (workspace_id)
       └── Documento → Referencia por payload (document_id)
            └── Chunk → Vector + payload mínimo
```

## Decisiones de arquitectura

| Decisión | Razón |
|----------|-------|
| 1 colección por sistema × modelo | Escalabilidad. Qdrant maneja millones de puntos. Filtro por payload aísla workspaces sin overhead de colecciones. |
| Workspace aislado por payload, no por colección | Evita explosión de colecciones. Si un cliente requiere aislamiento físico, se puede crear colección dedicada como excepción. |
| Payload mínimo | Qdrant solo almacena vectores, IDs canónicos y metadata de búsqueda. PostgreSQL es fuente de verdad para usuarios, documentos, permisos, billing. |
| API key obligatoria | Aunque Qdrant solo escucha en 127.0.0.1, la API key evita que cualquier proceso en el host acceda sin autorización. |
| Backend impone workspace_id | El LLM/cliente NUNCA construye el filtro de workspace. El backend lo inyecta desde JWT/token. |

## Cómo levantarlo

```bash
ssh root@5.252.52.190
cd /opt/homelab/qdrant
docker compose up -d
```

## Cómo configurar .env

```bash
# /opt/homelab/qdrant/.env
QDRANT__SERVICE__API_KEY=<api-key>
```

## Healthcheck

```bash
# Local
curl -H 'api-key: <key>' http://127.0.0.1:6333/readyz

# Desde otro contenedor en red coolify
curl -H 'api-key: <key>' http://qdrant:6333/readyz
```

## Cómo inicializar colecciones

Cada sistema ejecuta `init_collections.py` desde su propio repo con sus parámetros:

```bash
python infra/qdrant/init_collections.py \
  --host qdrant \
  --port 6333 \
  --api-key $QDRANT_API_KEY \
  --collection system_topic_bge_m3_1024 \
  --dim 1024
```

## Cómo ejecutar smoke test

```bash
python infra/qdrant/smoke_test.py \
  --host localhost \
  --port 6333 \
  --api-key $QDRANT_API_KEY
```

## Backup / Snapshot

```bash
bash infra/qdrant/backup_snapshot.sh
```

## Restauración

Ver [restore_snapshot.md](restore_snapshot.md).

## Crear una colección nueva

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="qdrant", port=6333, api_key="<key>")
client.create_collection(
    collection_name="system_nuevo_bge_m3_1024",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)
```

## Seguridad

| Regla | Estado |
|-------|--------|
| No exponer Qdrant a internet | ✅ 127.0.0.1 |
| API key obligatoria | ✅ |
| No llamar Qdrant desde frontend | ✅ |
| No buscar sin filtro workspace_id | ⚠️ Responsabilidad del backend |
| No almacenar documentos completos en payload | ⚠️ Responsabilidad del backend |
| No guardar secretos en el repo | ✅ `.env` en VPS, no en git |

## Qué NO hacer

- No exponer Qdrant a internet
- No llamar Qdrant desde frontend
- No dejar Qdrant sin API key
- No buscar sin filtro workspace_id
- No almacenar documentos completos en payload
- No guardar secretos en el repo
- No crear colección por workspace
- No permitir búsquedas cross-workspace
