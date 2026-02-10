# graph_service.py
from neo4j import GraphDatabase
from django.conf import settings

class GraphService:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_CONFIG['uri'],
                auth=settings.NEO4J_CONFIG['auth']
            )
            self.driver.verify_connectivity()
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")
            self.driver = None

    def get_car_detailed_path(self, plate_number):
        """
        مسیر پیشرفته یک خودرو را برمی‌گرداند (شامل زمان و نوع خودرو).
        """
        cypher_query = """
        MATCH (c:Car {plate_number: $plate_number})-[r:PASSED]->(cam:Camera)
        RETURN cam.name as camera_name, 
               r.timestamp as timestamp, 
               c.type_id as type_id
        ORDER BY r.timestamp ASC
        """
        
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run(cypher_query, {"plate_number": plate_number})
            
            path_list = []
            for record in result:
                path_list.append({
                    "camera": record["camera_name"],
                    "timestamp": str(record["timestamp"]),
                    "type_id": record["type_id"]
                })
            return path_list

    def get_all_traffic_logs(self):
        cypher_query = """
        MATCH (c:Car)-[r:PASSED]->(cam:Camera)
        RETURN c.plate_number as plate, 
               cam.name as camera_name, 
               r.timestamp as timestamp, 
               c.type_id as type_id
        ORDER BY r.timestamp DESC
        LIMIT 100
        """
        
        if not self.driver:
            return []

        with self.driver.session() as session:
            result = session.run(cypher_query)
            
            data_list = []
            for record in result:
                data_list.append({
                    "plate": record["plate"],
                    "camera": record["camera_name"],
                    "timestamp": str(record["timestamp"]),
                    "type_id": record["type_id"]
                })
            return data_list

    def get_traffic_by_plate_number_path(self, plate_number):
        cypher_query = """
        MATCH path = (c:Car {plate_number: $plate_number})-[:PASSED*]->(cam)
        RETURN [node IN nodes(path) | node.name] as cameras
        LIMIT 10
        """
        
        if not self.driver:
            return None

        with self.driver.session() as session:
            result = session.run(cypher_query, {"plate_number": plate_number})
            single_record = result.single()
            if single_record:
                return single_record["cameras"]
            return None

    def close(self):
        if self.driver:
            self.driver.close()

graph_service = GraphService()