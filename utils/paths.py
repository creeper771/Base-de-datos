import os
import sys

def get_resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso, compatible con PyInstaller y el entorno de desarrollo.
    Reemplaza la función repetida `rutas(self, ruta)` en varias clases.
    """
    try:
        # PyInstaller crea un directorio temporal y almacena su ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
