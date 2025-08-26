from pymongo import MongoClient
import os

# Configuración de MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
DATABASE_NAME = "flight_management"
COLLECTION_NAME = "flights"

class Database:
    client = None
    database = None

def get_database():
    if Database.client is None:
        Database.client = MongoClient(MONGO_URL)
        Database.database = Database.client[DATABASE_NAME]
    return Database.database

def get_flights_collection():
    database = get_database()
    return database[COLLECTION_NAME]