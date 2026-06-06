#!/bin/bash
# ============================================================
# sync-hermes-config.sh — Sincroniza archivos de configuracion
# de obsidian/ → obsidian/.hermes/ (donde Hermes lee)
# ============================================================
# Ejecutar en el VPS: bash /opt/hermes-workspace/infra/sync-hermes-config.sh
# O desde cron: 0 * * * * bash /opt/hermes-workspace/infra/sync-hermes-config.sh

set -e

WORKSPACE="/opt/hermes-workspace"
HERMES_DATA="$WORKSPACE/obsidian/.hermes"

echo "[sync-hermes] $(date '+%Y-%m-%d %H:%M:%S')"

# 1. SOUL.md — Personalidad y limites
if [ -f "$WORKSPACE/obsidian/hermes-soul.md" ]; then
    cp "$WORKSPACE/obsidian/hermes-soul.md" "$HERMES_DATA/SOUL.md"
    echo "  ✓ hermes-soul.md → SOUL.md"
else
    echo "  ⚠ hermes-soul.md no encontrado"
fi

# 2. AGENTS.md — Instrucciones del workspace
if [ -f "$WORKSPACE/obsidian/AGENTS.md" ]; then
    cp "$WORKSPACE/obsidian/AGENTS.md" "$HERMES_DATA/workspace/AGENTS.md" 2>/dev/null || true
    echo "  ✓ AGENTS.md synced"
fi

echo "[sync-hermes] done"
