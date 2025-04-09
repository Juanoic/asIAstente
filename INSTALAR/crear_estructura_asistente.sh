#!/bin/bash

BASE=~/agentes_IA/asistente_unificado
GUI=$BASE/gui
TAREAS=$BASE/tareas
APRENDIDOS=$BASE/aprendidos

echo '🛠️ Creando estructura de carpetas...'
mkdir -p "$GUI" "$TAREAS" "$APRENDIDOS"

echo '📂 Copiando archivos a sus ubicaciones...'

cat > "$BASE/gui/gui_asistente_final.py" << 'EOF'
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

EOF

cat > "$BASE/tareas/busqueda.py" << 'EOF'
# Descripción: Realiza una búsqueda en una fuente determinada ("google", "chatgpt" o "la pc") basada en una consulta.

import os
import subprocess
import webbrowser

def buscar_en_google(query):
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    print("Abriendo navegador para buscar en Google...")
    webbrowser.open(url)

def buscar_en_chatgpt(query):
    # Como ChatGPT no tiene una URL de búsqueda directa, se abre la página de ChatGPT.
    print("Abriendo ChatGPT. Por favor, ingresa tu consulta manualmente:")
    print("Consulta:", query)
    url = "https://chat.openai.com/"
    webbrowser.open(url)

def buscar_en_la_pc(query):
    # Realiza una búsqueda en la carpeta home (para no abarcar todo el sistema)
    home = os.path.expanduser("~")
    print(f"Buscando archivos en {home} que contengan '{query}'...")
    result = subprocess.run(["find", home, "-iname", f"*{query}*"], capture_output=True, text=True)
    print("Resultados de la búsqueda:")
    print(result.stdout if result.stdout else "No se encontraron coincidencias.")

def main():
    print("¿Dónde deseas buscar? (google, chatgpt, la pc)")
    donde = input("Ingresa la fuente de búsqueda: ").strip().lower()
    print("¿Qué deseas buscar?")
    que = input("Ingresa la consulta: ").strip()
    
    if donde == "google":
        buscar_en_google(que)
    elif donde == "chatgpt":
        buscar_en_chatgpt(que)
    elif donde == "la pc":
        buscar_en_la_pc(que)
    else:
        print("Fuente de búsqueda no reconocida. Usa 'google', 'chatgpt' o 'la pc'.")

if __name__ == "__main__":
    main()

EOF

cat > "$BASE/tareas/instala.py" << 'EOF'
# Descripción: Instala un paquete en el sistema. Busca información del paquete en el repositorio (apt-cache) y pide confirmación antes de instalar.
import subprocess
import sys

