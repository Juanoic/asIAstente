import tkinter as tk
from tkinter import messagebox
import os
import subprocess

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


CARPETA_TAREAS = os.path.expanduser("~/agentes_IA/tareas")

def ejecutar_script(script):
    ruta = os.path.join(CARPETA_TAREAS, script)
    subprocess.run(["python3", ruta])

def generar_acciones():
    objetivo = entry_objetivo.get()
    if not objetivo.strip():
        messagebox.showwarning("Falta el objetivo", "Escribí un objetivo antes de generar acciones.")
        return

    subprocess.run(["bash", "-c", "cd ~/agentes_IA/camel && source venv_camel/bin/activate && python3 camel_gen_acciones.py"], shell=True)
    subprocess.run(["bash", "-c", "cd ~/agentes_IA/open-interpreter && source venv_openinterpreter/bin/activate && python3 ejecutar_con_interpreter.py"], shell=True)

def actualizar_lista_tareas():
    lista_tareas.delete(0, tk.END)
    scripts = [f for f in os.listdir(CARPETA_TAREAS) if f.endswith(".py")]
    for s in sorted(scripts):
        lista_tareas.insert(tk.END, s)

def ejecutar_tarea_seleccionada(event=None):
    seleccion = lista_tareas.curselection()
    if seleccion:
        script = lista_tareas.get(seleccion[0])
        ejecutar_script(script)

ventana = tk.Tk()
ventana.title("Agente IA Unificado - CAMEL + Open Interpreter")
ventana.geometry("600x400")

frame_top = tk.Frame(ventana)
frame_top.pack(pady=10)

label_objetivo = tk.Label(frame_top, text="🎯 Objetivo de la tarea:")
label_objetivo.pack()
entry_objetivo = tk.Entry(frame_top, width=70)
entry_objetivo.pack()

btn_generar = tk.Button(frame_top, text="🔁 Generar pasos con CAMEL y ejecutar con Open Interpreter", command=generar_acciones)
btn_generar.pack(pady=10)

frame_mid = tk.Frame(ventana)
frame_mid.pack(pady=10, fill=tk.BOTH, expand=True)

label_tareas = tk.Label(frame_mid, text="📁 Scripts disponibles en 'tareas/':")
label_tareas.pack()

lista_tareas = tk.Listbox(frame_mid, width=60, height=10)
lista_tareas.pack()
lista_tareas.bind("<Double-1>", ejecutar_tarea_seleccionada)

btn_actualizar = tk.Button(frame_mid, text="🔄 Actualizar lista de scripts", command=actualizar_lista_tareas)
btn_actualizar.pack(pady=5)

os.makedirs(CARPETA_TAREAS, exist_ok=True)
actualizar_lista_tareas()

ventana.mainloop()
