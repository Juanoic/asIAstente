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
