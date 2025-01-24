# Libraries required for the backend code
import pyfirmata

# Global variables for Arduino control
board = pyfirmata.Arduino('ACM0')
it = pyfirmata.util.Iterator(board)
it.start()

