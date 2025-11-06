import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

uri = db_url = os.environ.get("mongo_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client.agenda_db 

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None
    db = None

# --- Create a Function to Get the DB ---
# This is what other files will import and call.
def get_db():
    """
    Returns the database instance.
    """
    if db is None:
        print("Database connection is not established.")
    return db

def get_tareas_collection():
    """
    Returns the 'tareas' collection instance.
    """
    if db is not None:
        return db.tareas
    return None