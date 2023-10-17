from django.apps import AppConfig


class WomenConfig(AppConfig):
    """Класс конфигурации приложения Women"""
    verbose_name = 'Женщины мира'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
