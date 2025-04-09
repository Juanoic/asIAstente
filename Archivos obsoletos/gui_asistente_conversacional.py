#!/usr/bin/env python3
import sys, os
import traceback  
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


def activate_venv(venv_path):
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    site_packages = os.path.join(venv_path, "lib", python_version, "site-packages")
    if os.path.isdir(site_packages):
        sys.path.insert(0, site_packages)
    else:
        print(f"❌ No se encontró site-packages en {site_packages}")

# Activación de entornos virtuales
activate_venv(os.path.expanduser("~/agentes_IA/camel/venv_camel"))
activate_venv(os.path.expanduser("~/agentes_IA/opin/venv_openinterpreter"))

# Rutas raíz
sys.path.insert(0, os.path.expanduser("~/agentes_IA/camel"))
sys.path.insert(0, os.path.expanduser("~/agentes_IA/opin"))

print("🔍 Rutas activas:")
for p in sys.path:
    print(p)

# === IMPORTS ===
try:
    from camel.agents.ollama_chat import OllamaChat
except ImportError as e:
    print("❌ Error al importar CAMEL:", e)

try:
    from interpreter import interpreter
except ImportError as e:
    print("❌ Error al importar Open Interpreter:", e)

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

# === FUNCIÓN ROBUSTA PARA RESPUESTA DE CAMEL ===
def procesar_comando(comando):
    agente = OllamaChat()
    mensaje = (
        "Necesito que generes una lista de pasos concretos para realizar la siguiente tarea:\n\n"
        f"{comando}\n\n"
        "Dame cada paso como una orden simple en una línea, sin explicaciones adicionales."
    )
    messages = [{"role": "user", "content": mensaje}]
    respuesta = agente.chat(messages)
    
    print("📤 CAMEL devolvió:", respuesta)  # Para depuración

    if isinstance(respuesta, str):
        return respuesta

    elif isinstance(respuesta, dict):
        if 'content' in respuesta:
            return respuesta['content']
        elif 'choices' in respuesta:
            try:
                return respuesta['choices'][0]['message']['content']
            except Exception:
                return str(respuesta)
        else:
            return str(respuesta)

    elif isinstance(respuesta, list):
        try:
            return "\n".join([msg['content'] for msg in respuesta if isinstance(msg, dict) and 'content' in msg])
        except:
            return str(respuesta)

    return str(respuesta)

# === FUNCIÓN PARA EJECUTAR LOS PASOS ===
def ejecutar_pasos(pasos, text_widget):
    lineas = [linea.strip() for linea in pasos.split("\n") if linea.strip()]
    for i, paso in enumerate(lineas):
        text_widget.insert(tk.END, f"\n▶️ Paso {i+1}: {paso}\n")
        try:
            resultado = interpreter.chat(paso)
            text_widget.insert(tk.END, f"✅ Resultado: {resultado}\n")
        except Exception as e:
            text_widget.insert(tk.END, f"❌ Error ejecutando paso {i+1}: {e}\n")
        text_widget.see(tk.END)

# === ENVÍO DEL COMANDO ===
def enviar_comando():
    comando = entry_comando.get().strip()
    if not comando:
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa una tarea.")
        return

    text_area.insert(tk.END, f"\n🧑 Usuario: {comando}\n")
    entry_comando.delete(0, tk.END)

   	

def proceso():
    try:
        pasos = procesar_comando(comando)
        print("🧾 Pasos normalizados desde CAMEL:", pasos)
        text_area.insert(tk.END, f"\n🧠 CAMEL generó los pasos:\n{pasos}\n")
        ejecutar_pasos(pasos, text_area)
        text_area.insert(tk.END, "\n✅ Tarea completada.\n")
    except Exception as e:
        error_trace = traceback.format_exc()
        print("❌ Error completo:\n", error_trace)
        text_area.insert(tk.END, f"\n❌ Error general:\n{error_trace}\n")

   
    threading.Thread(target=proceso).start()

# === GUI ===
ventana = tk.Tk()
ventana.title("🤖 Asistente CAMEL + Open Interpreter")
ventana.geometry("750x550")

frame_top = tk.Frame(ventana)
frame_top.pack(pady=10)

label = tk.Label(frame_top, text="¿Qué necesitas hacer?")
label.pack()

entry_comando = tk.Entry(frame_top, width=90)
entry_comando.pack(pady=5)

btn_enviar = tk.Button(frame_top, text="Enviar", command=enviar_comando)
btn_enviar.pack(pady=5)

text_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=90, height=25)
text_area.pack(pady=10)

ventana.mainloop()
