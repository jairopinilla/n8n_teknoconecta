# Setup Completo: Entorno de Desarrollo test_viral

> Este documento contiene TODO lo necesario para configurar el entorno de desarrollo del proyecto test_viral con OpenCode en Windows (sin WSL).
> Incluye: 5 servidores MCP, base de datos, credenciales, y archivos fuente completos.
> **IMPORTANTE:** Este archivo contiene credenciales sensibles. NO commitear a repositorios públicos.

---

## 🔧 Prerequisitos

Instalar en este orden desde PowerShell (como administrador):

```powershell
# 1. Node.js 18+ — descargar de https://nodejs.org (LTS recomendado)
node --version   # debe ser >= 18

# 2. Python 3.10+ — descargar de https://python.org
#    IMPORTANTE: marcar "Add Python to PATH" durante instalación
python --version  # debe ser >= 3.10

# 3. uv (gestor de paquetes Python rápido)
pip install uv

# 4. Verificar OpenSSH (viene con Windows 10+)
ssh -V

# 5. Generar SSH key para acceso al VPS
ssh-keygen -t ed25519 -f %USERPROFILE%\.ssh\id_ed25519 -N "" -C "testviral@dev"

# 6. Mostrar la clave pública — ENVIAR AL ADMINISTRADOR DEL VPS (Jairo)
type %USERPROFILE%\.ssh\id_ed25519.pub
```

> **IMPORTANTE:** Envía tu clave pública SSH a Jairo. Sin esto, el MCP de base de datos no funcionará.
> El VPS es `5.252.52.190` y tu key debe ser autorizada en `/root/.ssh/authorized_keys`.

---

## 📁 Estructura de archivos a crear en tu repo

```
test_viral/
├── mcp-servers/
│   ├── test-viral-db/
│   │   └── server.py
│   └── openalex/
│       ├── server.py
│       ├── data_objects.py
│       └── requirements.txt
├── opencode.jsonc
├── AGENTS.md
└── .gitignore
```

---

## 📄 Archivo: `opencode.jsonc`

Crear en la **raíz del repo**. Reemplazar `RUTA_REPO` con la ruta absoluta de tu repo.
Ejemplo: `C:\\Users\\TU_USUARIO\\Documents\\GitHub\\test_viral`

```jsonc
{
  "mcpServers": {
    // ═══════════════════════════════════════════
    // COOLIFY — Deploy y gestión de apps
    // SOLO operar sobre el proyecto test_viral
    // Project UUID: xon44yki7zp63j5v4d54r5rk
    // App UUID: f8kxqoahu0hwlwimhktgjp7t
    // ═══════════════════════════════════════════
    "coolify-mcp": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "coolify-mcp-server"
      ],
      "environment": {
        "COOLIFY_API_URL": "https://coolify.chitaraagenteia.com",
        "COOLIFY_API_TOKEN": "1|GP1qcJjN3Hyi9HmEvyPDfXAoLp0LomhB1Bgul5DEaf517cae"
      }
    },

    // ═══════════════════════════════════════════
    // BASE DE DATOS — PostgreSQL test_viral via SSH
    // ═══════════════════════════════════════════
    "test-viral-db": {
      "type": "local",
      "command": [
        "uv",
        "run",
        "--directory",
        "RUTA_REPO",
        "./mcp-servers/test-viral-db/server.py"
      ],
      "environment": {
        "TV_SSH_HOST": "5.252.52.190",
        "TV_SSH_USER": "root",
        "TV_DB_USER": "testviral_app",
        "TV_DB_PASS": "TestViral2026!",
        "TV_DB_NAME": "test_viral"
      }
    },

    // ═══════════════════════════════════════════
    // JINA — Búsqueda web, lectura URLs, clasificación
    // ═══════════════════════════════════════════
    "jina": {
      "type": "remote",
      "url": "https://mcp.jina.ai/v1",
      "headers": {
        "Authorization": "Bearer jina_83c362354d4347659eb9544c08c247a9_UWJyp2BtQG5BLdZTDE8m64iUYOh"
      }
    },

    // ═══════════════════════════════════════════
    // TAVILY — Búsqueda web con IA
    // ═══════════════════════════════════════════
    "tavily": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "tavily-mcp"
      ],
      "environment": {
        "TAVILY_API_KEY": "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"
      }
    },

    // ═══════════════════════════════════════════
    // OPENALEX — Búsqueda académica, papers, autores
    // ═══════════════════════════════════════════
    "openalex": {
      "type": "local",
      "command": [
        "uv",
        "run",
        "--directory",
        "RUTA_REPO",
        "./mcp-servers/openalex/server.py"
      ],
      "environment": {
        "OPENALEX_MAILTO": "contacto@teknoconecta.com"
      }
    }
  }
}
```

