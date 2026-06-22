# Neo4j en Chitara — Multi-instancia

## Servidores Neo4j disponibles (Docker)

Cada sistema tiene su propio contenedor Neo4j independiente, con su propia base de datos, puerto y volumen.

| Contenedor | Sistema | HTTP Browser | Bolt (driver) | Volumen |
|-----------|---------|-------------|---------------|---------|
| `neo4j` | General / default | `7474` | `7687` | `neo4j_data` |
| `neo4j-procesadoc` | Procesa_doc | `7475` | `7688` | `neo4j_procesadoc_data` |
| `neo4j-topicsystem` | Topic System | `7476` | `7689` | `neo4j_topicsystem_data` |

## Credenciales (igual para todos)

| Campo | Valor |
|-------|-------|
| **Usuario** | `neo4j` |
| **Password** | `flacavonoteni30` |

## Conexión desde dentro del VPS (misma red Docker `coolify`)

Todos los contenedores están en la red `coolify`. Se accede por **nombre de contenedor**:

### Python (neo4j driver)

```python
from neo4j import GraphDatabase

# Procesa_doc
driver = GraphDatabase.driver("bolt://neo4j-procesadoc:7687", auth=("neo4j", "flacavonoteni30"))

# Topic System
driver = GraphDatabase.driver("bolt://neo4j-topicsystem:7687", auth=("neo4j", "flacavonoteni30"))

# General
driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "flacavonoteni30"))
```

### JavaScript/TypeScript (neo4j-driver)

```ts
import neo4j from 'neo4j-driver'

const driver = neo4j.driver(
  "bolt://neo4j-procesadoc:7687",
  neo4j.auth.basic("neo4j", "flacavonoteni30")
)
```

### Conexión desde el host VPS (localhost + puerto)

```python
# Procesa_doc → bolt://127.0.0.1:7688
# Topic System → bolt://127.0.0.1:7689
# General      → bolt://127.0.0.1:7687
```

## Neo4j Browser (interfaz web)

| URL | Contenedor |
|-----|-----------|
| `https://neo4j.chitaraagenteia.com` | `neo4j` (general) |

Para acceder a los otros desde el mismo Browser, usar `:server disconnect` y conectar a `bolt://127.0.0.1:7688` (procesadoc) o `bolt://127.0.0.1:7689` (topicsystem) desde la pestaña de conexión.

Credenciales: `neo4j` / `flacavonoteni30`

## Agregar un nuevo sistema

Agregar al `docker-compose.yml` en `/opt/homelab/neo4j/`:

```yaml
  neo4j-nuevo:
    image: neo4j:5-community
    container_name: neo4j-nuevo
    restart: unless-stopped
    environment:
      - NEO4J_AUTH=neo4j/flacavonoteni30
      - NEO4J_server_memory_heap_max__size=1G
    ports:
      - 127.0.0.1:7477:7474
      - 127.0.0.1:7690:7687
    volumes:
      - neo4j_nuevo_data:/data
    networks:
      - coolify
```

Y declarar el volumen `neo4j_nuevo_data:` en la sección `volumes:`.

Luego:
```bash
cd /opt/homelab/neo4j && docker compose up -d
```

## Recursos

| Contenedor | RAM heap |
|-----------|---------|
| `neo4j` (general) | 2 GB |
| `neo4j-procesadoc` | 1 GB |
| `neo4j-topicsystem` | 1 GB |
| **Total** | 4 GB (de 47 GB disponibles) |

## Notas operativas

- Neo4j Community 5.x no soporta `CREATE DATABASE` vía Cypher — por eso usamos contenedores separados.
- Cada contenedor expone solo en `127.0.0.1` (no accesible desde internet directamente).
- El acceso web es solo vía Cloudflare Tunnel en `https://neo4j.chitaraagenteia.com`.
- Los volúmenes son persistentes: los datos sobreviven reinicios del contenedor.
- El compose está en `/opt/homelab/neo4j/docker-compose.yml`.
