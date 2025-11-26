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
import logging
import os
import signal

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
        app = FastAPI()

        logging.info("[Startup] Starting Application.....")
        
        return