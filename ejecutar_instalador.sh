#!/bin/bash
# Script para lanzar el instalador gráfico de asIAstente

echo "🚀 Iniciando instalador gráfico de asIAstente..."

# Ruta al instalador
INSTALLER=~/agentes_IA/instalador_asIAstente.py

# Verifica si existe
if [ -f "$INSTALLER" ]; then
    python3 "$INSTALLER"
else
    echo "❌ No se encontró el instalador en: $INSTALLER"
    exit 1
fi
