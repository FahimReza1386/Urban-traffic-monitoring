# traffic/management/commands/sync_to_neo.py
from django.core.management.base import BaseCommand
from traffic.models import TrafficLogs
from core.traffic.api.v1.services.graph_service import graph_service
import time

"""

    command : docker compose exec backend python manage.py sync_to_neo --start 2000000 --batch_size 10000

"""



class Command(BaseCommand):
    help = "Sync TrafficLogs from PostgreSQL to Neo4j efficiently in batches"

    def add_arguments(self, parser):
        parser.add_argument(
            '--start',
            type=int,
            default=0,
            help='Record number to start syncing from (0-based index)'
        )
        parser.add_argument(
            '--batch_size',
            type=int,
            default=1000,
            help='Number of records to send per batch to Neo4j'
        )

    def handle(self, *args, **options):
        start_from = options['start']
        batch_size = options['batch_size']
        self.stdout.write(f"Starting sync from record #{start_from} with batch size {batch_size}...")

        if not graph_service.driver:
            self.stdout.write(self.style.ERROR('Neo4j driver is not connected!'))
            return

        all_logs = TrafficLogs.objects.all()[start_from:].iterator(chunk_size=batch_size)
        
        count = start_from
        new_count = 0
        batch = []
        start_time = time.time()

        with graph_service.driver.session() as session:
            for log in all_logs:
                count += 1
                batch.append({
                    'plate_number': log.plate_number,
                    'type_id': log.type_id,
                    'id': log.id,
                    'camera_name': log.camera_id.name,
                    'timestamp': log.timestamp.isoformat()
                })

                if len(batch) >= batch_size:
                    session.run("""
                    UNWIND $batch AS row
                    MERGE (c:Car {plate_number: row.plate_number})
                      ON CREATE SET c.type_id = row.type_id, c.id = row.id
                    MERGE (cam:Camera {name: row.camera_name})
                    MERGE (cam)-[r:PASSED {timestamp: datetime(row.timestamp)}]->(c)
                      ON CREATE SET r.type_id = row.type_id
                    """, {'batch': batch})
                    
                    new_count += len(batch)
                    batch = []

                    if count % (batch_size * 10) == 0:
                        self.stdout.write(f"{count} records processed, {new_count} new records synced...")

            # ارسال باقی‌مانده‌ها
            if batch:
                session.run("""
                UNWIND $batch AS row
                MERGE (c:Car {plate_number: row.plate_number})
                  ON CREATE SET c.type_id = row.type_id, c.id = row.id
                MERGE (cam:Camera {name: row.camera_name})
                MERGE (cam)-[r:PASSED {timestamp: datetime(row.timestamp)}]->(c)
                  ON CREATE SET r.type_id = row.type_id
                """, {'batch': batch})
                new_count += len(batch)

        end_time = time.time()
        duration = end_time - start_time
        self.stdout.write(self.style.SUCCESS(
            f'Processed {count} records, synced {new_count} new records in {duration:.2f} seconds.'
        ))