---

## 📄 Archivo: `AGENTS.md`

```markdown
# AGENTS.md — test_viral

## 🔴 REGLA COOLIFY: SOLO PROYECTO test_viral

El token de Coolify da acceso a TODOS los proyectos del servidor.
Este repo SOLO tiene autorización para operar sobre:

- **Proyecto:** test_viral
- **Project UUID:** xon44yki7zp63j5v4d54r5rk
- **App UUID:** f8kxqoahu0hwlwimhktgjp7t
- **Dominio:** https://test.chitaraagenteia.com
- **Puerto interno:** 3000 → 4284

NUNCA listar, modificar, eliminar o deployar otros proyectos.

## 🗄️ Base de datos

- **DB:** test_viral (PostgreSQL 16 en VPS 5.252.52.190)
- **User:** testviral_app / TestViral2026!
- **Acceso:** via SSH tunnel (MCP test-viral-db)
- **Convención:** PascalCase estricto (ver sección abajo)

## 🔐 Seguridad

- `opencode.jsonc` DEBE estar en `.gitignore`
- NUNCA commitear credenciales en texto plano
- NUNCA operar sobre proyectos ajenos en Coolify

## MCPs disponibles

| MCP | Uso | Tipo |
|-----|-----|------|
| coolify-mcp | Deploy y gestión de la app (SOLO test_viral) | Node.js (npx) |
| test-viral-db | SQL directo sobre la base de datos test_viral | Python (SSH) |
| jina | Búsqueda web, lectura URLs, clasificación, reranking | Remote HTTP |
| tavily | Búsqueda web con IA | Node.js (npx) |
| openalex | Búsqueda académica, papers, autores, PubMed, ORCID | Python |
```

---

## 📄 Archivo: `.gitignore` (agregar estas líneas)

```
opencode.jsonc
.env
*.enc
node_modules/
__pycache__/
.venv/
```

---

## 📄 Archivo: `mcp-servers/test-viral-db/server.py`

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.0.0"]
# ///
"""MCP server for test_viral — PostgreSQL en VPS chitara via SSH."""

import json
import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SSH_HOST = os.environ.get("TV_SSH_HOST", "5.252.52.190")
SSH_USER = os.environ.get("TV_SSH_USER", "root")
DB_USER = os.environ.get("TV_DB_USER", "testviral_app")
DB_PASS = os.environ.get("TV_DB_PASS", "TestViral2026!")
DB_NAME = os.environ.get("TV_DB_NAME", "test_viral")

