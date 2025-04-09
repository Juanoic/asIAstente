# Descripción: Permite que la IA se reprograme a sí misma actualizando su propio código a partir de un archivo externo.
import os
import sys
import shutil

def reprogramar():
    print("=== MÓDULO DE REPROGRAMACIÓN ===")
    print("Esta tarea te permitirá actualizar el código del script actual con una nueva versión.")
    path_nuevo = input("Ingresa el path del archivo con el nuevo código: ").strip()
    if not os.path.exists(path_nuevo):
        print("El archivo especificado no existe.")
        return
    
    confirmar = input("¿Estás seguro de que deseas actualizar el código actual? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Actualización cancelada.")
        return
    
    # Hacer un backup del archivo actual
    current_file = os.path.realpath(__file__)
    backup_file = current_file + ".backup"
    try:
        shutil.copy2(current_file, backup_file)
        print(f"Backup del archivo actual guardado en: {backup_file}")
    except Exception as e:
        print(f"Error al crear backup: {e}")
        return
    
    try:
        # Leer el nuevo código y escribirlo en el archivo actual
        with open(path_nuevo, "r", encoding="utf-8") as f_new:
            new_code = f_new.read()
        with open(current_file, "w", encoding="utf-8") as f_current:
            f_current.write(new_code)
        print("El código ha sido actualizado exitosamente. Por favor, reinicia el script para ver los cambios.")
    except Exception as e:
        print(f"Error al actualizar el código: {e}")
        # Restaurar backup si falla
        shutil.copy2(backup_file, current_file)
        print("El archivo original ha sido restaurado desde el backup.")

if __name__ == "__main__":
    reprogramar()
