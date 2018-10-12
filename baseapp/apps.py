from django.apps import AppConfig


class BaseappConfig(AppConfig):
    name = 'baseapp'

    def ready(self):
        import baseapp.signals
