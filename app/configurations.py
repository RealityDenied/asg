from pymongo import MongoClient

# Local MongoDB connection (default port 27017)
MONGO_URI = "mongodb://localhost:27017/"

DB_NAME = "assessment_db"

# Connect to local MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

employees_collection = db["employees"]
