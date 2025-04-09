import tkinter as tk
from tkinter import scrolledtext, messagebox

def enviar_comando():
    comando = entry_comando.get()
    if not comando.strip():
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa un comando o tarea.")
        return
    # Aquí se mostrará el comando en el área de salida.
    text_area.insert(tk.END, f"Usuario: {comando}\n")
    # Limpiar la entrada para el próximo comando.
    entry_comando.delete(0, tk.END)
    # Simulación: Se muestra un mensaje de confirmación.
    text_area.insert(tk.END, "Asistente: Comando recibido. (Aquí se integrará la respuesta de CAMEL + Open Interpreter)\n")
    text_area.see(tk.END)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("GUI Básica del Asistente")
ventana.geometry("600x400")

# Marco superior para la entrada de comando
frame_top = tk.Frame(ventana)
frame_top.pack(pady=10)

label = tk.Label(frame_top, text="Ingresa el comando o tarea:")
label.pack()
entry_comando = tk.Entry(frame_top, width=70)
entry_comando.pack(pady=5)

btn_enviar = tk.Button(frame_top, text="Enviar", command=enviar_comando)
btn_enviar.pack()

# Área de texto con scroll para mostrar la interacción
text_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=70, height=20)
text_area.pack(pady=10)

# Ejecutar la GUI
ventana.mainloop()
