from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "assessment_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
employees_collection = db["employees"]
users_collection = db["users"]

# employee data validation rules
employee_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["employee_id", "name", "department", "salary"],
        "properties": {
            "employee_id": {
                "bsonType": "string",
                "description": "Employee ID must be string"
            },
            "name": {
                "bsonType": "string",
                "minLength": 2,
                "maxLength": 100,
                "description": "Name between 2-100 chars"
            },
            "department": {
                "bsonType": "string", 
                "enum": ["Engineering", "HR", "Finance", "Marketing", "Operations", "Electronics"],
                "description": "Must be valid department"
            },
            "salary": {
                "bsonType": "number",
                "minimum": 0,
                "maximum": 1000000,
                "description": "Salary must be positive"
            },
            "skills": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                },
                "description": "Skills array"
            },
            "joining_date": {
                "bsonType": "date",
                "description": "Valid date"
            }
        }
    }
}

def setup_schema_validation():
    """setup validation rules"""
    try:
        # check if collection exists
        collections = db.list_collection_names()
        if "employees" in collections:
            # modify existing
            db.command("collMod", "employees", validator=employee_schema)
        else:
            # create new with validation
            db.create_collection("employees", validator=employee_schema)
        print("Schema validation applied successfully")
    except Exception as e:
        print(f"Schema validation setup failed: {e}")

def setup_db_indexes():
    """setup db indexes for performance"""
    employees_collection.create_index("employee_id", unique=True)
    employees_collection.create_index("department") 
    employees_collection.create_index([("skills", "text")])

try:
    setup_db_indexes()
    setup_schema_validation()
except Exception:
    pass  
