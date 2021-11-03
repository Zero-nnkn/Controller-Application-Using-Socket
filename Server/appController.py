import os, signal
import subprocess
import json

class AppController():
    def __init__(self, clientSocket):
        self.appList = []
        self.__client = clientSocket

    def startListening(self):
        request = ""
        while True:
            request = self.self.__client.recv(1024).decode("utf-8")
            if not request:
                break
            if request == "view":
                self.viewList()
            elif request == "kill":   
                self.killApp()
            elif request == "start":   
                self.startApp()
            else: #Quit
                return

    def process2List(self,processes):
        a = processes.decode().strip()
        b = a.split("\r\n")
        b = [" ".join(x.split()) for x in b]
        c = [x.split() for x in b][2:]
        return c

    def viewList(self):
        app = subprocess.check_output(
            "powershell gps | where {$_.MainWindowTitle} | \
            select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}",
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        self.appList = self.process2List(app)

        dataToSend = json.dumps(self.appList).encode('utf-8') 
        size = len(dataToSend)
        self.__client.send(str(size).encode('utf-8'))
        check = self.__client.recv(10)
        self.__client.send(dataToSend)

    def killApp(self):
        buffer = ""
        buffer = self.__client.recv(1024).decode("utf-8")
        if buffer == "KillID":
            IDtoKill = self.__client.recv(10).decode('utf-8')
            test = False
            for app in self.appList:
                if IDtoKill==app[1]:
                    try:
                        os.kill(int(IDtoKill), signal.SIGTERM) 
                        s = "Success"
                        self.__client.send(s.encode('utf-8'))
                    except:
                        s = "Error"
                        self.__client.send(s.encode('utf-8'))
                    test = True
            if test==False:
                s = "No App Found"
                self.__client.send(s.encode('utf-8'))
        else:
            return

    def startApp(self):
        buffer = ""
        buffer = self.__client.recv(1024).decode("utf-8")
        if buffer == "StartID":
            ProcessToStart = self.__client.recv(1024).decode('utf-8') + ".exe"
            try:
                PathProcess = os.path.relpath(ProcessToStart)
                os.startfile(PathProcess)
                s = "Success"
                self.__client.send(s.encode('utf-8'))
            except:
                s = "Error"
                self.__client.send(s.encode('utf-8'))
        else:
            return


import win32con
import win32gui
import win32process

def get_hwnds_for_pid ():
  def callback (hwnd, hwnds):
    if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
      #if found_pid == pid:
        name = win32gui.GetWindowText (hwnd)
        if(name != ""):
            hwnds.append ((found_pid, name))
    return True
    
  hwnds = []
  win32gui.EnumWindows (callback, hwnds)
  return hwnds

print(set(get_hwnds_for_pid()))
