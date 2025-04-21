#!/usr/bin/env python
"""
Utilidad de línea de comandos de Django para tareas administrativas.

Este archivo se utiliza para ejecutar comandos administrativos de Django, como iniciar el servidor de desarrollo,
aplicar migraciones, crear superusuarios, entre otros.
"""

import os  # Importa el módulo os para interactuar con el sistema operativo.
import sys  # Importa el módulo sys para acceder a argumentos y configuraciones del sistema.

def main():
    """
    Ejecuta tareas administrativas.

    Configura la variable de entorno `DJANGO_SETTINGS_MODULE` para apuntar al archivo de configuración del proyecto
    y ejecuta los comandos proporcionados desde la línea de comandos.
    """
    # Establece el módulo de configuración predeterminado de Django.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistente.settings')
    try:
        # Importa la función para ejecutar comandos desde la línea de comandos.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Lanza un error si Django no está instalado o no está disponible en PYTHONPATH.
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y "
            "disponible en tu variable de entorno PYTHONPATH? ¿Olvidaste activar "
            "un entorno virtual?"
        ) from exc
    # Ejecuta el comando proporcionado en la línea de comandos.
    execute_from_command_line(sys.argv)

# Punto de entrada principal del script.
if __name__ == '__main__':
    main()