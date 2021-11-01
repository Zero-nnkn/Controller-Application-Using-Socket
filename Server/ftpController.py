import os
import psutil
import shutil
import json

CHUNKSIZE = 1_000_000

class FtpController():
    def __init__(self, clientSocket):
        self.__client = clientSocket
        self.currentPath = "\\"
        self.fileList = []
        self.folderList = []

    def startListening(self):
        self.getDrive()
        request = ""
        while True:
            request = self.self.__client.recv(1024).decode("utf-8")
            if not request:
                break
            if request=="view":
                info = self.self.__client.recv(1024).decode("utf-8")
                if(os.path.exists(os.path.join(self.currentPath, info))):
                    self.currentPath = os.path.join(self.currentPath, info)
                    self.sendFolderInfo(self.currentPath)
            elif request == "copy2server":
                info = self.self.__client.recv(1024).decode("utf-8")
                fullPath = os.path.join(self.currentPath, info)
                self.recvData(fullPath)
            elif request == "copy2client":
                info = self.self.__client.recv(1024).decode("utf-8")
                fullPath = os.path.join(self.currentPath, info)
                self.sendData(fullPath)
            elif request == "delete":
                info = self.self.__client.recv(1024).decode("utf-8")
                fullPath = os.path.join(self.currentPath, info)
                self.deleteData(fullPath)
            else: #Quit
                return


    def getDrive(self):
        drps = psutil.disk_partitions()
        self.drives = [dp.device for dp in drps if dp.fstype == 'NTFS']
        dataToSend = json.dumps(self.drives).encode('utf-8') 
        size = len(dataToSend)
        self.__client.send(str(size).encode('utf-8'))
        check = self.__client.recv(10)
        self.__client.send(dataToSend)


    def getFolderInfo(self, path):
        for root, subfolder, files in os.walk(path):
            self.fileList = files
            self.folderList = subfolder         
            break

    def sendFolderInfo(self):
        dataToSend = json.dumps(self.fileList).encode('utf-8') 
        size = len(dataToSend)
        self.__client.send(str(size).encode('utf-8'))
        check = self.__client.recv(10)
        self.__client.send(dataToSend)

        dataToSend = json.dumps(self.folderList).encode('utf-8') 
        size = len(dataToSend)
        self.__client.send(str(size).encode('utf-8'))
        check = self.__client.recv(10)
        self.__client.send(dataToSend)
        
        
        
    def delete(self,path, flag):
        if(flag==0): #file
            os.remove(path)
        elif(flag==1): #folder
            shutil.rmtree(path)
        else:
            return
    
    def sendData(self, srcPath, flag):
        if(flag==0):
            self.sendFile(self, srcPath)
        elif(flag==1):
            self.sendFolder(self, srcPath)

    def recvData(self, desPath, flag):
        if(flag==0):
            self.recvFile(self, desPath)
        elif(flag==1):
            self.recvFolder(self, desPath)

    def sendFile(self, relpath, filesize, srcPath):
        self.__client.sendall(relpath.encode() + b'\n')
        self.__client.sendall(str(filesize).encode() + b'\n')
        return None

    def sendFolder(self, srcPath):
        # Name of folder
        head, tail = os.path.split(srcPath)
        self.__client.send(tail.encode())
        check = self.__client.recv(10)

        for path,subfolder,files in os.walk(srcPath):
            for file in files:
                filename = os.path.join(path,file)
                relpath = os.path.relpath(filename,srcPath)
                filesize = os.path.getsize(filename)

                print(f'Sending {relpath}')

                with open(filename,'rb') as f:



                    # Send the file in chunks so large files can be handled.
                    while True:
                        data = f.read(CHUNKSIZE)
                        if not data: break
                        self.__client.sendall(data)

    def recvFile(self,desPath):
        f = open(desPath, 'w')
        buffer = self.__client.recv(1024)
        while(buffer):
            data = self.__client.recv(1024)
            buffer+=data
        self.content = buffer





