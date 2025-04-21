"""
Configuración de ASGI para el proyecto asistente.

Este archivo expone el callable de ASGI como una variable de nivel de módulo llamada ``application``.

Para más información sobre este archivo, consulta:
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os  # Importa el módulo os para interactuar con el sistema operativo.

from django.core.asgi import get_asgi_application  # Importa la función para obtener la aplicación ASGI de Django.

# Establece la configuración predeterminada del módulo de configuración de Django.
# Esto indica a Django qué archivo de configuración debe usar.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistente.settings')

# Obtiene la aplicación ASGI.
# Este es el punto de entrada para los servidores compatibles con ASGI que manejarán las solicitudes.
application = get_asgi_application()