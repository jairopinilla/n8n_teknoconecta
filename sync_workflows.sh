#!/usr/bin/env bash
# sync_workflows.sh
# Descarga todos los workflows de n8n y los guarda en ./workflows/
# Requiere: curl, jq
# Lee credenciales desde secrets.json (ignorado por git)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SECRETS_FILE="$SCRIPT_DIR/secrets.json"
OUTPUT_DIR="$SCRIPT_DIR/workflows"

if [[ ! -f "$SECRETS_FILE" ]]; then
  echo "ERROR: No se encontró $SECRETS_FILE"
  exit 1
fi

N8N_HOST=$(jq -r '.n8n.host' "$SECRETS_FILE")
API_KEY=$(jq -r '.n8n.api_key' "$SECRETS_FILE")

mkdir -p "$OUTPUT_DIR"

echo "Obteniendo lista de workflows desde $N8N_HOST..."

# Paginar todos los workflows
cursor=""
ids=()
names=()

while true; do
  url="$N8N_HOST/api/v1/workflows?limit=100&active=true"
  [[ -n "$cursor" ]] && url="${url}&cursor=${cursor}"

  response=$(curl -s -f \
    -H "X-N8N-API-KEY: $API_KEY" \
    -H "Accept: application/json" \
    "$url")

  count=$(echo "$response" | jq '.data | length')
  echo "  → $count workflows encontrados en esta página"

  while IFS= read -r id; do
    ids+=("$id")
  done < <(echo "$response" | jq -r '.data[].id')

  while IFS= read -r name; do
    names+=("$name")
  done < <(echo "$response" | jq -r '.data[].name')

  next=$(echo "$response" | jq -r '.nextCursor // empty')
  [[ -z "$next" ]] && break
  cursor="$next"
done

total=${#ids[@]}
echo "Total workflows: $total"
echo ""

for i in "${!ids[@]}"; do
  id="${ids[$i]}"
  name="${names[$i]}"
  # Sanitiza el nombre para usar como filename
  safe_name=$(echo "$name" | tr '/ :*?"<>|\\' '_')
  out_file="$OUTPUT_DIR/${safe_name}.json"

  echo "Descargando [$((i+1))/$total]: $name..."
  curl -s -f \
    -H "X-N8N-API-KEY: $API_KEY" \
    -H "Accept: application/json" \
    "$N8N_HOST/api/v1/workflows/$id" \
    | jq '.' > "$out_file"

  echo "  → $out_file"
done

echo ""
echo "Sincronización completa. $(ls "$OUTPUT_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ') archivos en $OUTPUT_DIR"
