#!/usr/bin/env python3
"""init_collections.py — Crear colección + índices de payload en Qdrant.

Uso:
  python init_collections.py \
    --host localhost --port 6333 --api-key $QDRANT_API_KEY \
    --collection system_topic_bge_m3_1024 --dim 1024
"""

import argparse
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType

def main():
    parser = argparse.ArgumentParser(description="Inicializar colección Qdrant")
    parser.add_argument("--host", default=os.environ.get("QDRANT_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("QDRANT_REST_PORT", "6333")))
    parser.add_argument("--api-key", default=os.environ.get("QDRANT_API_KEY", ""))
    parser.add_argument("--collection", required=True, help="Nombre de la colección")
    parser.add_argument("--dim", type=int, default=int(os.environ.get("QDRANT_DEFAULT_VECTOR_SIZE", "1024")),
                        help="Dimensión de vectores")
    parser.add_argument("--distance", default=os.environ.get("QDRANT_DEFAULT_DISTANCE", "Cosine"),
                        choices=["Cosine", "Euclid", "Dot"], help="Métrica de distancia")
    args = parser.parse_args()

    if not args.api_key:
        print("❌ ERROR: --api-key es obligatorio. Seteá QDRANT_API_KEY o pasá --api-key.")
        exit(1)

    distance = {"Cosine": Distance.COSINE, "Euclid": Distance.EUCLID, "Dot": Distance.DOT}[args.distance]

    client = QdrantClient(host=args.host, port=args.port, api_key=args.api_key)
    print(f"🔌 Conectado a {args.host}:{args.port}")

    # Crear colección si no existe
    collections = [c.name for c in client.get_collections().collections]
    if args.collection in collections:
        print(f"⚠️  Colección '{args.collection}' ya existe. Saltando creación.")
    else:
        client.create_collection(
            collection_name=args.collection,
            vectors_config=VectorParams(size=args.dim, distance=distance),
        )
        print(f"✅ Colección '{args.collection}' creada (dim={args.dim}, distance={args.distance})")

    # Índices de payload
    index_fields = [
        ("system_id", PayloadSchemaType.KEYWORD),
        ("workspace_id", PayloadSchemaType.KEYWORD),
        ("document_id", PayloadSchemaType.KEYWORD),
        ("topic_id", PayloadSchemaType.KEYWORD),
        ("language", PayloadSchemaType.KEYWORD),
        ("document_type", PayloadSchemaType.KEYWORD),
        ("sensitivity_level", PayloadSchemaType.KEYWORD),
    ]

    for field, schema_type in index_fields:
        try:
            client.create_payload_index(
                collection_name=args.collection,
                field_name=field,
                field_schema=schema_type,
            )
            print(f"  📌 Índice '{field}' ({schema_type.name}) creado")
        except Exception as e:
            if "already exists" in str(e).lower() or "conflict" in str(e).lower():
                print(f"  ⏭️  Índice '{field}' ya existe")
            else:
                print(f"  ⚠️  Índice '{field}': {e}")

    print(f"\n🎉 Colección '{args.collection}' lista.")

if __name__ == "__main__":
    main()
