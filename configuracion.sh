#!/bin/bash

BASE=~/agentes_IA/asistente_unificado
PYTHON=python3.12

echo "🔧 Preparando entorno..."

# Crear entorno virtual para el asistente
echo "📦 Creando entorno virtual..."
python3 -m venv $BASE/venv_asistente

# Activar entorno
source $BASE/venv_asistente/bin/activate

# Actualizar pip y herramientas base
echo "⬆️  Actualizando pip y setuptools..."
pip install --upgrade pip setuptools wheel

# Instalar dependencias necesarias
echo "📚 Instalando dependencias..."
pip install openai==1.2.3 requests PyYAML pillow colorama docstring_parser pandas numpy<2 numexpr bottleneck

# Verificar instalación
echo "✅ Entorno listo. Ejecuta así:"
echo ""
echo "source $BASE/venv_asistente/bin/activate"
echo "python $BASE/gui/gui_asistente_final.py"
echo ""

deactivate