def _ssh_exec(cmd: str) -> dict:
    safe_cmd = cmd.replace("'", "'\\''")
    ssh = f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 {SSH_USER}@{SSH_HOST} '{safe_cmd}'"
    try:
        r = subprocess.run(ssh, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": r.stdout, "stderr": r.stderr, "rc": r.returncode}
    except Exception as e:
        return {"error": str(e)}

def _psql(sql: str) -> dict:
    sql_escaped = sql.replace("'", "'\\''")
    return _ssh_exec(f"docker exec postgres psql -U {DB_USER} -d {DB_NAME} -c '{sql_escaped}'")

def _psql_json(sql: str) -> list:
    sql_escaped = sql.replace("'", "'\\''")
    r = _ssh_exec(f"docker exec postgres psql -U {DB_USER} -d {DB_NAME} -t -A -c '{sql_escaped}'")
    rows = []
    for line in r.get("stdout", "").strip().split("\n"):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except:
                rows.append(line)
    return rows

server = Server("test-viral-db")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="tv_list_schemas", description="List all schemas in test_viral DB.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="tv_list_tables", description="List tables in a schema.", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}}, "required": []}),
        Tool(name="tv_get_table", description="Get table structure (columns, types, constraints).", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}, "table": {"type": "string"}}, "required": ["table"]}),
        Tool(name="tv_exec_sql", description="Execute SQL on test_viral. Full read-write.", inputSchema={"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]}),
        Tool(name="tv_list_extensions", description="List PostgreSQL extensions.", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="tv_list_functions", description="List stored functions in a schema.", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}}, "required": []}),
        Tool(name="tv_get_indexes", description="Get indexes for a table.", inputSchema={"type": "object", "properties": {"schema": {"type": "string", "default": "public"}, "table": {"type": "string"}}, "required": ["table"]}),
        Tool(name="tv_server_info", description="Get DB stats and server info.", inputSchema={"type": "object", "properties": {}, "required": []}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "tv_list_schemas":
            rows = _psql_json("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT LIKE 'pg_%' AND schema_name NOT IN ('information_schema','extensions') ORDER BY schema_name")
            result = json.dumps(rows, indent=2)
        elif name == "tv_list_tables":
            schema = arguments.get("schema", "public")
            rows = _psql_json(f"SELECT json_build_object('schema',table_schema,'table',table_name,'type',table_type) FROM information_schema.tables WHERE table_schema='{schema}' ORDER BY table_name")
            result = json.dumps(rows, indent=2)
        elif name == "tv_get_table":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            rows = _psql_json(f"SELECT json_build_object('column',c.column_name,'type',c.data_type,'nullable',c.is_nullable,'default',c.column_default,'pk',CASE WHEN pk.constraint_type='PRIMARY KEY' THEN true ELSE false END) FROM information_schema.columns c LEFT JOIN (SELECT ku.table_schema,ku.table_name,ku.column_name,tc.constraint_type FROM information_schema.key_column_usage ku JOIN information_schema.table_constraints tc ON ku.constraint_name=tc.constraint_name AND ku.table_schema=tc.table_schema WHERE tc.constraint_type='PRIMARY KEY') pk ON c.table_schema=pk.table_schema AND c.table_name=pk.table_name AND c.column_name=pk.column_name WHERE c.table_schema='{schema}' AND c.table_name='{table}' ORDER BY c.ordinal_position")
            result = json.dumps(rows, indent=2)
        elif name == "tv_exec_sql":
            r = _psql(arguments["sql"])
            result = r.get("stdout", r.get("error", ""))
        elif name == "tv_list_extensions":
            rows = _psql_json("SELECT json_build_object('name',extname,'version',extversion,'schema',nspname) FROM pg_extension JOIN pg_namespace ON pg_extension.extnamespace=pg_namespace.oid ORDER BY extname")
            result = json.dumps(rows, indent=2)
        elif name == "tv_list_functions":
            schema = arguments.get("schema", "public")
            rows = _psql_json(f"SELECT json_build_object('schema',n.nspname,'name',p.proname,'args',pg_get_function_arguments(p.oid),'returns',pg_get_function_result(p.oid)) FROM pg_proc p JOIN pg_namespace n ON p.pronamespace=n.oid WHERE n.nspname='{schema}' ORDER BY p.proname")
            result = json.dumps(rows, indent=2)
        elif name == "tv_get_indexes":
            schema = arguments.get("schema", "public")
            table = arguments["table"]
            rows = _psql_json(f"SELECT json_build_object('name',indexname,'def',indexdef) FROM pg_indexes WHERE schemaname='{schema}' AND tablename='{table}' ORDER BY indexname")
            result = json.dumps(rows, indent=2)
        elif name == "tv_server_info":
            db_size = _psql_json("SELECT pg_size_pretty(pg_database_size(current_database()))")
            table_count = _psql_json("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'")
            stats = _psql_json("SELECT json_build_object('version',version(),'connections',(SELECT COUNT(*) FROM pg_stat_activity),'uptime',pg_postmaster_start_time())")
            result = json.dumps({"db": DB_NAME, "db_size": db_size[0] if db_size else "N/A", "total_tables": table_count[0] if table_count else 0, "stats": stats[0] if stats else {}}, indent=2)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        return [TextContent(type="text", text=result[:8000])]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]

async def main():
    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 📄 Archivo: `mcp-servers/openalex/requirements.txt`

```
fastmcp>=0.1.0
pyalex==0.18
aiohttp>=3.8.0
httpx>=0.25.0
biopython>=1.83
requests>=2.31.0
pydantic>=2.0.0
```

---

## 📄 Archivo: `mcp-servers/openalex/data_objects.py`

Crear este archivo con el siguiente contenido completo. Es el módulo de modelos de datos para el MCP de OpenAlex.

> **INSTRUCCIÓN PARA EL AGENTE:** Crea el archivo `mcp-servers/openalex/data_objects.py` con exactamente el contenido de abajo. Son ~448 líneas de código Python con modelos Pydantic optimizados para minimizar el uso de tokens.

