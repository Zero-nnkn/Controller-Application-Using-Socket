import os
from posixpath import relpath
import psutil
import shutil
import json

CHUNKSIZE = 1_000_000
import win32com.client 
def getFileMetadata(fullPath, metadata):
    path, filename = os.path.split(fullPath)
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path)
    file_metadata = dict()
    item = ns.ParseName(str(filename))
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value
    print(file_metadata)
    return file_metadata

METADATA = ['Name', 'Size', 'Item type', 'Date modified', 'Date created']
'''
path = "C:\\SQL2019"
def a(path):
    l = []
    for root, subfolder, files in os.walk(path):
        for i in files:
            dict = getFileMetadata(os.path.join(path,i),METADATA)
            l.append([dict['Name'], dict['Size'], dict['Item type']])
        for i in subfolder:
            l.append([i, '', 'File folder'])
        break
    for i in l:
        print(i)
a(path)
'''

class FtpController():
    def __init__(self, clientSocket):
        self.__client = clientSocket
        self.currentPath = "\\"
        self.info = []

    def startListening(self):
        self.senDrive()
        request = ""
        while True:
            request = self.__client.recv(1024).decode("utf-8")
            if not request:
                break
            if request=="view":
                info = self.__client.recv(1024).decode("utf-8")
                if(os.path.exists(os.path.join(self.currentPath, info))):
                    self.currentPath = os.path.join(self.currentPath, info)
                    self.sendFolderInfo(self.currentPath)
            elif request == "back":
                if self.currentPath[-2] == ":":
                    self.senDrive()
                    self.currentPath == "\\"
                else:
                    self.currentPath, tail = os.path.split(self.currentPath)
                    self.sendFolderInfo(self.currentPath)
            elif request == "copy2server":
                info = self.__client.recv(1024).decode("utf-8")
                fullPath = os.path.join(self.currentPath, info)
                self.recvData(fullPath)
            elif request == "copy2client":
                info = self.__client.recv(1024).decode("utf-8")
                fullPath = os.path.join(self.currentPath, info)
                self.sendData(fullPath)
            elif request == "delete":
                info = self.__client.recv(1024).decode("utf-8")
                fullPath = os.path.join(self.currentPath, info)
                self.deleteData(fullPath)
            else: #Quit
                return

    def getFileMetadata(self, fullPath, metadata):
        path, filename = os.path.split(fullPath)
        sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
        ns = sh.NameSpace(path)
        file_metadata = dict()
        item = ns.ParseName(str(filename))
        for ind, attribute in enumerate(metadata):
            attr_value = ns.GetDetailsOf(item, ind)
            if attr_value:
                file_metadata[attribute] = attr_value
        return file_metadata

    def getDrive(self):
        drps = psutil.disk_partitions()
        self.drives = [[dp.device, '', 'File folder'] for dp in drps if dp.fstype == 'NTFS']

    def senDrive(self):
        self.getDrive()

        dataToSend = json.dumps(self.drives).encode('utf-8') 
        size = len(dataToSend)
        self.__client.send(str(size).encode('utf-8'))
        check = self.__client.recv(10)
        self.__client.send(dataToSend)

    def getFolderInfo(self, path):
        self.info = []
        for root, subfolder, files in os.walk(path):
            for i in files:
                dict = self.getFileMetadata(os.path.join(path,i),METADATA)
                self.info.append([dict['Name'], dict['Size'], dict['Item type']])
            for i in subfolder:
                self.info.append([i, '', 'File folder'])
            break


    def sendFolderInfo(self,path):
        self.getFolderInfo(path)

        dataToSend = json.dumps(self.info).encode('utf-8') 
        size = len(dataToSend)
        self.__client.send(str(size).encode('utf-8'))
        check = self.__client.recv(10)
        self.__client.send(dataToSend)
        
        
    def deleteData(self,path):
        if(os.path.isfile(path)):
            os.remove(path)
        elif(os.path.isdir(path)):
            try:
                shutil.rmtree(path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        else:
            return

    def sendData(self, path):
        if(os.path.isfile(path)):
            head, relpath = os.path.split(path)
            self.sendFile(path, relpath)
        elif(os.path.isdir(path)):
            self.sendFolder(path)
        else:
            return

    def recvData(self, path):
        self.recvFolder(path)
        '''
        if(os.path.isfile(path)):
            self.recvFile(path)
        elif(os.path.isdir(path)):
            self.recvFolder(path)
        else:
            return
        '''


    def sendFile(self, fullPath, relpath):
        filesize = os.path.getsize(fullPath)
        self.__client.sendall(relpath.encode() + b'\n')
        self.__client.sendall(str(filesize).encode() + b'\n')

        # Message when need overwrite, rename or not
        check = self.__client.recv(10)
        if check == "continue":
            with open(fullPath,'rb') as f:
            # Send the file in chunks so large files can be handled.
                while True:
                    data = f.read(CHUNKSIZE)
                    if not data: break
                    self.__client.sendall(data)
        # When duplicate and pause copy
        else: 
            return

    def sendFolder(self, srcPath):
        for path,subfolder,files in os.walk(srcPath):
            for file in files:
                fullPath = os.path.join(path,file)
                relpath = os.path.relpath(fullPath,srcPath)
                

                print(f'Sending {relpath}')
                self.sendFile(fullPath, relpath)

    def recvFolder(self, desPath):
        with self.__client, self.__client.makefile('rb') as clientfile:
            while True:
                raw = clientfile.readline()
                if not raw: break # no more files, server closed connection.

                filename = raw.strip().decode()
                length = int(clientfile.readline())
                print(f'Downloading {filename}...\n  Expecting {length:,} bytes...',end='',flush=True)

                path = os.path.join(desPath,filename)
                os.makedirs(os.path.dirname(path),exist_ok=True)

                # Check if exists
                if os.path.exists(path):
                    self.__client.sendall("exists".encode())
                    request = self.recv(20).decode()
                    if request == "pause":
                        continue
                    elif request == "rename":
                        i = 1
                        while os.path.exists(path) == True:
                            dir, fileName = os.path.split(path)
                            fileName = "Copy {i} of " + fileName 
                            path = os.path.join(dir, fileName)
                            i += 1
                    else:
                        pass
                else:
                    self.__client.sendall("not exists".encode())   

                # Read the data in chunks so it can handle large files.
                with open(path,'wb') as f:
                    while length:
                        chunk = min(length,CHUNKSIZE)
                        data = clientfile.read(chunk)
                        if not data: break
                        f.write(data)
                        length -= len(data)
                    else: # only runs if while doesn't break and length==0
                        print('Complete')
                        continue

                # socket was closed early.
                print('Incomplete')
                break 



