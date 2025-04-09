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
