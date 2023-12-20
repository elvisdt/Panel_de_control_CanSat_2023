# _PANEL DE CONTROL CANSAT_

El presente proyecto contempla el diseño del panel de control de proyecto CANSAT 2023


## Requerimientos previos.
Para poder ejecutar el proyecto previamente debara tener instalada python ver 3.11 o superior, las librerias instaladas son:

```
Modulos y librerias intalados:
- customtkinter (tkinter personalizado)
- pyte (terminal virtual) 
- aioprocessing (ejecutar un nuevo proceso)

pip install customtkinter
pip install pyte 
pip install aioprocessing
pip install pywinpty

pip install pexpect

```

## Estructura de archivos.

El archivo principal del proyecto **panel de control** es [main.py](src/main.py) el cual se encuantra en la carpeta [src](src). Asimismo a continuacion se muestra la estructura del archivos en el presente proyecto:

```
nombre_del_proyecto/
|-- src/                     # Contiene el código fuente principal
|   |-- main.py              # Punto de entrada principal del programa
|   |-- ui/                  # Contiene archivos relacionados con la interfaz de usuario
|   |   |-- frames/          # Contiene clases de frames de Tkinter
|   |   |-- widgets/         # Contiene clases de widgets de Tkinter personalizados
|   |-- controllers/         # Contiene controladores para la lógica de negocio
|   |-- models/              # Contiene modelos de datos y objetos del dominio
|-- resources/               # Contiene recursos como imágenes, iconos y archivos de configuración
|   |-- images/              # Contiene imágenes y gráficos
|   |-- icons/               # Contiene iconos
|   |-- fonts/               # Contiene fuentes tipográficas
|   |-- config/              # Contiene archivos de configuración
|-- tests/                   # Contiene pruebas unitarias y de integración
|-- scripts/                 # Contiene scripts para automatización, como CI/CD y scripts de compilación
|-- docs/                    # Contiene documentación del proyecto, como guías y especificaciones
|-- README.md                # Describe el proyecto.
```
