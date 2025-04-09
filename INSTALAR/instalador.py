#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import time
import getpass
import shutil

cancelado = False

# Rutas
DESTINO = os.path.expanduser("~/AsIAstente")
LOGO_PATH = "/usr/share/icons/hicolor/128x128/apps/asIAstente.png"
ORIGEN = "/usr/share/asIAstente"
SCRIPTS = [
    "crear_estructura_asistente.sh",
    "configuracion.sh",
    "instalador.sh"
]

# Solicita contraseña sudo una vez
def obtener_sudo():
    global sudo_pass
    sudo_pass = getpass.getpass("🔒 Ingrese su contraseña de administrador: ")
    
  
 

# Ejecuta un script como sudo desde la nueva carpeta
def ejecutar_con_sudo(script):
    ruta = os.path.join(DESTINO, script)
    comando = f"echo '{sudo_pass}' | sudo -S bash {ruta}"
    return subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Copia todos los archivos desde /usr/share/asIAstente a ~/AsIAstente
def copiar_archivos():
    if not os.path.exists(DESTINO):
        os.makedirs(DESTINO)
    for archivo in os.listdir(ORIGEN):
        origen = os.path.join(ORIGEN, archivo)
        destino = os.path.join(DESTINO, archivo)
        shutil.copy2(origen, destino)

# Simula barra de progreso y ejecuta los scripts
def instalar_asistente(progreso, ventana):
    global cancelado
    print("📁 Copiando archivos a ~/AsIAstente...")
    mensaje_estado.set("📁 Copiando archivos a ~/AsIAstente...")
    copiar_archivos()

    total = len(SCRIPTS)
    for i, script in enumerate(SCRIPTS):
        if cancelado:
            mensaje_estado.set("❌ Instalación cancelada por el usuario.")
            print("❌ Instalación cancelada por el usuario.")
            return

        progreso["value"] = (i / total) * 100
        mensaje_estado.set(f"⚙️ Ejecutando: {script}")
        print(f"⚙️ Ejecutando: {script}")
        ventana.update_idletasks()

        ruta_script = os.path.join(DESTINO, script)
        try:
            os.chmod(ruta_script, 0o755)
            print(f"🔓 Permisos de ejecución otorgados a: {ruta_script}")
        except Exception as e:
            print(f"❌ No se pudo otorgar permisos a {ruta_script}: {e}")
            continue

        if script == "crear_estructura_asistente.sh":
            resultado = ejecutar_con_sudo(script)
            if resultado.returncode != 0:
                mensaje_estado.set("❌ Error creando la estructura. Instalación detenida.")
                print("❌ Error en crear_estructura_asistente.sh")
                return
            esperado = os.path.expanduser("~/AsIAstente")
            if not os.path.exists(esperado):
                mensaje_estado.set("❌ No se creó la estructura esperada.")
                print("❌ Faltan carpetas en asistente_unificado")
                return
        else:
            ejecutar_con_sudo(script)

        time.sleep(1)

    mensaje_estado.set("📎 Creando acceso directo en el escritorio...")
    print("📎 Creando acceso directo en el escritorio...")
    crear_acceso_directo()
    mensaje_estado.set("✅ Instalación completada.")
    print("✅ Instalación completada correctamente.")
    messagebox.showinfo("Completado", "✅ El asistente fue instalado con éxito.")
    ventana.destroy()



# Crea acceso directo en el escritorio
def crear_acceso_directo():
    escritorio = os.path.expanduser("~/Escritorio")
    if not os.path.exists(escritorio):
        os.makedirs(escritorio)
    acceso = os.path.join(escritorio, "asIAstente.desktop")
    with open(acceso, "w") as f:
        f.write("[Desktop Entry]\n"
                "Name=asIAstente\n"
                "Comment=Asistente conversacional con IA local\n"
                "Exec=bash -c 'cd ~/AsIAstente && python3 gui_asistente_final.py'\n"
                f"Icon={LOGO_PATH}\n"
                "Terminal=true\n"
                "Type=Application\n"
                "Categories=Utility;\n")
    os.chmod(acceso, 0o755)

# GUI
def iniciar_instalacion():
    obtener_sudo()
    threading.Thread(target=instalar_asistente, args=(barra, ventana), daemon=True).start()

ventana = tk.Tk()
ventana.title("Instalador de asIAstente")
ventana.geometry("420x300")
ventana.resizable(False, False)

if os.path.exists(LOGO_PATH):
    from PIL import Image, ImageTk
    logo = Image.open(LOGO_PATH).resize((100, 100))
    logo_tk = ImageTk.PhotoImage(logo)
    label_logo = tk.Label(ventana, image=logo_tk)
    label_logo.pack(pady=10)
else:
    tk.Label(ventana, text="asIAstente", font=("Arial", 20, "bold")).pack(pady=20)

tk.Label(ventana, text="Instalando el sistema...\nEsto puede tardar algunos minutos.").pack(pady=5)
barra = ttk.Progressbar(ventana, orient="horizontal", length=300, mode="determinate")
barra.pack(pady=20)

mensaje_estado = tk.StringVar()
estado_label = tk.Label(ventana, textvariable=mensaje_estado)
estado_label.pack(pady=5)

def cancelar_instalacion():
    global cancelado
    cancelado = True
    ventana.destroy()

btn_cancelar = tk.Button(ventana, text="❌ Cancelar", command=cancelar_instalacion)
btn_cancelar.pack(pady=5)

iniciar_instalacion()
ventana.mainloop()

