import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import os
import sys
import requests

# --- Activar entornos virtuales y rutas necesarias ---
def activate_venv(venv_path):
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    site_packages = os.path.join(venv_path, "lib", python_version, "site-packages")
    if os.path.isdir(site_packages):
        sys.path.insert(0, site_packages)

# Activar venvs
activate_venv(os.path.expanduser("~/agentes_IA/camel/venv_camel"))
activate_venv(os.path.expanduser("~/agentes_IA/opin/venv_openinterpreter"))

# Agregar los paths de los proyectos
sys.path.append(os.path.expanduser("~/agentes_IA/camel"))
sys.path.append(os.path.expanduser("~/agentes_IA/opin"))

# --- Implementación robusta de OllamaChat ---
class OllamaChat:
    def __init__(self, model="llama2", system_prompt="Eres un asistente útil."):
        self.model = model
        self.system_prompt = system_prompt

    def chat(self, messages):
        conversation = [{"role": "system", "content": self.system_prompt}]
        conversation.extend(messages)

        full_prompt = ""
        for msg in conversation:
            role = msg["role"]
            content = msg["content"]
            full_prompt += f"{'User' if role == 'user' else 'Assistant'}: {content}\n"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        }

        try:
            response = requests.post("http://localhost:11434/api/generate", json=payload)
            json_data = response.json()
            print("📦 DEBUG JSON recibido:", json_data)
            return json_data.get("response", json_data)
        except Exception as e:
            return f"Error general: {e}"

# --- Función para invocar Open Interpreter ---
try:
    from openinterpreter import chat as oi_chat
except ImportError:
    def oi_chat(prompt):
        return "❌ Open Interpreter no está disponible."

# --- Lógica del flujo CAMEL → Open Interpreter ---
def procesar_comando(comando):
    agente = OllamaChat()
    prompt = (
        "Necesito que generes una lista de pasos concretos para realizar la siguiente tarea:\n\n"
        f"{comando}\n\n"
        "Dame cada paso como una orden simple en una línea, sin explicaciones adicionales."
    )
    messages = [{"role": "user", "content": prompt}]
    respuesta = agente.chat(messages)
    return respuesta

def ejecutar_pasos(pasos, text_widget):
    lineas = [linea.strip() for linea in pasos.split("\n") if linea.strip()]
    for i, paso in enumerate(lineas):
        text_widget.insert(tk.END, f"\n▶️ Ejecutando paso {i+1}: {paso}\n")
        try:
            resultado = oi_chat(paso)
            text_widget.insert(tk.END, f"✅ Resultado: {resultado}\n")
        except Exception as e:
            text_widget.insert(tk.END, f"❌ Error ejecutando paso: {str(e)}\n")
        text_widget.see(tk.END)

# --- Función principal que activa el flujo ---
def enviar_comando():
    comando = entry_comando.get()
    if not comando.strip():
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa un comando o tarea.")
        return
    text_area.insert(tk.END, f"\n👤 Usuario: {comando}\n")
    entry_comando.delete(0, tk.END)

    def proceso():
        try:
            pasos = procesar_comando(comando)
            if isinstance(pasos, dict) and "error" in pasos:
                text_area.insert(tk.END, f"\n❌ Error en CAMEL: {pasos['error']}\n")
                return
            text_area.insert(tk.END, f"\n🤖 CAMEL generó los siguientes pasos:\n{pasos}\n")
            ejecutar_pasos(pasos, text_area)
            text_area.insert(tk.END, "\n--- Tarea completada ---\n")
        except Exception as e:
            text_area.insert(tk.END, f"\n❌ Error inesperado: {str(e)}\n")
    threading.Thread(target=proceso).start()

# --- GUI básica con Tkinter ---
ventana = tk.Tk()
ventana.title("Asistente Conversacional - CAMEL + Open Interpreter")
ventana.geometry("750x550")

frame_top = tk.Frame(ventana)
frame_top.pack(pady=10)

label = tk.Label(frame_top, text="🔧 Ingresa la tarea que necesitas realizar:")
label.pack()

entry_comando = tk.Entry(frame_top, width=80)
entry_comando.pack(pady=5)

btn_enviar = tk.Button(frame_top, text="🚀 Enviar comando", command=enviar_comando)
btn_enviar.pack(pady=5)

text_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=90, height=25)
text_area.pack(pady=10)

ventana.mainloop()