```python
#!/usr/bin/env python3
"""
Optimized data models for the OpenAlex MCP server.
Streamlined versions focusing on essential information for author disambiguation
and work retrieval while minimizing token usage.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class WorkIDs(BaseModel):
    openalex: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    pmcid: Optional[str] = None
    mag: Optional[str] = None


class OptimizedAuthorResult(BaseModel):
    id: str
    display_name: str
    orcid: Optional[str] = None
    display_name_alternatives: Optional[List[str]] = None
    current_affiliations: Optional[List[str]] = None
    past_affiliations: Optional[List[str]] = None
    cited_by_count: int = 0
    works_count: int = 0
    h_index: Optional[int] = None
    i10_index: Optional[int] = None
    research_fields: Optional[List[str]] = None
    last_known_institutions: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    works_api_url: Optional[str] = None


class OptimizedWorkResult(BaseModel):
    id: str
    title: Optional[str] = None
    doi: Optional[str] = None
    publication_year: Optional[int] = None
    type: Optional[str] = None
    ids: Optional[WorkIDs] = None
    cited_by_count: Optional[int] = 0
    journal_name: Optional[str] = None
    journal_issn: Optional[str] = None
    publisher: Optional[str] = None
    is_open_access: Optional[bool] = None
    author_count: Optional[int] = None
    first_author: Optional[str] = None
    corresponding_author: Optional[str] = None
    primary_field: Optional[str] = None
    concepts: Optional[List[str]] = None


class OptimizedSearchResponse(BaseModel):
    query: str
    total_count: int
    results: List[OptimizedAuthorResult]
    search_time: Optional[datetime] = Field(default_factory=datetime.now)


class OptimizedWorksSearchResponse(BaseModel):
    author_id: str
    author_name: Optional[str] = None
    total_count: int
    results: List[OptimizedWorkResult]
    search_time: Optional[datetime] = Field(default_factory=datetime.now)
    filters: Optional[Dict[str, Any]] = None


class OptimizedGeneralWorksSearchResponse(BaseModel):
    query: str
    total_count: int
    results: List[OptimizedWorkResult]
    search_time: Optional[datetime] = Field(default_factory=datetime.now)
    filters: Optional[Dict[str, Any]] = None


class AutocompleteAuthorCandidate(BaseModel):
    openalex_id: str
    display_name: str
    institution_hint: Optional[str] = None
    works_count: int = 0
    cited_by_count: int = 0
    entity_type: str = "author"
    external_id: Optional[str] = None


class AutocompleteAuthorsResponse(BaseModel):
    query: str
    context: Optional[str] = None
    total_candidates: int
    candidates: List[AutocompleteAuthorCandidate]
    search_metadata: Dict[str, Any] = Field(default_factory=dict)


def extract_institution_names(affiliations: List[Dict[str, Any]]) -> tuple[List[str], List[str]]:
    current = []
    past = []
    if not affiliations:
        return current, past
    for affiliation in affiliations:
        institution = affiliation.get('institution', {})
        if not institution:
            continue
        institution_name = institution.get('display_name')
        if not institution_name:
            continue
        years = affiliation.get('years', [])
        if years:
            current_year = datetime.now().year
            if max(years) >= current_year - 3:
                current.append(institution_name)
            else:
                past.append(institution_name)
        else:
            current.append(institution_name)
    return current, past


def extract_research_fields(concepts_or_topics: List[Dict[str, Any]]) -> List[str]:
    fields = []
    if not concepts_or_topics:
        return fields
    sorted_items = sorted(concepts_or_topics, key=lambda x: x.get('score', 0) or x.get('count', 0), reverse=True)
    for item in sorted_items[:5]:
        name = item.get('display_name')
        if name:
            fields.append(name)
    return fields


def extract_journal_info(locations: List[Dict[str, Any]]) -> tuple[Optional[str], Optional[str], Optional[str]]:
    if not locations:
        return None, None, None
    for location in locations:
        source = location.get('source', {})
        if source and source.get('type') == 'journal':
            journal_name = source.get('display_name')
            issn = None
            if source.get('issn'):
                issn = source['issn'][0] if isinstance(source['issn'], list) else source['issn']
            publisher = source.get('host_organization_name')
            return journal_name, issn, publisher
    if locations:
        source = locations[0].get('source', {})
        if source:
            return source.get('display_name'), None, source.get('host_organization_name')
    return None, None, None


def extract_authorship_info(authorships: List[Dict[str, Any]]) -> tuple[Optional[int], Optional[str], Optional[str]]:
    if not authorships:
        return None, None, None
    author_count = len(authorships)
    first_author = None
    corresponding_author = None
    for authorship in authorships:
        if authorship.get('author_position') == 'first':
            author = authorship.get('author', {})
            first_author = author.get('display_name')
            break
    for authorship in authorships:
        if authorship.get('is_corresponding'):
            author = authorship.get('author', {})
            corresponding_author = author.get('display_name')
            break
    return author_count, first_author, corresponding_author


def extract_comprehensive_ids(work_data: Dict[str, Any]) -> WorkIDs:
    ids_data = work_data.get('ids', {})
    return WorkIDs(
        openalex=ids_data.get('openalex') or work_data.get('id'),
        doi=ids_data.get('doi') or work_data.get('doi'),
        pmid=ids_data.get('pmid'),
        pmcid=ids_data.get('pmcid'),
        mag=ids_data.get('mag')
    )


def optimize_author_data(author_data: Dict[str, Any]) -> OptimizedAuthorResult:
    author_id = author_data.get('id', '')
    display_name = author_data.get('display_name', '')
    orcid = author_data.get('orcid')
    alternatives = author_data.get('display_name_alternatives', [])
    affiliations = author_data.get('affiliations', [])
    current_affiliations, past_affiliations = extract_institution_names(affiliations)
    cited_by_count = author_data.get('cited_by_count', 0)
    works_count = author_data.get('works_count', 0)
    summary_stats = author_data.get('summary_stats', {})
    h_index = summary_stats.get('h_index')
    i10_index = summary_stats.get('i10_index')
    concepts = author_data.get('x_concepts', []) or author_data.get('topics', [])
    research_fields = extract_research_fields(concepts)
    countries = []
    if affiliations:
        for affiliation in affiliations:
            institution = affiliation.get('institution', {})
            country = institution.get('country_code')
            if country and country not in countries:
                countries.append(country)
    works_api_url = author_data.get('works_api_url')
    return OptimizedAuthorResult(
        id=author_id, display_name=display_name, orcid=orcid,
        display_name_alternatives=alternatives[:3] if alternatives else None,
        current_affiliations=current_affiliations[:3] if current_affiliations else None,
        past_affiliations=past_affiliations[:3] if past_affiliations else None,
        cited_by_count=cited_by_count, works_count=works_count,
        h_index=h_index, i10_index=i10_index,
        research_fields=research_fields[:5] if research_fields else None,
        last_known_institutions=current_affiliations[:2] if current_affiliations else past_affiliations[:2],
        countries=countries[:3] if countries else None,
        works_api_url=works_api_url
    )


def optimize_work_data(work_data: Dict[str, Any]) -> OptimizedWorkResult:
    work_id = work_data.get('id', '')
    title = work_data.get('title')
    doi = work_data.get('doi')
    publication_year = work_data.get('publication_year')
    work_type = work_data.get('type')
    comprehensive_ids = extract_comprehensive_ids(work_data)
    cited_by_count = work_data.get('cited_by_count', 0)
    locations = work_data.get('locations', [])
    journal_name, journal_issn, publisher = extract_journal_info(locations)
    open_access = work_data.get('open_access', {})
    is_open_access = open_access.get('is_oa') if open_access else None
    authorships = work_data.get('authorships', [])
    author_count, first_author, corresponding_author = extract_authorship_info(authorships)
    primary_topic = work_data.get('primary_topic', {})
    primary_field = primary_topic.get('display_name') if primary_topic else None
    concepts = work_data.get('concepts', [])
    concept_names = []
    if concepts:
        sorted_concepts = sorted(concepts, key=lambda x: x.get('score', 0), reverse=True)
        concept_names = [c.get('display_name') for c in sorted_concepts[:3] if c.get('display_name')]
    return OptimizedWorkResult(
        id=work_id, title=title, doi=doi, publication_year=publication_year,
        type=work_type, ids=comprehensive_ids, cited_by_count=cited_by_count,
        journal_name=journal_name, journal_issn=journal_issn, publisher=publisher,
        is_open_access=is_open_access, author_count=author_count,
        first_author=first_author, corresponding_author=corresponding_author,
        primary_field=primary_field, concepts=concept_names if concept_names else None
    )
```

