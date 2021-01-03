from django.apps import AppConfig
from django.utils.module_loading import import_module


class WebapiConfig(AppConfig):
    name = 'WEBAPI'

    def ready(self):
        import_module("WEBAPI.signals.webapi_signals")
