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
