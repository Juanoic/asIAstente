import sys
import os

# Añadir el path donde vive la carpeta camel
sys.path.insert(0, os.path.expanduser("~/agentes_IA/camel"))

from camel.agents.ollama_chat import OllamaChat

agente = OllamaChat()
mensaje = [
    {"role": "user", "content": "Decime cómo crear un archivo de backup en Linux"}
]
respuesta = agente.chat(mensaje)

print("🧠 RESPUESTA:", respuesta)
