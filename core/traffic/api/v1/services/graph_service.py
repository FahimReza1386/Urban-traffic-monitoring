# Django Imports
from django.conf import settings

# Third-Party Imports
from neo4j import GraphDatabase
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime

# hello world
"""
    GraphService : 
        A general service made up of various functions that work with the database, including
        receiving TrafficLogs and receiving suspicious vehicles.
"""
class GraphService:
    def __init__(self):
        
        """
            This is the database connection with the username and password in the settings.
        """
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_CONFIG['uri'],
                auth=settings.NEO4J_CONFIG['auth']
            )
            self.driver.verify_connectivity()
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")
            self.driver = None
        
    def get_traffic_by_plate_number_path(self, plate_number=None, page=1, per_page=10, type_id=None, start_date=None, end_date=None, order_by=None):
        
        """
            A function to capture vehicle traffic :
                To use filtering, you can enter the specified parameters.
        """
        
        
        skip_value = max(page - 1, 0) * per_page

        where_clauses = []
        params = {
            "skipValue": skip_value,
            "per_page": per_page,
        } 

        if plate_number:
            where_clauses.append("c.plate_number STARTS WITH $plate_number")
            params["plate_number"] = plate_number

        if type_id is not None:
            where_clauses.append("c.type_id = $type_id")
            params["type_id"] = int(type_id)
          
        if start_date is not None:
            where_clauses.append("r.timestamp >= $start_date")
            params["start_date"] = start_date
            
        if end_date is not None:
            where_clauses.append("r.timestamp <= $end_date")
            params["end_date"] = end_date

        where_str = " AND ".join(where_clauses)
        where_clause = f"AND {where_str}" if where_str else ""   

        cypher_count = f""" 
        MATCH ()-[r]->()
        RETURN count(r) AS total
        """
        
        if where_clauses :
            cypher_count = f""" 
            MATCH (c:Car)<-[r]-()
            WHERE 1=1 {where_clause }
            RETURN count(r) AS total
            """
       
        cypher_query = f"""
            MATCH (cam:Camera)-[r:PASSED]->(c:Car)
            USING INDEX r:PASSED(timestamp)
            WHERE r.timestamp IS NOT NULL
            RETURN 
                cam.name           AS camera,
                r.timestamp        AS timestamp,
                c.type_id          AS type_id,
                r.id               AS car_node_id,
                c.plate_number     AS plate_number
            
            ORDER BY r.timestamp {order_by if order_by is not None else "ASC"}
            SKIP $skipValue
            LIMIT $per_page
            """
        
        if where_clauses :
            cypher_query = f"""
                MATCH (cam:Camera)-[r:PASSED]->(c:Car)
                WHERE r.timestamp IS NOT NULL
                {where_clause}
                RETURN 
                    cam.name           AS camera,
                    r.timestamp        AS timestamp,
                    c.type_id          AS type_id,
                    r.id               AS car_node_id,
                    c.plate_number     AS plate_number
                
                ORDER BY r.timestamp {order_by if order_by is not None else "ASC"}
                SKIP $skipValue
                LIMIT $per_page
                """
        
        skip_value = max(page - 1, 0) * per_page
        if not self.driver:
            return {
                "results": path_list,
                "current_page": page,
                "first_item": first_item_id,
                "has_pages": page < total_pages,
                "last_item": last_item_id,
                "last_page": total_pages,
                "on_first_page": page == 1,
                "on_last_page": page >= total_pages,
                "per_page": per_page,
                "total" : total,
                "total_pages": total_pages,
            }
        with self.driver.session() as session:
            total_result = session.run(cypher_count, params).single()
            total = total_result['total'] if total_result else 0
            
            
    
            result = session.run(cypher_query, params)
            path_list = []
            for record in result:
                path_list.append({
                    "id" : record["car_node_id"],
                    "plate_number" : record["plate_number"],
                    "camera": record["camera"],
                    "timestamp": str(record["timestamp"]),
                    "type_id": record["type_id"]
                })
        
            total_pages = (total + per_page - 1) // per_page

            first_item_id  = path_list[0]["id"] if path_list else None
            last_item_id = path_list[-1]["id"] if path_list else None

            return {
                "results": path_list,
                "current_page": page,
                "first_item": first_item_id,
                "has_pages": page < total_pages,
                "last_item": last_item_id,
                "last_page": total_pages,
                "on_first_page": page == 1,
                "on_last_page": page >= total_pages,
                "per_page": per_page,
                "total" : total,
                "total_pages": total_pages
            }
    def get_suspicious_vehicles(self, plate_number, page=1, per_page=10, type_id=None, start_date=None, end_date=None, order_by=None):
        """
            Get suspicious car or vehicles : 
                    It is a function to catch suspicious vehicles.
                    You can use the specified parameters for filtering.
        """
        
        skip_value = max(page - 1, 0) * per_page
        where_clauses = []
        params = {
            "skipValue": skip_value,
            "per_page": per_page,
        } 

        if plate_number:
            where_clauses.append("c.plate_number STARTS WITH $plate_number")
            params["plate_number"] = plate_number

        if type_id is not None:
            where_clauses.append("c.type_id = $type_id")
            params["type_id"] = int(type_id)
          
        if start_date is not None:
            where_clauses.append("r.timestamp >= $start_date")
            params["start_date"] = start_date
            
        if end_date is not None:
            where_clauses.append("r.timestamp <= $end_date")
            params["end_date"] = end_date

        where_str = " AND ".join(where_clauses)
        where_clause = f"AND {where_str}" if where_str else ""   

        cypher_count = f""" 
        MATCH ()-[r]->()
        RETURN count(r) AS total
        """
        
        if where_clauses :
            cypher_count = f""" 
            MATCH (c:suspicious)<-[r]-()
            WHERE 1=1 {where_clause }
            RETURN count(r) AS total
            """
       
        cypher_query = f"""
            MATCH (cam:Camera)-[r:PASSED]->(c:suspicious)
            USING INDEX r:PASSED(timestamp)
            WHERE r.timestamp IS NOT NULL
            RETURN 
                cam.name           AS camera,
                r.timestamp        AS timestamp,
                c.type_id          AS type_id,
                r.id               AS suspicious_node_id,
                c.plate_number     AS plate_number
            
            ORDER BY r.timestamp {order_by if order_by is not None else "ASC"}
            SKIP $skipValue
            LIMIT $per_page
            """
        
        if where_clauses :
            cypher_query = f""" 
                MATCH (cam:Camera)-[r:PASSED]->(c:suspicious)
                WHERE r.timestamp IS NOT NULL
                {where_clause}
                RETURN 
                    cam.name           AS camera,
                    r.timestamp        AS timestamp,
                    c.type_id          AS type_id,
                    r.id               AS suspicious_node_id,
                    c.plate_number     AS plate_number
                
                ORDER BY r.timestamp {order_by if order_by is not None else "ASC"}
                SKIP $skipValue
                LIMIT $per_page
                """
        if not self.driver:
            return {
                "results": path_list,
                "current_page": page,
                "first_item": first_item_id,
                "has_pages": page < total_pages,
                "last_item": last_item_id,
                "last_page": total_pages,
                "on_first_page": page == 1,
                "on_last_page": page >= total_pages,
                "per_page": per_page,
                "total" : total,
                "total_pages": total_pages
            }
        with self.driver.session() as session:
            total_result = session.run(cypher_count, params).single()
            # total = 5000
            total = total_result['total'] if total_result else 0
            
            
    
            result = session.run(cypher_query, params)
            path_list = []
            for record in result:
                path_list.append({
                    "id" : record["suspicious_node_id"],
                    "plate_number" : record["plate_number"],
                    "camera": record["camera"],
                    "timestamp": str(record["timestamp"]),
                    "type_id": record["type_id"]
                })
        
            total_pages = (total + per_page - 1) // per_page

            first_item_id  = path_list[0]["id"] if path_list else None
            last_item_id = path_list[-1]["id"] if path_list else None

            return {
                "results": path_list,
                "current_page": page,
                "first_item": first_item_id,
                "has_pages": page < total_pages,
                "last_item": last_item_id,
                "last_page": total_pages,
                "on_first_page": page == 1,
                "on_last_page": page >= total_pages,
                "per_page": per_page,
                "total" : total,
                "total_pages": total_pages
            }
    
    def delete_all_data(self):
        """
            A complete database deletion is used when changes are made to the database structure.
        """
        with self.driver.session() as session:
            cypher_test = """
            MATCH (n)
            WITH n LIMIT 10000
            DETACH DELETE n
            """
            session.run(cypher_test)
        
    def close(self):
        """
            To disconnect from the database when requests are finished
        """
        if self.driver:
            self.driver.close()

graph_service = GraphService()