---

## 📄 Archivo: `mcp-servers/openalex/server.py`

> **INSTRUCCIÓN PARA EL AGENTE:** Crea el archivo `mcp-servers/openalex/server.py` con el contenido de abajo. Son ~1755 líneas. Es un servidor MCP completo con búsqueda de autores, papers, PubMed y ORCID.
> Este archivo es LARGO — es correcto. Créalo completo sin truncar.

El archivo `server.py` del MCP de OpenAlex es muy extenso (~1755 líneas). Contiene:
- Búsqueda de autores con desambiguación inteligente
- Búsqueda de papers con filtrado peer-review
- Autocompletado de autores con ranking por institución
- Integración con PubMed (búsqueda, resúmenes, análisis de autores)
- Integración con ORCID (búsqueda de perfiles, publicaciones)

**Para obtener este archivo, ejecuta este comando en tu terminal:**

```powershell
# Opción 1: Si tienes acceso al repo fuente (pedir a Jairo)
# Copiar desde el repo n8n_teknoconecta/mcp-servers/openalex/server.py

# Opción 2: Pedir al agente de OpenCode que lo cree
# Dile al agente: "Crea el MCP server de OpenAlex usando fastmcp con las siguientes tools:
# - search_authors: búsqueda de autores por nombre con filtros de institución, tema y país
# - retrieve_author_works: obtener papers de un autor con filtrado peer-review
# - search_works: búsqueda de papers con modos general, title, title_and_abstract
# - autocomplete_authors: autocompletado inteligente con ranking por institución
# - search_pubmed: búsqueda en PubMed por autor, DOI, título o keywords
# - pubmed_author_sample: muestra detallada de un autor en PubMed con afiliaciones
# - search_orcid_authors: búsqueda de perfiles ORCID
# - get_orcid_publications: obtener publicaciones de un perfil ORCID
# Usa pyalex para la API de OpenAlex y los modelos de data_objects.py"
```

