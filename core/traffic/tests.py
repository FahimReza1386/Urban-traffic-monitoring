# Django Imports
from django.test import TestCase
from datetime import datetime
# Third-Party Imports
from neo4j import GraphDatabase

# Locale Imports
from traffic.models import TrafficLogs, Cameras

class TrafficTestCase(TestCase):
    """
    
        A Class For Testing The Models
    
    """
    def __init__(self, *args, **kwargs):
        self.db = self.connection_db()
        super().__init__(*args, **kwargs)
    
    def connection_db(self):
        """
            for connection to database
        """
        driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "traffic@2684"))
        return driver  
     
    def setUp(self):
        """
            this obj creating for testing
        """
        camera=Cameras.objects.create(
            name="تست ۱۴۰۴"
        )
        TrafficLogs.objects.create(
        plate_number="۳۲ ت ۳۲۲ ۳۲",
        camera_id = camera,
        timestamp= datetime.utcnow(),
        type_id = 2
        )
        
        return super().setUp()
    
    
    def test_camera_creation(self):
        """
            this creating camera test 
        """

        params = {
            'name' : "تست ۱۴۰۴"
        }
        
        cypher_get_camera = """
        MATCH (c:Camera)
        WHERE c.name=$name
        RETURN c.id as camera_id, c.name as camera_name
        """
        with self.db.session() as session:
            result = session.run(cypher_get_camera, params)
            record = result.single()
            self.assertIsNotNone(record)
            self.assertEqual(record["camera_name"], params["name"])
    
    def test_traffic_log_creation(self):  
        """
            this creating traffic test 
        """   
        params = {
            'plate_number': "۳۲ ت ۳۲۲ ۳۲",
            'camera_id': 1332,
            'type_id': 2
        }
        
        cypher_get_car_query = """
        MATCH (cam:Camera)-[r:PASSED]->(c:Car)
        WHERE c.plate_number= $plate_number AND c.type_id=$type_id
        RETURN c.plate_number AS plate_number, c.timestamp AS timestamp, cam.id AS camera_id, c.type_id AS type_id
        """
     
        with self.db.session() as session:
            result = session.run(cypher_get_car_query, params)
            record = result.single()
            self.assertIsNotNone(record)
            self.assertEqual(record["plate_number"], "۳۲ ت ۳۲۲ ۳۲")
            self.assertEqual(record["type_id"], 2)
            
    def test_get_traffic_list(self):
        """
            this creating traffic log path test 
        """
        traffic_path_query = """
            MATCH (cam:Camera)-[r:PASSED]->(c:Car)
            WHERE c.plate_number STARTS WITH $plate_number AND c.type_id=$type_id
            ORDER BY r.timestamp ASC
            RETURN c.plate_number, c.type_id, r.id, r.timestamp
        """
        
        params = {
            'plate_number': '۳۲',
            'type_id' : 2
        }
        
        with self.db.session() as session:
            result=session.run(traffic_path_query, params)
            record=result.single()
            self.assertIsNotNone(record)

    
    def test_traffic_suspicious_creation(self):
        """
            this creating suspicious vehicle test 
        """    
        camera = Cameras.objects.create(
            name="میدان علی"
        )
        log = TrafficLogs.objects.create(
        plate_number="۳۲ ت ۳۲۲ ۳۲",
        camera_id = camera,
        timestamp= datetime.utcnow(),
        type_id = 4
        )
        params = {
            'plate_number': log.plate_number,
            'camera_id': log.camera_id.id,
            'type_id': log.type_id
        }
        
        cypher_get_car_query = """
        MATCH (cam:Camera)-[r:PASSED]->(c:suspicious)
        WHERE c.plate_number= $plate_number AND c.type_id=$type_id
        RETURN c.plate_number AS plate_number, c.timestamp AS timestamp, cam.id AS camera_id, c.type_id AS type_id
        """
     
        with self.db.session() as session:
            result = session.run(cypher_get_car_query, params)
            record = result.single()
            self.assertIsNotNone(record)
            
    @classmethod
    def tearDownClass(self):
        """
            for close the connection
        """
        if hasattr(self, 'driver'):
            self.db.driver.close() 
            
        