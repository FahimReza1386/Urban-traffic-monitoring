# Django Imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# Locale Imports
from traffic.models import TrafficLogs, SuspiciousVehicles
from traffic.api.v1.services.graph_service import graph_service

@receiver(post_save, sender=TrafficLogs)
def sync_traffic_log_to_neo4j(sender, instance, created, **kwargs):
    params = {
        'camera_name': instance.camera_id.name,
        'type_id': instance.type_id,
        'timestamp': instance.timestamp.isoformat(),
        'plate_number': instance.plate_number,
    }
    
    if graph_service.driver:
        with graph_service.driver.session() as session:
            # # ۱. بررسی مشکوک
            # cypher_check_suspicious = """
            # MATCH (c:Car {plate_number: $plate_number})
            # WHERE c.type_id IS NOT NULL AND c.type_id <> $type_id
            # RETURN c.type_id AS existing_type
            # """
            # result = session.run(params)
            
            # if result.peek(): 
            #     # Testing For Mashkook Pelak
            #     cypher_mashkok_merge = """
            #     MATCH (c:Car)
            #     WHERE 
            #     c.plate_number =~ '.*(\\d)\\1\\1.*' OR
            #     c.plate_number =~ '^[0-9]+$' AND size(c.plate_number) >= 5 OR
            #     ANY(char IN ['ث', 'ص', 'ض', 'ط', 'ظ', 'غ'] WHERE char IN c.plate_number)
            #     RETURN c.plate_number, c.type           
            #     """
            #     print(f"{instance.plate_number} با نوع متفاوت پیدا شد")
            
            # ۲. مرج کردن داده‌ها
            cypher_full_merge = """
            MERGE (c:Car {plate_number: $plate_number})
            SET c.plate_number = $plate_number,
                c.type_id = $type_id,
                c.name = $plate_number
            MERGE (cam:Camera {name: $camera_name})
            MERGE (cam)-[r:PASSED]->(c)
            SET r.timestamp = datetime($timestamp)
            """
            session.run(cypher_full_merge, params)