# Database communication code for a MongoDB instance. Works for a local instance
# and for cloud instances. The only thing needing to be changed in either case is
# the .env file

import os
import pydantic
import fastapi
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime


class DataBaseComm:

    '''
    Implementation for the database communication. Handles creating and getting
    dies from the database as well as adding the individual sweeps to each die
    as testing is ongoing. 
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
    
    # Creates a die input in the database. Each die has a UUID attached to it
    def create_die(self, die_id : str) -> None:
        dies.insert_one({"ID" : die_id, "currtestnum" : 1})

    # Fetches a die from the database by searching for the UUID
    def get_die(self, die_id : str) -> None:
        return dies.find({"ID" : die_id})

    # Increments testnum for a die given the UUID. The testnum is incremented when
    # a new test is done on the die
    def increment_die_testnum(self, die_id : str) -> None:
        die_query = {"ID" : die_id}
        die_new_test_val = {"inc" : {"currtestnum" : 1}}
        dies.update_one(die_query, die_new_test_val)

    # Returns the specified die's testnum for use in generating sweeps so that the 
    # sweeps for one test can be distinguished from another test
    def get_die_testnum(self, die_id : str) -> int:
        die = dies.find_one({"ID" : die_id})
        return die["currtestnum"] if die else None

    # Fetches all sweeps from the database that correspond to the die id and testnum
    def get_die_sweeps(self, die_id, test_num) -> list:
        die_sweeps_list = list()

        # If test_num == -1, we want all of the sweeps associated with the die
        if test_num == -1:
            # Get current die number
            num = get_die_testnum({"ID": die_id})
            # Get all sweeps for the die ID
            for i in range(num):
                for die_sweep in die_sweeps.find({"ID" : die_id, "testnum" : num}):
                    die_sweeps_list.append(die_sweep)
        else: 
            # Get all sweeps for a specified die ID and test_num
            for die_sweep in die_sweeps.find({"ID" : die_id, "testnum" : test_num}):
                die_sweeps_list.append(die_sweep)
        return die_sweeps_list
    
    
    # Creates a new sweep for the die and adds it to the database
    def create_die_sweep(self, die_id : str, test_num : int, sweep_voltage : float, sweep_humidity : float, sweep_temp : float, sweep_capacitance : float) -> None:
        new_sweep = { "ID" : die_id, "testnum" : test_num , "timestamp" : datetime.now(), "humidity" : sweep_humidity, "voltage" : sweep_voltage, "capacitance" : sweep_capacitance, "temp" : sweep_temp}
        die_sweeps.insert_one(new_sweep)