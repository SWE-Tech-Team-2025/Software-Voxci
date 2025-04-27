from esp32_wifi_communicator import WiFiCommunicator
from database_comm import DataBaseComm
import uuid

# Tester file to ensure proper functionality of all code

# Testing esp_32_wifi_communicator

def main() -> None:
    test_esp_comm = WiFiCommunicator(128, 11111)