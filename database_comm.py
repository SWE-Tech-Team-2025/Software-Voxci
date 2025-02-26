import os
from pydantic import BaseModel
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv

class DataBaseComm:

    '''
    TODO: Complete implementation for the database communicator so we can read and write
    data to the database as we get it from the ESP32
    '''

    def __init__(self) -> None:
        self

        # Load the .env to get the database connection
        # and initialize the database client
        load_dotenv()
        self.app = FastAPI()
        self.client = MongoClient(os.getenv("MONGODB_URI"))

        # Create a db object to get a certain section of the database
        self.db = client["data"]
        self.dies = db["dies"]
        self.die_sweeps = db["die_sweeps"]

    # Fetches die serial numbers and names
    @app.get("/dies")
    def get_dies():
        return {"Hello": "World"}

    # Fetches data sweeps for the die
    @app.get("/dies/{die_id}")
    def get_die(die_id: str):
        dies = db["dies"]
        for die in dies.find({"name" : die_id}):
            print(die)
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
    def add_die_sweep(die_id: str, sweep: float):
        die_sweeps.insert_one(die_id, sweep)
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

    # Example of searching the database for a specific object or field
    # print(collection.insert_one({"name" : "Samantha"}))
    for die in collection.find({"name" : "Samantha"}):
        print(die)

class CreateDieInput(BaseModel):
    id: str
    name: str