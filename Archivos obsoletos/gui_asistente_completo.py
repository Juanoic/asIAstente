import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, filedialog
import threading
import datetime
import os
import subprocess
import imaplib
import email
from email.header import decode_header

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

# --- Asistente Conversacional (CAMEL + Open Interpreter) ---
try:
    from camel.agents.ollama_chat import OllamaChat
except ImportError:
    print("Error: No se pudo importar CAMEL. Verifica que esté instalado.")
try:
    from openinterpreter import chat as oi_chat
except ImportError:
    print("Error: No se pudo importar Open Interpreter. Verifica que esté instalado.")

def procesar_comando(comando):
    """Envía el comando a CAMEL para que genere una lista de pasos."""
    agente = OllamaChat()
    mensaje = (
        "Necesito que generes una lista de pasos concretos para realizar la siguiente tarea:\n\n"
        f"{comando}\n\n"
        "Dame cada paso como una orden simple en una línea, sin explicaciones adicionales."
    )
    messages = [{"role": "user", "content": mensaje}]
    respuesta = agente.chat(messages)
    return respuesta

def ejecutar_pasos(pasos, text_widget):
    """Ejecuta cada paso generado usando Open Interpreter y muestra la salida."""
    lineas = [linea.strip() for linea in pasos.split("\n") if linea.strip() != ""]
    for i, paso in enumerate(lineas):
        text_widget.insert(tk.END, f"\n▶️ Ejecutando paso {i+1}: {paso}\n")
        resultado = oi_chat(paso)
        text_widget.insert(tk.END, f"✅ Resultado: {resultado}\n")
        text_widget.see(tk.END)

def enviar_comando():
    """Función para procesar el comando ingresado en la GUI."""
    comando = entry_comando.get()
    if not comando.strip():
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa un comando o tarea.")
        return
    text_area.insert(tk.END, f"\n👤 Usuario: {comando}\n")
    entry_comando.delete(0, tk.END)
    
    def proceso():
        try:
            pasos = procesar_comando(comando)
            text_area.insert(tk.END, f"\n🤖 CAMEL generó los siguientes pasos:\n{pasos}\n")
            ejecutar_pasos(pasos, text_area)
            text_area.insert(tk.END, "\n--- Tarea completada ---\n")
        except Exception as e:
            text_area.insert(tk.END, f"\n❌ Error: {str(e)}\n")
    
    threading.Thread(target=proceso).start()

# --- Integración de credenciales (para Gmail, etc.) ---
import credentials_manager as cm

# --- Función para leer correos (IMAP usando credenciales) ---
def leer_correos():
    username, password = cm.get_credentials("gmail")
    if not username or not password:
        text_area.insert(tk.END, "\n❌ No se pudieron obtener las credenciales de Gmail.\n")
        return
    imap_url = "imap.gmail.com"
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select("inbox")
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        latest_email_ids = email_ids[-5:] if len(email_ids) >= 5 else email_ids
        mails_info = []
        for e_id in latest_email_ids:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg.get("Subject", ""))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From", "Desconocido")
                    mails_info.append(f"De: {from_}\nAsunto: {subject}\n")
        mail.logout()
        for mail_info in mails_info:
            text_area.insert(tk.END, f"{mail_info}\n")
        text_area.insert(tk.END, "✅ Lectura de correos completada.\n")
    except Exception as e:
        text_area.insert(tk.END, f"\n❌ Error al leer correos: {str(e)}\n")

def btn_leer_correos():
    text_area.insert(tk.END, "\n📧 Leyendo últimos correos...\n")
    threading.Thread(target=leer_correos).start()

