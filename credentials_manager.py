import os
import json
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import tkinter as tk
from tkinter import simpledialog, messagebox

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

# Activa el entorno de Camel-AI
activate_venv(os.path.expanduser("~/agentes_IA/camel/venv_camel"))
# Activa el entorno de Open Interpreter
activate_venv(os.path.expanduser("~/agentes_IA/open-interpreter/venv_openinterpreter"))



# Rutas donde se guardarán los datos cifrados y la sal
CREDENTIALS_FILE = os.path.expanduser("~/agentes_IA/creds.enc")
SALT_FILE = os.path.expanduser("~/agentes_IA/creds.salt")
MASTER_KEY = None

def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Deriva una clave segura a partir de la contraseña maestra y una sal.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def get_master_key():
    """
    Obtiene (o solicita) la contraseña maestra y deriva la clave correspondiente.
    Si ya se obtuvo en la sesión, se usa la misma.
    """
    global MASTER_KEY
    if MASTER_KEY is not None:
        return MASTER_KEY
    # Si no existe la sal, se crea una nueva
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    # Pedir la contraseña maestra mediante una ventana de diálogo
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    master_password = simpledialog.askstring("Contraseña maestra",
                                             "Ingresa la contraseña maestra para las credenciales:",
                                             show="*")
    root.destroy()
    if master_password is None:
        messagebox.showerror("Error", "No se ingresó la contraseña maestra. Abortando.")
        exit(1)
    key = derive_key(master_password, salt)
    MASTER_KEY = key
    return key

def load_credentials():
    """
    Carga y descifra el archivo de credenciales. Si no existe, retorna un diccionario vacío.
    """
    key = get_master_key()
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    with open(CREDENTIALS_FILE, "rb") as f:
        encrypted_data = f.read()
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(encrypted_data)
    except InvalidToken:
        messagebox.showerror("Error", "Contraseña maestra incorrecta o datos corruptos.")
        return {}
    return json.loads(decrypted.decode())

def save_credentials(creds: dict):
    """
    Cifra y guarda el diccionario de credenciales en el archivo correspondiente.
    """
    key = get_master_key()
    fernet = Fernet(key)
    data = json.dumps(creds).encode()
    encrypted = fernet.encrypt(data)
    with open(CREDENTIALS_FILE, "wb") as f:
        f.write(encrypted)

def get_credentials(service: str):
    """
    Para un servicio dado (por ejemplo, "gmail"), busca las credenciales almacenadas.
    Si no existen, solicita al usuario (vía ventana de diálogo) que las ingrese, las guarda cifradas y las retorna.
    """
    creds = load_credentials()
    if service in creds:
        return creds[service]["username"], creds[service]["password"]
    else:
        root = tk.Tk()
        root.withdraw()
        username = simpledialog.askstring("Credenciales",
                                          f"Ingrese el usuario para {service}:")
        password = simpledialog.askstring("Credenciales",
                                          f"Ingrese la contraseña para {service}:",
                                          show="*")
        root.destroy()
        if username is None or password is None:
            messagebox.showerror("Error", "No se ingresaron las credenciales necesarias.")
            return None, None
        creds[service] = {"username": username, "password": password}
        save_credentials(creds)
        return username, password
