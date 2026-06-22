# Procesa_doc — Graphify

## Ultima ejecucion

- Fecha: 2026-06-19
- VPS: `5.252.52.190`
- Contenedor usado: `rag-api`
- Workspace: `caso-audios`
- GraphML origen: `/opt/homelab/rag/data/lightrag/procesadoc/caso-audios/graph_chunk_entity_relation.graphml`
- Output JSON: `/opt/homelab/rag/data/graphify/procesadoc/caso-audios/graph.json`
- Output reporte: `/opt/homelab/rag/data/graphify/procesadoc/caso-audios/GRAPH_REPORT.md`
- Resultado: 540 nodos, 611 aristas

## Comando ejecutado

```bash
docker exec rag-api sh -lc 'cd /app && DATA_DIR=/data python -m app.cli build-graphify --workspace-id caso-audios'
```

## Verificacion

```bash
ls -lh /opt/homelab/rag/data/graphify/procesadoc/caso-audios/
sed -n '1,40p' /opt/homelab/rag/data/graphify/procesadoc/caso-audios/GRAPH_REPORT.md
```

## Notas

- El comando debe ejecutarse dentro de `rag-api` porque ahi ya estan el codigo, dependencias y el volumen `/data` montado.
- Si falta el GraphML, primero hay que correr la ingesta/LightRAG del workspace.
- El front de Procesa_doc no parece consumir automaticamente `data/graphify/procesadoc/<workspace>/graph.json` todavia. No se encontro referencia a `graphify` o `graph.json` en `apps/web` ni en rutas del RAG API.
- Para otros workspaces, cambiar `--workspace-id caso-audios` por el workspace correspondiente.
