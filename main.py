from esp32_wifi_communicator import WiFiCommunicator
from database_comm import DataBaseComm
import uuid

class Main:
    curr_chip_id = "empty"
    communicator = WiFiCommunicator(max_buffer_sz=128)
    database_comm = DataBaseComm()
    def new_die_test()-> str:
        curr_chip_id = uuid4()
        database_comm.dies.create_die(curr_chip_id)
        
        return curr_chip_id

    def main():
        return

    def run():
        return       