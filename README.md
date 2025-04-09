# 🤖 asIAstente – Asistente Unificado con CAMEL + Open Interpreter

Este asistente combina procesamiento natural de lenguaje con ejecución de tareas automáticas en tu sistema. Está basado en modelos locales (como LLaMA2 usando Ollama) y puede ejecutar instrucciones paso a paso gracias a Open Interpreter.

---

## 📁 Estructura de Carpetas

~/agentes_IA/asistente_unificado/
├── gui/                         → Interfaz gráfica (Tkinter)
│   └── gui_asistente_final.py
├── tareas/                      → Banco de scripts personalizados
│   ├── busqueda.py
│   ├── instala.py
│   ├── limpia_la_ram.py
│   ├── aprende.py
│   ├── reprograma.py
│   └── convertir_csv_json.py
├── aprendidos/                  → Información aprendida por la IA
├── venv_asistente/              → Entorno virtual de Python

---

## 🚀 Instalación y Configuración

1. Ejecutar el generador de estructura

```bash
chmod +x crear_estructura_asistente.sh
./crear_estructura_asistente.sh
```

2. Configurar el entorno virtual y dependencias

```bash
chmod +x configuracion.sh
./configuracion.sh
```

Esto instalará automáticamente todas las dependencias necesarias y dejará el entorno listo.

---

## ▶️ Cómo ejecutar el asistente

```bash
source ~/agentes_IA/asistente_unificado/venv_asistente/bin/activate
python ~/agentes_IA/asistente_unificado/gui/gui_asistente_final.py
```

---

## 💡 ¿Qué puede hacer este asistente?

- Tomar una orden compleja en lenguaje natural.
- Generar los pasos necesarios usando el modelo CAMEL (via Ollama).
- Ejecutar cada paso automáticamente con Open Interpreter.
- Consultar tus mails, instalar software, aprender cosas nuevas, limpiar RAM, convertir archivos y más.

---

## ❗ Requisitos

- Python 3.12
- Ollama funcionando en http://localhost:11434
- Modelos ligeros como mistral, tinyllama u otros para bajo consumo de RAM

---

## 🧠 Personalización

Podés agregar nuevas tareas personalizadas en la carpeta `tareas/`. Serán detectadas automáticamente en versiones futuras de la GUI.

---

## 🛡️ Seguridad

Este sistema puede ejecutar tareas directamente en tu sistema operativo. Usalo con conocimiento y control de lo que los scripts hacen.

---

## ✨ Autoría y Licencia

Desarrollado como asistente personal con herramientas de IA open source.
