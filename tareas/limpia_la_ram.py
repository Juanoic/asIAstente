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
