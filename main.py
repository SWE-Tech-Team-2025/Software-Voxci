from typing import BaseModel
from fastapi import FastAPI

app = FastAPI()

class CreateDieInput(BaseModel):
    id: str
    name: str


#Fetches die serial numbers and names
@app.get("/dies")
def get_dies():
    return {"Hello": "World"}

#Fetches data sweeps for the die
@app.get("/dies/{die_id}")
def get_die(die_id: str):
    return {"Hello": "World"}

#Creates a new die 
@app.post("/dies")
def create_die(die: CreateDieInput):
    return {"id": die.id}

#Adds a sweep to existing die
@app.post("/dies/{die_id}/sweeps")
def add_die_sweep(die_id: str):
    return {"Hello": "World"}

#Deletes all sweeps
@app.delete("/dies/{die_id}")
def delete_die(die_id: str):
    return {"Hello": "World"}