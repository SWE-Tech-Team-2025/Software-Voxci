from fastapi import APIRouter
from services import process_data

router = APIRouter()

class CreateDieInput(BaseModel):
    id: str
    name: str

    # Fetches die serial numbers and names
    @router.get("/dies")
    def get_dies():
        return {"Hello": "World"}

    # Fetches data sweeps for the die
    @router.get("/dies/{die_id}")
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