from django.apps import AppConfig


class MylifeConfig(AppConfig):
    name = 'mylife'

    def ready(self):
        import mylife.signals
