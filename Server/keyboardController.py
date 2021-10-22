from ctypes import *

class keyboardController():
    def __init__(self, clientSocket):
        self.client = clientSocket

    def lockKeyboard():
        while True:
            windll.user32.BlockInput(True);

    def unlockKeyboard():
        windll.user32.BlockInput(False); 