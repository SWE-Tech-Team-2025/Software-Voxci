from fastapi import APIRouter
from pydantic import BaseModel
import services
import backend.esp32_wifi_communicator
import backend.shared_shutdown
import backend.database_comm

router = APIRouter()

class Inputs(BaseModel):
    freq: float
    voltage: float

# Routing for the start button in the UI to send the message
# to start the test on the hardware side
@router.post("/start")
def start(data: Inputs):
    freq = OutMessage(data.freq, False, False)
    send_message(freq)

    volt = OutMessage(data.voltage, True, False)
    send_message(volt)

    send_start_stop(StartStopTestMsg(True, False))
    return

# Routing for the stop button in the UI to send the message
# to stop the test on the hardware side
@router.post("/stop")
def stop(data: Inputs):
    send_start_stop(StartStopTestMsg(False, False))
    return

# Routing for the export button to tell the backend to export the
# die and its sweeps to Excel
@router.post("/excel")
def export(data: Inputs):
    test_num = database_comm.dies.get_die_testnum(curr_chip_id)
    write_data(curr_chip_id, test_num)
    return

# Routing to send the shutdown message and shutdown the application
@router.post("/shutdown")
def shutdown(data: Inputs):
    shutdown()
    return

""" class CreateDieInput(BaseModel):
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
        return {"Hello": "World"} """