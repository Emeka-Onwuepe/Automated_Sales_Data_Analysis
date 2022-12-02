from django.apps import AppConfig


class DataSetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_sets'
    
    def ready(self):
        from data_sets import signals
    