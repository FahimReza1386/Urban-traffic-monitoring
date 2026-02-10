# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from traffic.models import TrafficLogs
from traffic.api.v1.services.graph_service import graph_service

@receiver(post_save, sender=TrafficLogs)
def sync_traffic_log_to_neo4j(sender, instance, created, **kwargs):
    cypher_merge_car = """
    MERGE (c:Car {plate_number: $plate_number})
    SET c.plate_number = $plate_number,
        c.type_id = $type_id,
        c.name = $type_id
    """
    
    camera_name = instance.camera_id.name
    
    cypher_merge_camera = """
    MERGE (cam:Camera {name: $camera_name})
    """

    cypher_create_relation = """
    MATCH (c:Car {plate_number: $plate_number})
    MATCH (cam:Camera {name: $camera_name})
    CREATE (cam)-[r:PASSED]->(c)
    SET r.timestamp = datetime($timestamp)
    """

    params = {
        'camera_name': camera_name,
        'type_id': instance.type_id,
        'timestamp': instance.timestamp.isoformat(),
        'plate_number': instance.plate_number,
    }

    if graph_service.driver:
        with graph_service.driver.session() as session:
            session.run(cypher_merge_car, params)
            session.run(cypher_merge_camera, params)
            session.run(cypher_create_relation, params)