from django.apps import AppConfig


class DealsConfig(AppConfig):
    name = 'deals'

    def ready(self):
        from . import signals
