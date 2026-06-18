# Payload Schema — Qdrant multi-tenant

## Payload mínimo (obligatorio)

Todo point insertado en Qdrant DEBE incluir estos campos:

```json
{
  "system_id": "topic_system",
  "workspace_id": "workspace_abc123",
  "document_id": "doc_xyz789",
  "chunk_id": "chunk_001",
  "source_type": "markdown",
  "source_path": "s3://topicsystem/documents/doc_xyz789/chunk_001.md",
  "document_title": "Informe de mercado Q1 2026",
  "document_type": "pdf",
  "language": "es",
  "page_number": 1,
  "section_title": "Resumen Ejecutivo",
  "chunk_index": 0,
  "created_at": "2026-06-16T12:00:00Z",
  "updated_at": "2026-06-16T12:00:00Z"
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `system_id` | keyword | Slug del sistema dueño |
| `workspace_id` | keyword | ID canónico del workspace (obligatorio en filtro) |
| `document_id` | keyword | ID canónico del documento en PostgreSQL |
| `chunk_id` | keyword | ID único del chunk |
| `source_type` | keyword | `markdown`, `text`, `image_description` |
| `source_path` | keyword | Ruta S3 o filesystem al chunk original |
| `document_title` | keyword | Título del documento padre |
| `document_type` | keyword | `pdf`, `docx`, `pptx`, `xlsx`, `md`, `txt`, `image` |
| `language` | keyword | `es`, `en`, `pt`, `unknown` |
| `page_number` | integer | Número de página en el documento original |
| `section_title` | keyword | Título de la sección |
| `chunk_index` | integer | Índice del chunk dentro del documento |
| `created_at` | keyword | ISO-8601 |
| `updated_at` | keyword | ISO-8601 |

## Payload opcional

```json
{
  "topic_id": "topic_456",
  "tags": ["finanzas", "mercado", "2026"],
  "quality_score": 0.92,
  "ocr_confidence": 0.88,
  "translation_status": "none",
  "is_translated": false,
  "original_language": "es",
  "target_language": "en",
  "sensitivity_level": "internal",
  "source_hash": "sha256:abc123..."
}
```

## Índices de payload

Al crear una colección, crear índices para estos campos:

| Campo | Tipo de índice | Obligatorio |
|-------|---------------|-------------|
| `system_id` | keyword | ✅ |
| `workspace_id` | keyword | ✅ |
| `document_id` | keyword | Opcional |
| `topic_id` | keyword | Opcional |
| `language` | keyword | Opcional |
| `document_type` | keyword | Opcional |
| `tags` | keyword | Opcional |
| `sensitivity_level` | keyword | Opcional |
| `created_at` | datetime | Opcional |

## Naming de colecciones

```
system_{system_slug}_{embedding_model}_{dimension}
```

Ejemplos:
- `system_topic_bge_m3_1024`
- `system_chitara_bge_m3_1024`
- `system_sandiego_bge_m3_1024`

## Aislamiento por workspace_id

Toda consulta DEBE incluir filtro `must` por `workspace_id`:

```python
qdrant.search(
    collection_name="system_topic_bge_m3_1024",
    query_vector=embedding,
    query_filter={
        "must": [
            {"key": "workspace_id", "match": {"value": workspace_id_from_jwt}}
        ]
    }
)
```

El `workspace_id` lo resuelve el backend desde el JWT/token de sesión.
El LLM NUNCA construye este filtro. El cliente NUNCA envía `workspace_id`.
