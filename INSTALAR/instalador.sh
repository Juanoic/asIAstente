#!/bin/bash

echo "=========================="
echo "Instalación y configuración de componentes básicos"
echo "=========================="

# Actualizar sistema e instalar dependencias básicas
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip build-essential

# Instalar Ollama y descargar LLaMA2
echo "Instalando Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

if ! command -v ollama &> /dev/null; then
  echo "⚠️ Ollama no está en el PATH. Reiniciá la terminal."
fi

echo "Iniciando Ollama..."
ollama serve &

echo "Descargando modelo LLaMA2..."
ollama pull llama2

# Instalar Open Interpreter
echo "Instalando Open Interpreter..."
cd ~/agentes_IA/open-interpreter || exit
git clone https://github.com/OpenInterpreter/open-interpreter.git .
python3 -m venv venv_openinterpreter
source venv_openinterpreter/bin/activate
pip install -e .
deactivate

# Instalar CAMEL-AI
echo "Instalando CAMEL-AI..."
cd ~/agentes_IA/camel || exit
git clone https://github.com/lightaime/camel.git .
python3 -m venv venv_camel
source venv_camel/bin/activate
pip install -r requirements.txt
deactivate

echo "=========================="
echo "Componentes instalados y configurados correctamente."
