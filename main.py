from esp32_wifi_communicator import WiFiCommunicator
from database_comm import DataBaseComm
from excel_export import Exporter
import uuid
import pydantic
from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import jwt
from jwt import encode as jwt_encode

class Main:
    curr_chip_id = "empty"
    communicator = None
    database_comm = None
    def new_die(self)-> str:
        curr_chip_id = uuid4()
        database_comm.dies.create_die(curr_chip_id)
        return curr_chip_id

    def export_Die(self, die_id : str, test_num : int) -> None:
        write_data(die_id, test_num)
        
    def connect_esp32(self, ip_addr : str) -> bool:
        
        return true # TODO: Change this
    

    def main():
        communicator = WiFiCommunicator(max_buffer_sz=128)
        database_comm = DataBaseComm()
        return

    def run():
        return       

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