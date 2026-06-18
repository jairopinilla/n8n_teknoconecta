# Restauración de snapshots Qdrant

## Requisitos

- Qdrant corriendo con API key configurada
- Snapshots descargados (ver `backup_snapshot.sh`)
- `curl`

## Procedimiento

### 1. Verificar que la colección existe

```bash
curl -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections/<nombre>
```

Si no existe, crearla con los mismos parámetros (dim, distance).

### 2. Subir snapshot

Qdrant expone un endpoint para restaurar desde archivo snapshot:

```bash
curl -X PUT \
  -H "api-key: $QDRANT_API_KEY" \
  -F "snapshot=@./snapshots/system_topic_bge_m3_1024_20260616_120000.snapshot" \
  "http://localhost:6333/collections/system_topic_bge_m3_1024/snapshots/recover"
```

### 3. Verificar restauración

```bash
curl -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections/system_topic_bge_m3_1024
```

### 4. Recrear índices de payload

Después de restaurar, los índices de payload deben recrearse:

```bash
python init_collections.py \
  --host localhost --port 6333 \
  --api-key $QDRANT_API_KEY \
  --collection system_topic_bge_m3_1024 \
  --dim 1024
```

El script es idempotente: si la colección ya existe, solo crea los índices faltantes.

## Alternativa: backup del volumen Docker

Si los snapshots vía API no son suficientes, se puede respaldar el volumen directamente:

```bash
# En el VPS
docker run --rm -v qdrant_qdrant_storage:/data -v $(pwd):/backup alpine tar czf /backup/qdrant_volume_backup.tar.gz -C /data .
```

Para restaurar:

```bash
docker run --rm -v qdrant_qdrant_storage:/data -v $(pwd):/backup alpine tar xzf /backup/qdrant_volume_backup.tar.gz -C /data
docker restart qdrant
```
