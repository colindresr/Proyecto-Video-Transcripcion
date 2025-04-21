from django.apps import AppConfig  # Importa AppConfig para configurar la aplicación de Django.


class VideosConfig(AppConfig):
    """
    Configuración de la aplicación 'videos'.

    Esta clase define la configuración predeterminada para la aplicación,
    como el tipo de campo automático para los modelos y el nombre de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Define el tipo de campo automático predeterminado para los modelos.
    name = 'videos'  # Especifica el nombre de la aplicación.