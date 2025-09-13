from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "assessment_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
employees_collection = db["employees"]

def setup_db_indexes():
    """Setup database indexes , will give better performance"""
    
    employees_collection.create_index("employee_id", unique=True)
    
    #  filtering
    employees_collection.create_index("department")
    
    # skills searchx
    employees_collection.create_index([("skills", "text")])

try:
    setup_db_indexes()
except Exception:
    pass  