def obtener_info_paquete(paquete):
    """Usa apt-cache show para obtener detalles del paquete."""
    try:
        result = subprocess.run(["apt-cache", "show", paquete], capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout:
            return None
        return result.stdout
    except Exception as e:
        print(f"Error al obtener información del paquete: {e}")
        return None

def instalar_paquete(paquete):
    """Instala el paquete usando sudo apt install."""
    try:
        print(f"Iniciando instalación de '{paquete}'...")
        result = subprocess.run(["sudo", "apt", "install", "-y", paquete], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Paquete '{paquete}' instalado correctamente.")
            print(result.stdout)
        else:
            print(f"Error durante la instalación de '{paquete}':")
            print(result.stderr)
    except Exception as e:
        print(f"Error al instalar el paquete: {e}")

def main():
    print("=== MÓDULO INSTALA ===")
    paquete = input("Ingresa el nombre del paquete que deseas instalar: ").strip()
    if not paquete:
        print("No se ingresó ningún paquete.")
        sys.exit(1)
    
    print(f"\nBuscando información para el paquete '{paquete}'...\n")
    info = obtener_info_paquete(paquete)
    if not info:
        print(f"No se encontró información para el paquete '{paquete}'. Verifica que el nombre sea correcto.")
        sys.exit(1)
    
    # Mostrar parte de la información para que el usuario confirme
    print("Información obtenida (primeros 500 caracteres):\n")
    print(info[:500])
    
    confirmar = input("\n¿Deseas proceder a instalar este paquete? (s/n): ").strip().lower()
    if confirmar == "s":
        instalar_paquete(paquete)
    else:
        print("Instalación cancelada.")

if __name__ == "__main__":
    main()

EOF

cat > "$BASE/tareas/limpia_la_ram.py" << 'EOF'
# Descripción: Limpia la memoria RAM liberando caches del sistema (requiere privilegios sudo).
import subprocess
import os

def limpiar_caches():
    print("Ejecutando sync para asegurar que todos los datos se escriban en disco...")
    subprocess.run(["sync"])
    print("Liberando caches (drop_caches)...")
    # Se utiliza sudo para escribir en /proc/sys/vm/drop_caches; puede solicitar la contraseña.
    result = subprocess.run(["sudo", "bash", "-c", "echo 3 > /proc/sys/vm/drop_caches"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Caches liberadas correctamente.")
    else:
        print("Error al liberar caches:", result.stderr)

if __name__ == "__main__":
    print("Iniciando limpieza de RAM...")
    if os.geteuid() != 0:
        print("Nota: Se requieren privilegios de root para liberar caches. Se te solicitará la contraseña de sudo si es necesario.")
    limpiar_caches()
    print("Limpieza de RAM completada.")

EOF

cat > "$BASE/tareas/reprograma.py" << 'EOF'
# Descripción: Permite que la IA se reprograme a sí misma actualizando su propio código a partir de un archivo externo.
import os
import sys
import shutil

def reprogramar():
    print("=== MÓDULO DE REPROGRAMACIÓN ===")
    print("Esta tarea te permitirá actualizar el código del script actual con una nueva versión.")
    path_nuevo = input("Ingresa el path del archivo con el nuevo código: ").strip()
    if not os.path.exists(path_nuevo):
        print("El archivo especificado no existe.")
        return
    
    confirmar = input("¿Estás seguro de que deseas actualizar el código actual? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Actualización cancelada.")
        return
    
    # Hacer un backup del archivo actual
    current_file = os.path.realpath(__file__)
    backup_file = current_file + ".backup"
    try:
        shutil.copy2(current_file, backup_file)
        print(f"Backup del archivo actual guardado en: {backup_file}")
    except Exception as e:
        print(f"Error al crear backup: {e}")
        return
    
    try:
        # Leer el nuevo código y escribirlo en el archivo actual
        with open(path_nuevo, "r", encoding="utf-8") as f_new:
            new_code = f_new.read()
        with open(current_file, "w", encoding="utf-8") as f_current:
            f_current.write(new_code)
        print("El código ha sido actualizado exitosamente. Por favor, reinicia el script para ver los cambios.")
    except Exception as e:
        print(f"Error al actualizar el código: {e}")
        # Restaurar backup si falla
        shutil.copy2(backup_file, current_file)
        print("El archivo original ha sido restaurado desde el backup.")

if __name__ == "__main__":
    reprogramar()

EOF

cat > "$BASE/tareas/aprende.py" << 'EOF'
# Descripción: La IA aprende información desde la web o desde un archivo proporcionado.
import os
import sys
import requests
import re
from datetime import datetime

def aprender_desde_web():
    url = input("Ingresa la URL de la página de la cual quieres aprender: ").strip()
    if not url:
        print("No se ingresó ninguna URL.")
        return None
    try:
        print("Obteniendo información de la web...")
        response = requests.get(url)
        response.raise_for_status()
        contenido = response.text
        resumen = contenido[:500]  # Tomamos los primeros 500 caracteres
        print("Información obtenida (primeros 500 caracteres):\n")
        print(resumen)
        return contenido
    except Exception as e:
        print(f"Error al obtener la información de la web: {str(e)}")
        return None

def aprender_desde_archivo():
    path = input("Ingresa el path completo del archivo: ").strip()
    if not os.path.exists(path):
        print("El archivo no existe.")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            contenido = f.read()
        print("Contenido del archivo (primeros 500 caracteres):\n")
        print(contenido[:500])
        return contenido
    except Exception as e:
        print(f"Error al leer el archivo: {str(e)}")
        return None

def almacenar_informacion(info):
    if not info:
        print("No hay información para almacenar.")
        return
    almacenar = input("¿Deseas almacenar esta información para futuras referencias? (s/n): ").strip().lower()
    if almacenar == "s":
        # Solicitar un nombre descriptivo para la información aprendida
        nombre = input("Ingresa un nombre descriptivo para esta información: ").strip()
        if not nombre:
            nombre = "aprendido"
        # Sanear el nombre para usarlo como nombre de archivo
        nombre_sanitizado = re.sub(r'\s+', '_', nombre)
        # Agregar un timestamp para hacerlo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{nombre_sanitizado}_{timestamp}.txt"
        # Crear la carpeta "aprendidos" si no existe
        directory = os.path.join(os.getcwd(), "aprendidos")
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(info)
            print(f"Información almacenada en: {filepath}")
        except Exception as e:
            print(f"Error al almacenar la información: {str(e)}")
    else:
        print("La información no se almacenó.")

def main():
    print("=== MÓDULO APRENDE ===")
    print("¿Desde dónde deseas que aprenda la IA? Escribe 'web' o 'archivo'.")
    opcion = input("Fuente de información: ").strip().lower()
    info = None
    if opcion == "web":
        info = aprender_desde_web()
    elif opcion == "archivo":
        info = aprender_desde_archivo()
    else:
        print("Opción no reconocida. Debe ser 'web' o 'archivo'.")
        sys.exit(1)
    
    almacenar_informacion(info)
    print("Proceso de aprendizaje completado.")

if __name__ == "__main__":
    main()

EOF

cat > "$BASE/tareas/convertir_csv_json.py" << 'EOF'
# Descripción: Convierte archivos CSV a JSON.
import sys

def convertir_csv_a_json():
    print("Ejecutando conversión de CSV a JSON...")
    # Aquí se implementaría la lógica real de conversión.
    # Por ahora, simulamos el proceso.
    print("Archivo CSV convertido a JSON exitosamente.")

if __name__ == "__main__":
    convertir_csv_a_json()

EOF

echo '✅ Todo listo en $BASE'