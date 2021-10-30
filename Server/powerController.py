import os
from ctypes import windll

class powerController():
    def __init__(self, clientSocket):
        self.__client = clientSocket

    def power(self):
        request = ""
        while True:
            request = self.self.__client.recv(1024).decode("utf-8")
            if not request:
                break
            if request == "shutdow":
                self.shutdown()
            elif request == "logout":   
                self.unhookKey()
            else: #Quit
                return

    def shutdown(self):
        os.system("shutdown /s /t 60")
    
    def logout(self):
        windll.user32.ExitWindowsEx(0, 1);