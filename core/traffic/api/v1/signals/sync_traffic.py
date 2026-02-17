# Django Imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
# Locale Imports
from traffic.models import TrafficLogs, Cameras
from traffic.api.v1.services.graph_service import graph_service

@receiver(post_save, sender=TrafficLogs)
def sync_traffic_log_to_neo4j(sender, instance, created, **kwargs):
    """
        Creating Signals To When Creating object for TrafficLogs Table :
    """
    
    
    params = {
        'camera_name': instance.camera_id.name,
        'type_id': instance.type_id,
        'timestamp': instance.timestamp.isoformat(),
        'plate_number': instance.plate_number,
        'id' : instance.id or instance.pk
    }
    
    if graph_service.driver:
        with graph_service.driver.session() as session:
 
            if TrafficLogs.objects.filter(Q(plate_number=params["plate_number"]) & ~Q(type_id=params["type_id"])):
                cypher_suspicious_merge = """
                MERGE (c:suspicious {plate_number: $plate_number})
                SET c.plate_number = $plate_number,
                c.type_id = $type_id,
                c.id = $id
                MERGE (cam:Camera {name: $camera_name})
                CREATE (cam)-[r:PASSED]->(c)
                SET r.timestamp = datetime($timestamp),
                r.id = $id
                """
                print(f"this suspicious {params["plate_number"]}")
                session.run(cypher_suspicious_merge, params)
            cypher_full_merge = """
            MERGE (c:Car {plate_number: $plate_number})
            SET c.plate_number = $plate_number,
                c.type_id = $type_id,
                c.name = $plate_number,
                c.id = $id
            MERGE (cam:Camera {name: $camera_name})
            CREATE (cam)-[r:PASSED]->(c)
            SET r.timestamp = datetime($timestamp),
            r.id = $id
            """
            session.run(cypher_full_merge, params)

@receiver(post_save, sender=Cameras)
def sync_cameras_to_neo4j(sender, instance, created, **kwargs):
    """
        Creating Signals To When Creating object for Cameras Table :
    """
    params = {
        'name': instance.name,
        'id' : instance.id or instance.pk
    }
    
    if graph_service.driver:
        with graph_service.driver.session() as session:
            cypher_full_merge = """
            MERGE (cam:Camera {name: $name})
            SET cam.id = $id
            """
            session.run(cypher_full_merge, params)