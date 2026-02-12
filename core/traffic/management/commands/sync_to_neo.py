# traffic/management/commands/sync_to_neo.py
from django.core.management.base import BaseCommand
from traffic.models import TrafficLogs
from traffic.api.v1.services.graph_service import graph_service
import time

class Command(BaseCommand):
    help = "Sync existing TrafficLogs from PostgreSQL to Neo4j"

    def handle(self, *args, **options):
        self.stdout.write("Starting sync to Neo4j...")
        
        if not graph_service.driver:
            self.stdout.write(self.style.ERROR('Neo4j driver is not connected!'))
            return

        all_logs = TrafficLogs.objects.all().iterator(chunk_size=2000)
        
        count = 0
        start_time = time.time()

        with graph_service.driver.session() as session:
            for log in all_logs:
                count += 1
                
                camera_name = log.camera_id.name
                
                cypher_query = """
                MERGE (c:Car {plate_number: $plate_number})
                SET c.type_id = $type_id
                SET c.id = $id
                
                MERGE (cam:Camera {name: $camera_name})
                
                MERGE (cam)-[r:PASSED]->(c)
                SET r.timestamp = datetime($timestamp),
                    r.type_id = $type_id
                """
                
                params = {
                    'plate_number': log.plate_number,
                    'camera_name': camera_name,
                    'timestamp': log.timestamp.isoformat(),
                    'type_id': log.type_id,
                    'id': log.id,
                }
                
                session.run(cypher_query, params)
                
                if count % 10000 == 0:
                    self.stdout.write(f"{count} records synced...")

        end_time = time.time()
        duration = end_time - start_time
        self.stdout.write(self.style.SUCCESS(f'Successfully synced {count} records in {duration:.2f} seconds.'))