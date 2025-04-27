from esp32_wifi_communicator import WiFiCommunicator
from database_comm import DataBaseComm
import uuid
import time

# Tester file to ensure proper functionality of all code

# Testing esp_32_wifi_communicator

def main() -> None:
    test_esp_comm = WiFiCommunicator(128, 11111)
    test_esp_comm.send_message("test")
    time.sleep(0.1)
    out_message = test_esp_comm.get_message()
    if out_message == None:
        print("failed")
