import os
from pydantic import BaseModel
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from WiFiCommunicator import WiFiCommunicator


# Global Variables
int curr_chip_id = 0
 communicator = WiFiCommunicator(max_buffer_sz=256)

 