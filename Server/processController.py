import os, signal
import subprocess
import json

def processController():
    def __init__(self, clientSocket):
        self.processList = []
        self.client = clientSocket

    def process2List(self,processes):
        a = processes.decode().strip()
        b = a.split("\r\n")
        b = [" ".join(x.split()) for x in b]
        c = [x.split() for x in b][2:]
        return c

    def viewList(self):
        proc = subprocess.check_output("powershell gps | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}",stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processList = self.process2List(proc)

        dataToSend = json.dumps(self.processList).encode('utf-8') 
        size = len(dataToSend)
        self.client.send(str(size).encode('utf-8'))
        check = self.client.recv(10)
        self.client.send(dataToSend)

    def killProcess(self):
        buffer = ""
        buffer = self.client.recv(1024).decode("utf-8")
        if buffer == "KillID":
            IDtoKill = self.client.recv(10).decode('utf-8')
            test = False
            for process in self.processList:
                if IDtoKill == process[1]:
                    try:
                        os.kill(int(IDtoKill),signal.SIGTERM)
                        s = "Success"
                        self.client.send(s.encode('utf-8'))
                    except:
                        s = "Error"
                        self.client.send(s.encode('utf-8'))
                    test = True
            if test == False:
                s = "Error"
                self.client.send(s.encode('utf-8'))
        else:
            return
    
    def startProcess(self):
        buffer = ""
        buffer = self.client.recv(1024).decode("utf-8")
        if buffer == "StartID":
            ProcessToStart = self.client.recv(1024).decode('utf-8') + ".exe"
            try:
                PathProcess = os.path.relpath(ProcessToStart)
                os.startfile(PathProcess)
                s = "Success"
                self.client.send(s.encode('utf-8'))
            except:
                s = "Error"
                self.client.send(s.encode('utf-8'))
        else:
            return

