from django.apps import AppConfig
from traffic.api.v1.services.graph_service import graph_service

class TrafficConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'traffic'
    
    def ready(self):
        from traffic.api.v1.signals.sync_traffic import sync_traffic_log_to_neo4j, sync_cameras_to_neo4j
        
        self.create_neo4j_indexes()
    
    def create_neo4j_indexes(self):
        try:
            if graph_service.driver:
                with graph_service.driver.session() as session:
                    session.run("""
                    CREATE INDEX car_plate IF NOT EXISTS 
                    FOR (c:Car) ON (c.plate_number)
                    """)
                    
                    session.run("""
                    CREATE INDEX traffic_time IF NOT EXISTS 
                    FOR (c:Car) ON (c.timestamp)
                    """)
                    
                    session.run("""
                    CREATE INDEX camera_name IF NOT EXISTS 
                    FOR (c:Camera) ON (c.name)
                    """)
                    
                    session.run("""
                    CREATE INDEX suspicious_plate IF NOT EXISTS 
                    FOR (c:suspicious) ON (c.plate_number)
                    """)
                    session.run("""
                    CREATE INDEX suspicious_plate IF NOT EXISTS 
                    FOR (c:suspicious) ON (c.timestamp)
                    """)
                    
                    print("✅ Neo4j indexes created/verified successfully")
        except Exception as e:
            print(f"⚠️ Error creating Neo4j indexes: {e}")