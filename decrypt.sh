#!/bin/bash
# ============================================================
# DESENCRIPTADOR DE ARCHIVOS — SandiegoApart / TeknoConecta
# ============================================================
# Clave maestra: 5486
# Algoritmo: AES-256-CBC (PBKDF2, 100000 iteraciones)
#
# USO:
#   bash decrypt.sh                  → Desencripta todos los archivos
#   bash decrypt.sh opencode.jsonc   → Desencripta un archivo especifico
#
# ============================================================
# ARCHIVOS ENCRIPTADOS (listado de referencia):
# ============================================================
# opencode.jsonc.enc → Config principal de MCPs (26 servidores)
#   Contiene: tokens de Cloudflare, Clerk, OpenAI, Coolify,
#   MercadoPago, Neon, Vercel, Google Maps, Jina, Perplexity,
#   Scrapling, Supabase, Stays, PriceLabs. GitHub PAT, etc.
#
# documentacion/credenciales.enc → Credenciales de infra
#   Contiene: passwords de servicios (n8n, Directus, Coolify,
#   Code-server, Healthchecks), AWS keys, conexiones DB
# ============================================================

set -e

CLAVE="5486"

decrypt_file() {
  local input="$1"
  local output="${1%.enc}"
  
  if [ ! -f "$input" ]; then
    echo "❌ No encontrado: $input"
    return 1
  fi
  
  if [ -f "$output" ]; then
    echo "⚠️  Ya existe: $output (saltando)"
    return 0
  fi
  
  echo "🔓 Desencriptando $input → $output"
  openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -d -pass "pass:$CLAVE" -base64 -A -in "$input" -out "$output"
  echo "✅ $output listo"
}

# Si se especifica un archivo
if [ -n "$1" ]; then
  decrypt_file "$1.enc"
  exit $?
fi

# Desencriptar todos
echo "🔐 Desencriptando todos los archivos..."
echo ""

decrypt_file "opencode.jsonc.enc" || true
decrypt_file "documentacion/credenciales.enc" || true

echo ""
echo "✅ Proceso completado."
echo "⚠️  IMPORTANTE: Los archivos desencriptados NO se borran (estan en .gitignore)."
echo "   opencode.jsonc → Config principal de MCPs"
echo "   documentacion/credenciales → Passwords de infraestructura"