# --- Google Calendar ---
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    token_path = 'token.pickle'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                messagebox.showerror("Error", "Falta el archivo 'credentials.json' para Google Calendar.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    service = build("calendar", "v3", credentials=creds)
    return service

def agendar_evento():
    title = simpledialog.askstring("Evento", "Título del evento:")
    date_str = simpledialog.askstring("Fecha", "Fecha (AAAA-MM-DD):")
    start_time_str = simpledialog.askstring("Hora inicio", "Hora de inicio (HH:MM, 24h):")
    end_time_str = simpledialog.askstring("Hora fin", "Hora de fin (HH:MM, 24h):")
    description = simpledialog.askstring("Descripción", "Descripción del evento:")
    if not (title and date_str and start_time_str and end_time_str):
        messagebox.showwarning("Datos faltantes", "Todos los campos son obligatorios.")
        return
    try:
        start_datetime = datetime.datetime.strptime(date_str + " " + start_time_str, "%Y-%m-%d %H:%M")
        end_datetime = datetime.datetime.strptime(date_str + " " + end_time_str, "%Y-%m-%d %H:%M")
    except Exception as e:
        messagebox.showerror("Error", f"Error al parsear fecha/hora: {str(e)}")
        return
    text_area.insert(tk.END, "\n📅 Agendando evento en Google Calendar...\n")
    def proceso_agendar():
        try:
            service = get_calendar_service()
            if service is None:
                return
            event = {
                'summary': title,
                'description': description if description else "",
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'America/Argentina/Buenos_Aires',
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'America/Argentina/Buenos_Aires',
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
            text_area.insert(tk.END, f"✅ Evento agendado. Link: {event.get('htmlLink')}\n")
        except Exception as e:
            text_area.insert(tk.END, f"\n❌ Error al agendar evento: {str(e)}\n")
    threading.Thread(target=proceso_agendar).start()

def btn_agendar_evento():
    threading.Thread(target=agendar_evento).start()

# --- LibreOffice ---
def crear_documento_libreoffice():
    filename = simpledialog.askstring("Crear documento", "Ingresa el nombre del documento (sin extensión):")
    if not filename:
        return
    content = simpledialog.askstring("Contenido", "Ingresa el contenido del documento:")
    try:
        from odf.opendocument import OpenDocumentText
        from odf.text import P
        doc = OpenDocumentText()
        p = P(text=content if content else "")
        doc.text.addElement(p)
        folder = os.path.expanduser("~/agentes_IA/documentos_libreoffice")
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename + ".odt")
        doc.save(filepath)
        messagebox.showinfo("Documento creado", f"Documento creado en: {filepath}")
    except ImportError:
        messagebox.showerror("Error", "El módulo odfpy no está instalado. Instálalo con: sudo apt install python3-odfpy")

def abrir_documento_libreoffice():
    filepath = filedialog.askopenfilename(title="Selecciona un documento LibreOffice", filetypes=[("ODT files", "*.odt"), ("All files", "*.*")])
    if filepath:
        subprocess.run(["libreoffice", filepath])

def btn_libreoffice():
    ventana_lo = tk.Toplevel(ventana)
    ventana_lo.title("Acceso a LibreOffice")
    ventana_lo.geometry("400x200")
    tk.Label(ventana_lo, text="Selecciona una acción para LibreOffice:").pack(pady=10)
    tk.Button(ventana_lo, text="Crear nuevo documento", command=crear_documento_libreoffice).pack(pady=5)
    tk.Button(ventana_lo, text="Abrir documento existente", command=abrir_documento_libreoffice).pack(pady=5)

# --- Construcción de la GUI Principal ---
ventana = tk.Tk()
ventana.title("Asistente Unificado - Funcionalidades Integradas")
ventana.geometry("900x700")

frame_top = tk.Frame(ventana)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Ingresa la tarea que necesitas realizar:").pack()
entry_comando = tk.Entry(frame_top, width=90)
entry_comando.pack(pady=5)
tk.Button(frame_top, text="Enviar comando", command=enviar_comando).pack(pady=5)

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Leer últimos correos", command=btn_leer_correos).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Agendar evento en Calendar", command=btn_agendar_evento).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Acceso a LibreOffice", command=btn_libreoffice).grid(row=0, column=2, padx=10)

text_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=100, height=30)
text_area.pack(pady=10)

ventana.mainloop()
