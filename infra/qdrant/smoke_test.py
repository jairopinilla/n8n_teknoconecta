#!/usr/bin/env python3
"""smoke_test.py — Verificar aislamiento cross-workspace en Qdrant.

Uso:
  python smoke_test.py \
    --host localhost --port 6333 --api-key $QDRANT_API_KEY

El script:
  1. Crea colección de prueba 'smoke_test_tmp'
  2. Inserta 3 points: 2 del workspace_a, 1 del workspace_b
  3. Busca con filtro workspace_id = workspace_a
  4. Verifica que solo devuelve resultados de workspace_a
  5. Limpia la colección de prueba
"""

import argparse
import os
import random
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

DIM = 128  # Dimensión pequeña para test

def random_vector(dim: int) -> list[float]:
    return [random.uniform(-1, 1) for _ in range(dim)]

def main():
    parser = argparse.ArgumentParser(description="Smoke test Qdrant — aislamiento workspace_id")
    parser.add_argument("--host", default=os.environ.get("QDRANT_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("QDRANT_REST_PORT", "6333")))
    parser.add_argument("--api-key", default=os.environ.get("QDRANT_API_KEY", ""))
    args = parser.parse_args()

    if not args.api_key:
        print("❌ ERROR: --api-key es obligatorio.")
        exit(1)

    client = QdrantClient(host=args.host, port=args.port, api_key=args.api_key)
    collection = "smoke_test_tmp"
    print(f"🔌 Conectado a {args.host}:{args.port}")

    # Crear colección de prueba
    client.recreate_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=DIM, distance=Distance.COSINE),
    )
    print(f"📦 Colección '{collection}' creada")

    # Insertar points
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=random_vector(DIM),
                    payload={"workspace_id": "workspace_a", "document_id": "doc_1", "text": "Resultado A1"}),
        PointStruct(id=str(uuid.uuid4()), vector=random_vector(DIM),
                    payload={"workspace_id": "workspace_a", "document_id": "doc_2", "text": "Resultado A2"}),
        PointStruct(id=str(uuid.uuid4()), vector=random_vector(DIM),
                    payload={"workspace_id": "workspace_b", "document_id": "doc_3", "text": "Resultado B1"}),
    ]
    client.upsert(collection_name=collection, points=points)
    print(f"⬆️  Insertados {len(points)} points (2 workspace_a, 1 workspace_b)")

    # Buscar con filtro workspace_a
    query_vec = random_vector(DIM)
    results = client.search(
        collection_name=collection,
        query_vector=query_vec,
        query_filter=Filter(
            must=[FieldCondition(key="workspace_id", match=MatchValue(value="workspace_a"))]
        ),
        limit=10,
    )

    workspace_ids = [r.payload.get("workspace_id") for r in results]
    print(f"🔍 Resultados de búsqueda (filtro workspace_a): {len(results)} points")
    for i, r in enumerate(results):
        print(f"  [{i}] workspace_id={r.payload['workspace_id']} score={r.score:.4f}")

    # Verificar aislamiento
    if "workspace_b" in workspace_ids:
        print("\n❌ FAIL: Se filtró resultado de workspace_b. El aislamiento NO funciona.")
        exit(1)

    if len(results) != 2 or all(w == "workspace_a" for w in workspace_ids):
        print("\n✅ PASS: Aislamiento por workspace_id funciona correctamente.")
    else:
        print(f"\n❌ FAIL: Se esperaban 2 resultados de workspace_a, se obtuvieron {len(results)}.")
        exit(1)

    # Limpiar
    client.delete_collection(collection_name=collection)
    print(f"🧹 Colección '{collection}' eliminada.")

if __name__ == "__main__":
    main()
