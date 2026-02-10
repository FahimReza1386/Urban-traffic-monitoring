from django.apps import AppConfig


class TrafficConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'traffic'
    
    def ready(self):
        from traffic.api.v1.signals.sync_traffic import sync_traffic_log_to_neo4j