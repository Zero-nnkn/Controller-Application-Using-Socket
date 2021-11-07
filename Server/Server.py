import socket
import tkinter as tk
import os, signal
from PIL import ImageGrab
import json
import subprocess
import sys
import ctypes

from mySocket import MySocket
import appController
import processController
import ftpController
import keyboardController
import macAddress
import powerController
import registryController
import streamingClient

PORT = 5000
PORT_STREAM = 5500

class Server(tk.Frame):
    def __init__(self, master = None):
        self.__running = False
        self.__host = ''
        self.__port = PORT
        self.__portStream = PORT_STREAM
        self.__client = None

        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    #DESIGN
    def createWidgets(self):      
        #Button1
        self.butConnect = tk.Button(self,text = "Open server", relief="groove")
        self.butConnect["command"] = self.buttonClick
        self.butConnect.place(x=50, y=15, height=70, width=100) 

    def Shutdown(self):
        os.system("shutdown /s /t 60")

    def Screenshot(self):
        while True:
            buffer = ""
            buffer = self.__client.recv(1024).decode("utf-8")
            if not buffer:
                break
            if buffer == "Take":
                img = ImageGrab.grab()
                imgToSend = img.tobytes()
                size = len(imgToSend)
                self.__client.send(str(size).encode('utf-8'))
                check = self.__client.recv(10)
                self.__client.send(str(img.size[0]).encode('utf-8'))
                check = self.__client.recv(10)
                self.__client.send(str(img.size[1]).encode('utf-8'))
                check = self.__client.recv(10)
                self.__client.send(imgToSend)
            else:
                break        

    def process2List(self,processes):
        a = processes.decode().strip()
        b = a.split("\r\n")
        b = [" ".join(x.split()) for x in b]
        c = [x.split() for x in b][2:]
        return c

    def AppRunning(self):
        Apps = []      
        while True:
            buffer = ""
            buffer = self.__client.recv(1024).decode("utf-8")
            if not buffer:
                break

            if buffer == "View":
                s = subprocess.check_output("powershell gps | where {$_.MainWindowTitle} | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}", stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                Apps = self.process2List(s)
                dataToSend = json.dumps(Apps).encode('utf-8') 
                size = len(dataToSend)
                self.__client.send(str(size).encode('utf-8'))
                check = self.__client.recv(10)
                self.__client.send(dataToSend)
            elif buffer == "Kill":
                while True:
                    buffer2 = ""
                    buffer2 = self.__client.recv(1024).decode("utf-8")
                    if buffer2 == "KillID":
                        IDtoKill = self.__client.recv(10).decode('utf-8')
                        test = False
                        for app in Apps:
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
                        break 
            elif buffer == "Start":
                while True:
                    buffer2 = ""
                    buffer2 = self.__client.recv(1024).decode("utf-8")
                    if buffer2 == "StartID":
                        AppToStart = self.__client.recv(1024).decode('utf-8') + ".exe"
                        try:
                            PathApp= os.path.relpath(AppToStart)
                            os.startfile(PathApp)
                            s = "Success"
                            self.__client.send(s.encode('utf-8'))
                        except:
                            s = "Error"
                            self.__client.send(s.encode('utf-8'))
                    else:
                        break
            else: #Quit
                return
    
    def ProcessRunning(self):
        Processes = []

        while True:
            buffer = ""
            buffer = self.__client.recv(1024).decode("utf-8")
            if not buffer:
                break

            if buffer == "View":
                s = subprocess.check_output("powershell gps | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}",stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                Processes = self.process2List(s)

                dataToSend = json.dumps(Processes).encode('utf-8') 
                size = len(dataToSend)
                self.__client.send(str(size).encode('utf-8'))
                check = self.__client.recv(10)
                self.__client.send(dataToSend)
            elif buffer == "Kill":
                while True:
                    buffer2 = ""
                    buffer2 = self.__client.recv(1024).decode("utf-8")
                    if buffer2 == "KillID":
                        IDtoKill = self.__client.recv(10).decode('utf-8')
                        test = False
                        for process in Processes:
                            if IDtoKill == process[1]:
                                try:
                                    os.kill(int(IDtoKill),signal.SIGTERM)
                                    s = "Success"
                                    self.__client.send(s.encode('utf-8'))
                                except:
                                    s = "Error"
                                    self.__client.send(s.encode('utf-8'))
                                test = True
                        if test == False:
                            s = "Error"
                            self.__client.send(s.encode('utf-8'))
                    else:
                        break 
            elif buffer == "Start":
                while True:
                    buffer2 = ""
                    buffer2 = self.__client.recv(1024).decode("utf-8")
                    if buffer2 == "StartID":
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
                        break
            else: #Quit
                return

    def KeyStroke(self):
        self.keyController.startListening()
        
    def buttonClick(self):
        self.__serverSocket = MySocket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serverSocket.bind((self.__host, self.__port))
        self.__serverSocket.listen(5)
        print("Waiting for connection...")
        self.__client, addr = self.__serverSocket.accept()

        self.appController = appController.AppController(self.__client)
        self.processController = processController.ProcessController(self.__client)
        self.ftpController = ftpController.FtpController(self.__client)
        self.keyboardController = keyboardController.KeyboardController(self.__client)
        self.macAddress = macAddress.MacAddress(self.__client)
        self.powerController = powerController.PowerController(self.__client)
        self.registryController = registryController.RegistryController(self.__client)
        self.screenShareClient = streamingClient.ScreenShareClient(addr[0],self.__portStream, self.__client)


        while True:

            buffer = ""
            buffer = self.__client.recv(1024)
            
            if not buffer:
                break
            message = buffer.decode('utf-8')

            if message == "APP":
                self.appController.startListening()
            elif message == "PROCESS":
                self.processController.startListening()
            elif message == "FTP":
                self.ftpController.startListening()
            elif message == "KEYBOARD":
                self.keyboardController.startListening()
            elif message == "MACADDRESS":
                self.macAddress.startListening()
            elif message == "POWER":
                self.powerController.startListening()
            elif message == "REGISTRY":
                self.registryController.startListening()
            elif message == "STREAM":
                self.screenShareClient.startListening()
            elif message == 'EXIT':
                self.__serverSocket.close()
                self.screenShareClient.stop_stream()
                break
            else:
                break
        self.__serverSocket.close()
        

def CloseButton(root):
    root.destroy()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
'''
if is_admin():
    # Code of your program here
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
    app = Server(root)
    app.master.title("Server")
    app.master.minsize(210, 100)
    app.mainloop()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
'''

root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
app = Server(root)
app.master.title("Server")
app.master.minsize(210, 100)
app.mainloop()
