# Django Imports
from django.conf import settings

# Third-Party Imports
from neo4j import GraphDatabase
from rest_framework import status
from rest_framework.response import Response

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
        
    def get_traffic_by_plate_number_path(self, plate_number=None, page_number=1, limit=10):
        if plate_number != None:
            cypher_query = """ 
            MATCH (cam)-[r:PASSED]->(c:Car {plate_number: $plate_number})
            RETURN cam.name AS camera, r.timestamp AS timestamp, c.type_id AS type_id, r.id AS id , c.plate_number AS plate_number
            ORDER BY timestamp DESC
            SKIP $skipValue
            LIMIT $limit
            """
        else:
            cypher_query = """ 
            MATCH (cam)-[r:PASSED]->(c:Car)
            RETURN cam.name AS camera, r.timestamp AS timestamp, c.type_id AS type_id, r.id AS id , c.plate_number AS plate_number
            ORDER BY timestamp DESC
            SKIP $skipValue
            LIMIT $limit
            """
        
        skip_value = max(page_number - 1, 0) * limit

        if not self.driver:
            return []

        with self.driver.session() as session:
            result = session.run(
                cypher_query,
                {"plate_number": plate_number, "skipValue": skip_value, "limit": limit}
            )

            path_list = []
            for record in result:
                path_list.append({
                    "id" : record["id"],
                    "plate_number" : record["plate_number"],
                    "camera": record["camera"],
                    "timestamp": str(record["timestamp"]),
                    "type_id": record["type_id"]
                })

            return path_list
    
    def get_suspicious_vehicles(self, page_number, limit):
        skip_value = (limit - 1) * page_number

        cypher_query = """
        MATCH (c:Car)
        WITH c.plate_number AS plate_number, COLLECT(DISTINCT c.type_id) AS type_ids
        WHERE SIZE(type_ids) > 1
        RETURN plate_number, type_ids
        ORDER BY plate_number
        SKIP $skip_value
        LIMIT $page_size
        """
        
        params = {
            'skip_value': skip_value,
            'page_size': limit
        }

        if not graph_service.driver:
            return Response({"error": "Neo4j driver not initialized"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        with graph_service.driver.session() as session:
            result = session.run(cypher_query, params)
            data = []
            for record in result:
                data.append({
                    "plate_number": record["plate_number"],
                    "type_ids": record["type_ids"]
                })

            return data
    def delete_all_data(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        
    def get_all_traffic_logs(self, page_number, limit):
        cypher_query = """
        MATCH (cam)-[r:PASSED]->(c:Car)
        RETURN cam.name AS camera, r.timestamp AS timestamp, c.type_id AS type_id, c.plate_number AS plate_number, c.id AS id
        ORDER BY timestamp DESC
        SKIP $skipValue
        LIMIT $limit
        """
        skip_value = max(page_number - 1, 0) * limit
        
        with self.driver.session() as session:  
            result = session.run(
                cypher_query,
                {
                    "skipValue": skip_value, "limit": limit
                }
            )
            return [
            {
                "id" : record["id"],
                "plate_number": record["plate_number"],
                "camera": record["camera"],
                "timestamp": str(record["timestamp"]),
                "type_id": record["type_id"]
            }
            for record in result
            ]
            
    def close(self):
        if self.driver:
            self.driver.close()

graph_service = GraphService()