import os
from pydantic import BaseModel
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv

class DataBase_Comm:

    '''
    TODO: Complete implementation for the database communicator so we can read and write
    data to the database as we get it from the ESP32
    '''

    def __init__(self) -> None:
        self

# Load the .env to get the database connection
# and initialize the database client
load_dotenv()
app = FastAPI()
client = MongoClient(os.getenv("MONGODB_URI"))

# Create a db object to get a certain section of the database
db = client["data"]
collection = db["dies"]

# Example of searching the database for a specific object or field
# print(collection.insert_one({"name" : "Samantha"}))
for die in collection.find({"name" : "Samantha"}):
    print(die)

class CreateDieInput(BaseModel):
    id: str
    name: str

# Fetches die serial numbers and names
@app.get("/dies")
def get_dies():
    return {"Hello": "World"}

# Fetches data sweeps for the die
@app.get("/dies/{die_id}")
def get_die(die_id: str):
    return {"Hello": "World"}
# Fetches die serial numbers and names
@app.get("/dies")
def get_dies():
    return {"Hello": "World"}

# Fetches data sweeps for the die
@app.get("/dies/{die_id}")
def get_die(die_id: str):
    return {"Hello": "World"}

# Creates a new die 
@app.post("/dies")
def create_die(die: CreateDieInput):
    return {"id": die.id}

# Adds a sweep to existing die
@app.post("/dies/{die_id}/sweeps")
def add_die_sweep(die_id: str):
    return {"Hello": "World"}

# Deletes all sweeps
@app.delete("/dies/{die_id}")
def delete_die(die_id: str):
    return {"Hello": "World"}
# Creates a new die 
@app.post("/dies")
def create_die(die: CreateDieInput):
    return {"id": die.id}

# Adds a sweep to existing die
@app.post("/dies/{die_id}/sweeps")
def add_die_sweep(die_id: str):
    return {"Hello": "World"}

# Deletes all sweeps
@app.delete("/dies/{die_id}")
def delete_die(die_id: str):
    return {"Hello": "World"}