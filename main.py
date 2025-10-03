from esp32_wifi_communicator import WiFiCommunicator
from database_comm import DataBaseComm
from excel_export import Exporter
import uuid

class Main:
    curr_chip_id = "empty"
    communicator = WiFiCommunicator(max_buffer_sz=128)
    database_comm = DataBaseComm()
    def new_die(self)-> str:
        curr_chip_id = uuid4()
        database_comm.dies.create_die(curr_chip_id)
        return curr_chip_id

    def export_Die(self, die_id : str, test_num : int) -> None:
        write_data(die_id, test_num)
        
    def connect_esp32(self, ip_addr : str) -> bool:
        
        return true # TODO: Change this
    

    def main():
        return

    def run():
        return       