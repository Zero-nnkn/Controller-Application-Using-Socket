import os
import psutil
import shutil

CHUNKSIZE = 1_000_000

class ftpController():
    def __init__(self, clientSocket):
        self.__client = clientSocket
        self.currentPath = "\\"
        self.startPath = "\\"
        self.fileList = []
        self.folderList = []

    def getDrive(self):
        drps = psutil.disk_partitions()
        self.drives = [dp.device for dp in drps if dp.fstype == 'NTFS']

    def list_files(self, startpath):
        for root, subfolder, files in os.walk(startpath):
            self.fileList = files
            self.folderList = subfolder         
            '''
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))
            '''
            break
        
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

    def sendFile(self, srcPath):
        # os.getcwd()
        # os.getcwd()+ '\\' + link
        # Name of file
        head, tail = os.path.split(srcPath)
        self.__client.send(tail.encode())
        check = self.__client.recv(10)

        f = open(srcPath)
        size = os.path.getsize(srcPath)
        self.__client.send(str(size).encode('utf-8'))
        check = self.__client.recv(10)
        while size > 0:
            l = f.read(1024)
            self.__client.send(l)
            size = size - len(l)
        f.close()

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
                    self.__client.sendall(relpath.encode() + b'\n')
                    self.__client.sendall(str(filesize).encode() + b'\n')

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





