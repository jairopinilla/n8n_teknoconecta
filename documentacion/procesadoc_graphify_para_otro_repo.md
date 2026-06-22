# Procesa_doc - Graphify listo en entorno real

Este documento resume lo que ya se ejecutó en el VPS y lo que el repo `Procesa_doc` debe documentar o conectar en el front si quiere mostrar el grafo.

## Estado actual

Graphify ya fue ejecutado correctamente en el entorno real usando el contenedor `rag-api`.

Workspace usado:

```text
caso-audios
```

GraphML de origen:

```text
/opt/homelab/rag/data/lightrag/procesadoc/caso-audios/graph_chunk_entity_relation.graphml
```

Comando ejecutado:

```bash
docker exec rag-api sh -lc 'cd /app && DATA_DIR=/data python -m app.cli build-graphify --workspace-id caso-audios'
```

Resultado:

```text
Graphify built for caso-audios: 540 nodes, 611 edges
JSON: /data/graphify/procesadoc/caso-audios/graph.json
Report: /data/graphify/procesadoc/caso-audios/GRAPH_REPORT.md
```

Rutas reales en el VPS:

```text
/opt/homelab/rag/data/graphify/procesadoc/caso-audios/graph.json
/opt/homelab/rag/data/graphify/procesadoc/caso-audios/GRAPH_REPORT.md
```

## Verificación realizada

Se validó que los archivos existen y tienen contenido.

```bash
ls -lh /opt/homelab/rag/data/graphify/procesadoc/caso-audios/
sed -n '1,40p' /opt/homelab/rag/data/graphify/procesadoc/caso-audios/GRAPH_REPORT.md
```

Resumen verificado:

```text
graph.json       581 KB
GRAPH_REPORT.md 984 B
Nodes: 540
Edges: 611
```

Top entities detectadas en el reporte:

```text
Servicio de Impuestos Internos
Banco Security
Santiago
Chile
Scotiabank Chile
Banco de Chile
Banco de Crédito e Inversiones
Comisión para el Mercado Financiero
Contraloría General de la República
Daniel Amir Sauer Adlerstein
```

## Importante para el repo Procesa_doc

El backend/RAG ya genera el grafo correctamente desde el GraphML de LightRAG.

Lo que falta, si se quiere ver el grafo en la app web, es conectar el front o un endpoint a este archivo:

```text
/data/graphify/procesadoc/<workspace-id>/graph.json
```

Para `caso-audios`, el path real dentro del contenedor `rag-api` es:

```text
/data/graphify/procesadoc/caso-audios/graph.json
```

Y en el host VPS:

```text
/opt/homelab/rag/data/graphify/procesadoc/caso-audios/graph.json
```

## Recomendación de implementación

Agregar en el backend un endpoint de lectura, por ejemplo:

```text
GET /api/workspaces/:workspaceId/graphify
```

Ese endpoint debería:

1. Recibir `workspaceId`.
2. Leer `/data/graphify/procesadoc/{workspaceId}/graph.json`.
3. Si no existe, devolver `404` con mensaje claro: `Graphify output not found`.
4. Si existe, devolver el JSON tal cual.

Ejemplo de respuesta esperada:

```json
{
  "nodes": [],
  "edges": []
}
```

También conviene agregar otro endpoint opcional para el reporte:

```text
GET /api/workspaces/:workspaceId/graphify/report
```

Que devuelva el contenido de:

```text
/data/graphify/procesadoc/{workspaceId}/GRAPH_REPORT.md
```

## Comando reusable para regenerar

Para regenerar el grafo de `caso-audios`:

```bash
docker exec rag-api sh -lc 'cd /app && DATA_DIR=/data python -m app.cli build-graphify --workspace-id caso-audios'
```

Para otro workspace:

```bash
docker exec rag-api sh -lc 'cd /app && DATA_DIR=/data python -m app.cli build-graphify --workspace-id <workspace-id>'
```

Antes de correrlo, verificar que exista:

```text
/opt/homelab/rag/data/lightrag/procesadoc/<workspace-id>/graph_chunk_entity_relation.graphml
```

Si ese GraphML no existe, primero hay que correr la ingesta o generación LightRAG del workspace.

## Nota operativa

El comando debe ejecutarse dentro del contenedor `rag-api`, no directamente en el host, porque ahí están:

- el código Python correcto,
- las dependencias,
- el montaje `/data`,
- la configuración real de `DATA_DIR`.

## Estado final

Graphify ya está listo para `caso-audios`.

Pendiente para el repo `Procesa_doc`:

1. Documentar este flujo en su runbook interno.
2. Agregar endpoint o integración web para consumir `graph.json`.
3. Validar en el front que el grafo renderice los 540 nodos y 611 aristas generados.
