# Terminal OVR - Gestor de Notas Ciberpunk 📟💻

![Profesión](https://img.shields.io/badge/Profesi%C3%B3n-Arquitectos%20T%C3%A9cnicos-2e7d32?logo=micro%3Abit&logoColor=white&style=flat-square)
![Role](https://img.shields.io/badge/Role-BIM%20%26%20ConTech-007ACC?logo=bim360&style=flat-square)
![Location](https://img.shields.io/badge/Location-A%20Coru%C3%B1a%20%F0%9F%8C%8A-005B94?logo=lighthouse&logoColor=white&style=flat-square)
![Maker](https://img.shields.io/badge/Maker-Software-red?logo=makerbot&style=flat-square)
![Hardware](https://img.shields.io/badge/Hardware---grey?style=flat-square)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&style=flat-square)
![Language](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white&style=flat-square)
![Stars](https://img.shields.io/github/stars/jmcaamanog/notas-en-pantalla?style=flat-square&color=yellow&logo=github)
![License](https://img.shields.io/github/license/jmcaamanog/notas-en-pantalla?style=flat-square&color=green)

(Arquitecto Técnico_JMC) Herramienta de escritorio ligera diseñada para la toma de notas en entornos de alta concentración. Presenta una interfaz de terminal inmersiva (estilo retro/ciberpunk) enfocada en evitar distracciones, incorporando herramientas de productividad, monitorización real del hardware y protocolos de cifrado para mantener la información local segura.

## 🚀 La Filosofía de la Herramienta (Fricción Cero)

Cuando estás picando código, modelando o redactando informes técnicos, las ventanas blancas de los editores convencionales rompen la concentración y cansan la vista. Esta utilidad nace para ser tu bloc de notas táctico: un entorno oscuro, rápido, que puedes volver transparente sobre otras ventanas y que te permite bloquear tu información sensible de miradas indiscretas con un solo atajo de teclado.

## 🧠 Características del Software (v5.0)

* **Sistema de Cifrado Real:** Al activar el "Lock Core" (o pulsar `ESC` como botón del pánico), la terminal bloquea la lectura, lanza una animación Matrix y encripta tus archivos `.txt` locales en Base64.
* **Monitorización de Hardware (Uplink Real):** Lee y muestra en tiempo real el consumo de CPU y RAM de tu ordenador directamente en el panel del sistema.
* **CLI (Command Line Interface):** Incorpora una consola integrada para ejecutar comandos como `/clear`, buscar texto con `/find` o generar reportes automáticos de tus notas con `/report`.
* **Pomodoro Integrado:** Ejecuta `/uplink 25` y activa un temporizador de concentración visual (barra de progreso ASCII) sin salir de la interfaz.
* **Modo Transparente:** Pulsa `Ctrl+T` para volver la terminal translúcida y poder tomar notas mientras lees documentación o ves un modelo 3D de fondo.

## 📂 Estructura del Repositorio
* 📁 **`CODE/`**: Contiene el codigo en python listo para descargar, editar y/o usar.
* 📁 **`PROGRAMA/`**: Contiene el programa compilado (`.exe`) listo para descargar y usar en Windows, sin necesidad de instalar Python.
* 📄 **`notas_de_pantalla.py`**: El código fuente principal de la terminal.
* 📄 **`app_icon.ico`**: El icono nativo de la aplicación necesario para la compilación.

## ⚙️ Requisitos para el Código Fuente

Si prefieres ejecutar o modificar el software desde el código fuente, necesitarás:

1. Clonar el repositorio y navegar a la carpeta.
2. Instalar la dependencia necesaria para la lectura de hardware:
   ```bash
   pip install psutil
3. Ejecutar el programa:
   ```bash
   python notas_de_pantalla.py

## ⚙️ Requisitos para el Código Fuente

Si prefieres ejecutar o modificar el software desde el código fuente, necesitarás:

1. Clonar el repositorio y navegar a la carpeta.
2. Instalar la dependencia necesaria para la lectura de hardware:
   ```bash
   pip install psutil
3. Ejecutar el programa:
   ```bash
   python notas_de_pantalla.py

## 🛠️ ¿Cómo compilar tu propio .exe?

1. Si modificas el código y quieres generar tu propio ejecutable con el icono incrustado en la ventana y sin consola de fondo, usa este comando con PyInstaller:
   ```bash
   pyinstaller --noconsole --onefile --icon="app_icon.ico" notas_de_pantalla.py

## 👨‍💻 Autor

Jose Manuel Caamaño González | Arquitecto Técnico & BIM Manager.
Digital Product Lead | ConTech & Digital Twin SaaS | BIM, Energy Modeling & Sustainability | Data Analytics (SQL, Power BI)

Hecho con código y café desde A Coruña. ☕

Jose Manuel Caamaño González | [LinkedIn](https://www.linkedin.com/in/jmcaamanog/)

































