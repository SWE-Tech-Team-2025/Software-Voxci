import os
from pydantic import BaseModel
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import jwt
from jwt import encode as jwt_encode
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from bson import ObjectId

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

    # Example of searching the database for a specific object or field
    # print(collection.insert_one({"name" : "Samantha"}))
    # for die in collection.find({"name" : "Samantha"}):
    #     print(die)
    
    # Creates a die input in the database
    def create_die(self, die_id : str) -> None:
        dies.insert_one({"ID" : die_id, "currtestnum" : 1})

    # Fetches a die from the database
    def get_die(self, die_id : str) -> None:
        return dies.find({"ID" : die_id})

    # Increments testnum for a specific die
    def increment_die_testnum(self, die_id : str) -> None:
        die_query = {"ID" : die_id}
        die_new_test_val = {"inc" : {"currtestnum"}}
        dies.update_one(die_query, die_new_test_val)

    # Returns the specified die's testnum for use in generating sweeps
    def get_die_testnum(self, die_id : str) -> int:
        die = dies.find({"ID" : die_id})
        return die[1]

    # Fetches all sweeps from the database that correspond to the die id
    def get_die_sweeps(self, die_id, test_num) -> list:
        die_sweeps_list = list()
        for die_sweep in die_sweeps.find({"ID" : die_id, "testnum" : test_num}):
            die_sweeps_list.append(die_sweep)
        return die_sweeps_list
    
    # Creates a new sweep for the die and adds it to the database
    def create_die_sweep(self, die_id : str, test_num : int, sweep_voltage : float, sweep_humidity : float, sweep_temp : float, sweep_capacitance : float) -> None:
        new_sweep = { "ID" : die_id, "testnum" : test_num , "timestamp" : datetime.now(), "humidity" : sweep_humidity, "voltage" : sweep_voltage, "capacitance" : sweep_capacitance, "temp" : sweep_temp}
        die_sweeps.insert_one(new_sweep)


# class CreateDieInput(BaseModel):
#     id: str
#     name: str

#     # Fetches die serial numbers and names
#     @app.get("/dies")
#     def get_dies():
#         return {"Hello": "World"}

#     # Fetches data sweeps for the die
#     @app.get("/dies/{die_id}")
#     def get_die(die_id: str):
#         dies = db["dies"]
#         for die in dies.find({"name" : die_id}):
#             print(die)
#         return {"Hello": "World"}

#     # Fetches die serial numbers and names
#     @app.get("/dies")
#     def get_dies():
#         return {"Hello": "World"}

#     # Fetches data sweeps for the die
#     @app.get("/dies/{die_id}")
#     def get_die(die_id: str):
#         return {"Hello": "World"}

#     # Creates a new die 
#     @app.post("/dies")
#     def create_die(die: CreateDieInput):
#         return {"id": die.id}

#     # Adds a sweep to existing die
#     @app.post("/dies/{die_id}/sweeps")
#     def add_die_sweep(die_id: str, sweep: float):
#         die_sweeps.insert_one(die_id, sweep)
#         return {"Hello": "World"}

#     # Deletes all sweeps
#     @app.delete("/dies/{die_id}")
#     def delete_die(die_id: str):
#         return {"Hello": "World"}

#     # Creates a new die 
#     @app.post("/dies")
#     def create_die(die: CreateDieInput):
#         return {"id": die.id}

#     # Adds a sweep to existing die
#     @app.post("/dies/{die_id}/sweeps")
#     def add_die_sweep(die_id: str):
#         return {"Hello": "World"}

#     # Deletes all sweeps
#     @app.delete("/dies/{die_id}")
#     def delete_die(die_id: str):
#         return {"Hello": "World"}