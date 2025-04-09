import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import subprocess
import threading

## lo nuevo 1
import sys, os
sys.path.append(os.path.expanduser("~/agentes_IA/camel"))
sys.path.append(os.path.expanduser("~/agentes_IA/open-interpreter"))

import sys, os

## lo nuevo 2 

def activate_venv(venv_path):
    # Determina la carpeta de site-packages basada en la versión actual de Python.
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    site_packages = os.path.join(venv_path, "lib", python_version, "site-packages")
    if os.path.isdir(site_packages):
        sys.path.insert(0, site_packages)
    else:
        print(f"Advertencia: No se encontró site-packages en {site_packages}")

### hasta aca

# Ruta del banco de procesos
PROCESS_DIR = os.path.expanduser("~/agentes_IA/tareas")

# Importar CAMEL para usar su agente (asegúrate de que esté instalado y configurado)
try:
    from camel.agents.ollama_chat import OllamaChat
except ImportError:
    print("Error: No se pudo importar CAMEL. Verifica que camel.agents.ollama_chat esté instalado.")

def buscar_proceso(comando):
    """
    Recorre la carpeta de procesos, extrae la descripción de cada script (la primera línea que comience con "# Descripción:"),
    y genera un prompt para que CAMEL seleccione el proceso más adecuado según el comando ingresado.
    Retorna el nombre del archivo seleccionado.
    """
    tasks = []
    if not os.path.exists(PROCESS_DIR):
        return None, "No existe la carpeta de tareas."
    
    for filename in os.listdir(PROCESS_DIR):
        if filename.endswith(".py"):
            path = os.path.join(PROCESS_DIR, filename)
            with open(path, "r") as f:
                first_line = f.readline().strip()
                if first_line.startswith("# Descripción:"):
                    description = first_line[len("# Descripción:"):].strip()
                else:
                    description = "Sin descripción."
            tasks.append((filename, description))
    
    if not tasks:
        return None, "No se encontraron procesos en la carpeta."
    
    # Construir el prompt para CAMEL
    prompt = "Tengo la siguiente lista de procesos disponibles:\n"
    for filename, description in tasks:
        prompt += f"- {filename}: {description}\n"
    prompt += f"\nEl usuario solicita: {comando}\n"
    prompt += "¿Cuál de estos procesos es el más adecuado ejecutar? Responde solo con el nombre del archivo."
    
    agente = OllamaChat()
    messages = [{"role": "user", "content": prompt}]
    respuesta = agente.chat(messages)
    selected_process = respuesta.strip()
    return selected_process, prompt  # Retornamos también el prompt para fines de depuración si se desea.

def ejecutar_proceso(file_name, text_widget):
    """
    Ejecuta el script indicado (dentro de la carpeta de procesos) y muestra la salida en el área de texto.
    """
    path = os.path.join(PROCESS_DIR, file_name)
    if not os.path.exists(path):
        text_widget.insert(tk.END, f"\n❌ El proceso '{file_name}' no existe.\n")
        return
    text_widget.insert(tk.END, f"\n▶️ Ejecutando proceso: {file_name}\n")
    try:
        result = subprocess.run(["python3", path], capture_output=True, text=True)
        text_widget.insert(tk.END, f"✅ Salida:\n{result.stdout}\n")
        if result.stderr:
            text_widget.insert(tk.END, f"⚠️ Errores:\n{result.stderr}\n")
    except Exception as e:
        text_widget.insert(tk.END, f"\n❌ Error al ejecutar el proceso: {str(e)}\n")

def btn_buscar_ejecutar():
    """
    Función que se invoca al pulsar el botón.
    Toma el comando ingresado, usa CAMEL para buscar el proceso adecuado en el banco,
    y ejecuta el script seleccionado.
    """
    comando = entry_comando.get()
    if not comando.strip():
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa una tarea.")
        return
    text_area.insert(tk.END, f"\n👤 Usuario: {comando}\n")
    
    def proceso():
        try:
            selected_process, debug_prompt = buscar_proceso(comando)
            if not selected_process:
                text_area.insert(tk.END, f"\n❌ No se encontró un proceso adecuado.\n")
                return
            text_area.insert(tk.END, f"\n🤖 Proceso seleccionado: {selected_process}\n")
            # Para depuración, se puede imprimir el prompt generado:
            # text_area.insert(tk.END, f"\n[DEBUG] Prompt enviado:\n{debug_prompt}\n")
            ejecutar_proceso(selected_process, text_area)
            text_area.insert(tk.END, "\n--- Proceso completado ---\n")
        except Exception as e:
            text_area.insert(tk.END, f"\n❌ Error: {str(e)}\n")
    
    threading.Thread(target=proceso).start()

# Construcción de la GUI
ventana = tk.Tk()
ventana.title("Asistente - Banco de Procesos Unificado")
ventana.geometry("700x500")

frame_top = tk.Frame(ventana)
frame_top.pack(pady=10)

label = tk.Label(frame_top, text="Ingresa la tarea que necesitas realizar:")
label.pack()
entry_comando = tk.Entry(frame_top, width=80)
entry_comando.pack(pady=5)

btn_ejecutar = tk.Button(frame_top, text="Buscar y ejecutar proceso", command=btn_buscar_ejecutar)
btn_ejecutar.pack(pady=5)

text_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=20)
text_area.pack(pady=10)

ventana.mainloop()