**Dependencias inline del script (header del archivo):**
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "fastmcp>=0.1.0",
#   "pyalex==0.18",
#   "aiohttp>=3.8.0",
#   "httpx>=0.25.0",
#   "biopython>=1.83",
#   "requests>=2.31.0",
# ]
# ///
```

---

## 🚀 Setup inicial (ejecutar una vez después de crear los archivos)

```powershell
# 1. Instalar dependencias del MCP de base de datos
cd mcp-servers\test-viral-db
uv venv
uv pip install mcp

# 2. Instalar dependencias del MCP de OpenAlex
cd ..\openalex
uv venv
uv pip install -r requirements.txt

# 3. Verificar SSH al VPS
ssh -o ConnectTimeout=5 root@5.252.52.190 "echo OK"
# Debe responder "OK". Si falla, tu SSH key no está autorizada aún.

# 4. Abrir OpenCode y verificar MCPs
# Dentro de OpenCode, probar cada MCP:
```

## ✅ Verificación de MCPs

| Comando de prueba | MCP | Respuesta esperada |
|-------------------|-----|-------------------|
| "lista las tablas de test_viral" | test-viral-db | Lista de tablas (puede estar vacía al inicio) |
| "muestra el estado de la app test-viral-app en coolify" | coolify-mcp | Status de la app |
| "busca en la web qué es machine learning" | jina | Resultados de búsqueda |
| "busca noticias recientes sobre IA" | tavily | Resultados de búsqueda |
| "busca papers de Albert Einstein" | openalex | Papers y métricas del autor |

---

## 📋 Credenciales de referencia rápida

| Servicio | Credencial | Valor |
|----------|-----------|-------|
| **Coolify API** | Token | `1\|GP1qcJjN3Hyi9HmEvyPDfXAoLp0LomhB1Bgul5DEaf517cae` |
| **Coolify URL** | Base URL | `https://coolify.chitaraagenteia.com` |
| **DB test_viral** | User | `testviral_app` |
| **DB test_viral** | Password | `TestViral2026!` |
| **DB test_viral** | Host | `5.252.52.190` (via SSH) |
| **Jina** | API Key | `jina_83c362354d4347659eb9544c08c247a9_UWJyp2BtQG5BLdZTDE8m64iUYOh` |
| **Tavily** | API Key | `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` |
| **OpenAlex** | Email | `contacto@teknoconecta.com` |
| **VPS SSH** | Host | `root@5.252.52.190` |
| **App dominio** | URL | `https://test.chitaraagenteia.com` |
| **Coolify Project** | UUID | `xon44yki7zp63j5v4d54r5rk` |
| **Coolify App** | UUID | `f8kxqoahu0hwlwimhktgjp7t` |
