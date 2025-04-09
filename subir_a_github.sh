#!/bin/bash

echo "📦 Subida automática del proyecto a GitHub"

CONFIG_FILE=".github_repo_url"

# Leer o solicitar la URL del repositorio remoto
if [ -f "$CONFIG_FILE" ]; then
    repo_url=$(cat "$CONFIG_FILE")
    echo "🔗 Usando URL guardada: $repo_url"
else
    read -p "🔗 Pegá la URL del repositorio remoto de GitHub (ej: https://github.com/usuario/asIAstente.git): " repo_url
    echo "$repo_url" > "$CONFIG_FILE"
fi

# Confirmar si está en una carpeta con contenido
if [ ! "$(ls -A .)" ]; then
   echo "⚠️ Esta carpeta está vacía. Abortando..."
   exit 1
fi

# Inicializar git si no existe
if [ ! -d ".git" ]; then
    git init
fi

# Configurar el remoto (forzando cambio si ya existe)
git remote remove origin 2>/dev/null
git remote add origin "$repo_url"

# Agregar todo recursivamente
git add .

# Commit con fecha y hora
commit_msg="Actualización del proyecto - $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$commit_msg"

# Crear rama main si no existe
git branch -M main

# Subir al remoto
git push -u origin main

echo "✅ Proyecto subido correctamente a GitHub."
