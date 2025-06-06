import time
import socket
import threading
from queue import Queue


class InMessage:
    '''
    Incoming Message definition
    NOTE: This is created so that you can add as many flags as you want,
    without changing the interface, and you'd only need to chance the decoding method
    Iniltializes incoming messages from the ESP32 to be added to the incoming message queue
    @param data: the value of the value read by the testing device
    @param client_addr: The address of the ESP32
    '''
    def __init__(self, data, require_ack: bool, client_addr: str) -> None:
        self.data = data
        self.require_acknowledgment = require_ack
        self.client_addr = client_addr


class OutMessage:
    '''
    Outgoing Message definition
    NOTE: This is created so that you can add as many flags as you want,
    without changing the interface, and you'd only need to chance the encoding method
    Initializes the outgoing message for the ESP32 to be added to the outgoing message queue
    @param type_of_message: true for voltage range, false for voltage increment value
    '''
    def __init__(self, data, type_of_message: bool, require_ack: bool = False) -> None:
        self.data = data

class StartStopTestMsg:
    '''
    Initializes a special type of outgoing message to tell the ESP32 to start/stop the tests as needed.
    @param data: true starts the test, false stops
    '''
    def __init__(self, data: bool, require_ack: bool = False) -> None:
        self.data = data
        self.require_ack = require_ack


class WiFiCommunicator:
    '''
    '''
    ACKNOWLEDGMENT_FLAG = 'A'
    CPU_RELEASE_SLEEP = 0.000_001

    def __init__(self, max_buffer_sz: int, port: int, in_queue_sz: int, out_queue_sz: int, start_stop_queue_sz: int) -> None:
        '''
        @param max_buffer_sz: The maximum amount of bytes to be received at once
        @param port: The port on which we shall communicate
        @param in_queue_sz: The incoming messages' queue size, if 0 -> infinite
        @param out_queue_sz: The outgoing messages' queue size, if 0 -> infinite
        '''
        assert max_buffer_sz > 0, f"Buffer size must be > 0 [{max_buffer_sz = }]"
        assert in_queue_sz >= 0, f"Queue size can't be negative [{in_queue_sz = }]"
        assert out_queue_sz >= 0, f"Queue size can't be negative [{out_queue_sz = }]"
        assert start_stop_queue_sz >= 0, f"Queue size can't be negative [{start_stop_queue_sz = }]"
        
        # Signal to the communicator to "Rest In Peace"
        self._rip = False
        self._have_client = False


        self._max_buffer_size = max_buffer_sz
        self._incoming_messages_queue = Queue(maxsize=in_queue_sz)
        self._outgoing_messages_queue = Queue(maxsize=out_queue_sz)
        self._start_stop_messages_queue = Queue(maxsize=start_stop_queue_sz)

        # Client info
        self._client = None
        self._client_address = None

        # Socket creation
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # To allow the ESP through the firewall (if u had firewall problems, and u're on Linux):
        # $ sudo iptables -I INPUT -s ESP.IP.GOES.HERE -p tcp --dport 15000 -j ACCEPT 
        soc.bind(('0.0.0.0', port))
        soc.listen(0)

        # Start the show
        self._threads = [
            threading.Thread(target=self.__listener_thread, daemon=True),
            threading.Thread(target=self.__sender_thread, daemon=True),
            threading.Thread(target=self.__wait_for_connection_thread, daemon=True, args=[soc]),
        ]
        for thread in self._threads:
            thread.start()

    def get_message(self) -> InMessage:
        '''
        Returns (if exists) a message from the incoming messages queue
        '''
        return self._incoming_messages_queue.get()

    def send_message(self, message: OutMessage) -> None:
        '''
        Adds a message to the sending queue to be sent
        @param message: The message to be sent to the ESP32
        '''
        self._outgoing_messages_queue.put(message)
        
    def send_start_stop(self, message: StartStopTestMsg) -> None:
        '''
        Tells the ESP32 to start or stop the tests
        @param message: The start/stop message to be sent to the ESP32
        '''
        self.start_stop_queue.put(message)

    def destroy(self):
        '''
        Destroy the communicator
        '''
        if self._client is not None:
            self._client.close()
        
        self._rip = True
        for thread in self._threads:
            thread.join(0.1)

    def __wait_for_connection_thread(self, soc: socket.socket) -> None:
        '''
        Establish a connection with a client, and die
        @param soc: socket to use to establish communication with
        '''
        self._client, self._client_address = soc.accept()
        self._have_client = True

    def __decode(self, in_bytes: bytes) -> 'None|InMessage':
        '''
        Decodes the incoming message to the required format
        @param in_bytes: The bytes that make up the message to decode
        '''
        message = in_bytes.decode()
        if not len(message):
            return None

        ack = message[0] == self.ACKNOWLEDGMENT_FLAG
        data = message[1 * ack:]
        return InMessage(data=data, require_ack=ack, client_addr=self._client_address)

    def __listener_thread(self):
        '''
        '''
        while not self._rip:
            if not self._have_client:
                time.sleep(self.CPU_RELEASE_SLEEP)
                continue

            message = self._client.recv(self._max_buffer_size)
            decoded_msg = self.__decode(message)
            if decoded_msg is not None:
                self._incoming_messages_queue.put(decoded_msg)

    def __encode(self, message: OutMessage) -> bytes:
        '''
        Encodes the outgoing message into the required sendable format
        @param message: The message to encode
        '''
        return message.data.encode()

    def __sender_thread(self):
        '''
        '''
        while not self._rip:
            if not self._have_client:
                time.sleep(self.CPU_RELEASE_SLEEP)
                continue

            # This is blocking on purpose, if not, we'd have to handle getting no-data when timing-out
            msg = self._outgoing_messages_queue.get()
            self._client.send(self.__encode(msg))