#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import time
import getpass

# Rutas
BASE = os.path.expanduser("~/agentes_IA")
LOGO_PATH = os.path.join(BASE, "logo.png")
SCRIPT1 = os.path.join(BASE, "instalar", "crear_estructura_asistente.sh")
SCRIPT2 = os.path.join(BASE, "instalar", "configuracion.sh")
SCRIPT3 = os.path.join(BASE, "instalar", "instalador.sh")

# Solicita contraseña sudo una vez
def obtener_sudo():
    global sudo_pass
    sudo_pass = getpass.getpass("🔒 Ingrese su contraseña de administrador: ")

# Ejecuta un script con privilegios sudo
def ejecutar_con_sudo(script):
    comando = f"echo '{sudo_pass}' | sudo -S bash {script}"
    return subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Simula barra de progreso mientras instala
def instalar_asistente(progreso, ventana):
    pasos = [SCRIPT1, SCRIPT2, SCRIPT3]
    total = len(pasos)
    for i, script in enumerate(pasos):
        progreso["value"] = (i / total) * 100
        ventana.update_idletasks()
        ejecutar_con_sudo(script)
        time.sleep(1)
    progreso["value"] = 100
    ventana.update_idletasks()
    crear_acceso_directo()
    messagebox.showinfo("Completado", "✅ El asistente fue instalado con éxito.")
    ventana.destroy()

def crear_acceso_directo():
    escritorio = os.path.expanduser("~/Escritorio")
    if not os.path.exists(escritorio):
        os.makedirs(escritorio)

    acceso = os.path.join(escritorio, "asIAstente.desktop")
    with open(acceso, "w") as f:
        f.write(f"""[Desktop Entry]
Name=asIAstente
Comment=Asistente conversacional con IA local
Exec=bash -c 'source ~/agentes_IA/asistente_unificado/venv_asistente/bin/activate && python ~/agentes_IA/asistente_unificado/gui/gui_asistente_final.py'
Icon={BASE}/logo.png
Terminal=true
Type=Application
Categories=Utility;
""")
    os.chmod(acceso, 0o755)


# GUI de instalación
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

iniciar_instalacion()
ventana.mainloop()
