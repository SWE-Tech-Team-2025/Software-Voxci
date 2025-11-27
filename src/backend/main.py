from esp32_wifi_communicator import WiFiCommunicator
from backend.database_comm import DataBaseComm
from backend.excel_export import Exporter
from backend.routes import router
import uuid
import pydantic
from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import jwt
import logging
import os
import signal

app = FastAPI()

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

    def run():
        communicator = WiFiCommunicator(max_buffer_sz=256)
        database_comm = DataBaseComm()

        app.include_router(router)

        logging.info("[Startup] Starting Application.....")
        
        return