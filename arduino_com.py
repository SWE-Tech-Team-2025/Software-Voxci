import pyfirmata
import time

board = pyfirmata.Arduino('/dev/')
it = pyfirmata.util.Iterator(board)


