import socket
import tkinter as tk

from tkinter import Label, ttk
from tkinter import Image, messagebox
from tkinter import END,INSERT
from tkinter.constants import ANCHOR, CENTER, VERTICAL
from tkinter.font import BOLD

from PIL import Image
from PIL import ImageTk

import cv2

import pickle
import struct
import threading
import json

import os
from posixpath import relpath
import psutil
import shutil
import win32com.client

PORT = 5000
PORT_STREAM = 5500

clientSocket = None
streamSocket = None

CHUNKSIZE = 1_000_000
METADATA = ['Name', 'Size', 'Item type', 'Date modified', 'Date created']



def CloseButton(root):
    s = "Quit"
    clientSocket.send(s.encode("utf-8"))
    root.destroy()



class StreamingServer:
    """
    Class for the streaming server.
    Attributes
    ----------
    Private:
        __host : str
            host address of the listening server
        __port : int
            port on which the server is listening
        __slots : int
            amount of maximum avaialable slots (not ready yet)
        __used_slots : int
            amount of used slots (not ready yet)
        __quit_key : chr
            key that has to be pressed to close connection
        __running : bool
            inicates if the server is already running or not
        __block : Lock
            a basic lock used for the synchronization of threads
        __server_socket : socket
            the main server socket
    Methods
    -------
    Private:
        __init_socket : method that binds the server socket to the host and port
        __server_listening: method that listens for new connections
        __client_connection : main method for processing the client streams
    Public:
        start_server : starts the server in a new thread    
        stop_server : stops the server and closes all connections
    """

    # TODO: Implement slots functionality
    def __init__(self, host, port, quit_key='q'):
        """
        Creates a new instance of StreamingServer
        Parameters
        ----------
        host : str
            host address of the listening server
        port : int
            port on which the server is listening
        slots : int
            amount of avaialable slots (not ready yet) (default = 8)
        quit_key : chr
            key that has to be pressed to close connection (default = 'q')  
        """
        self.__host = host
        self.__port = port
        self.__running = False
        self.__quit_key = quit_key
        self.__block = threading.Lock()
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__init_socket()

    def __init_socket(self):
        """
        Binds the server socket to the given host and port
        """
        self.__server_socket.bind((self.__host, self.__port))

    def start_server(self):
        """
        Starts the server if it is not running already.
        """
        if self.__running:
            print("Server is already running")
        else:
            self.__running = True
            server_thread = threading.Thread(target=self.__server_listening)
            server_thread.start()

    def __server_listening(self):
        """
        Listens for new connections.
        """
        self.__server_socket.listen()
        while self.__running:
            self.__block.acquire()
            connection, address = self.__server_socket.accept()

            self.__block.release()
            thread = threading.Thread(target=self.__client_connection, args=(connection, address,))
            thread.start()

    def stop_server(self):
        """
        Stops the server and closes all connections
        """
        if self.__running:
            self.__running = False
            closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_connection.connect((self.__host, self.__port))
            closing_connection.close()
            self.__block.acquire()
            self.__server_socket.close()
            self.__block.release()
        else:
            print("Server not running!")

    def __client_connection(self, connection, address):
        """
        Handles the individual client connections and processes their stream data.
        """
        payload_size = struct.calcsize('>L')
        data = b""

        while self.__running:

            break_loop = False

            while len(data) < payload_size:
                received = connection.recv(4096)
                if received == b'':
                    connection.close()
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += connection.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            #----------TO DO----------
            # Thay vì show lên cv2 thì show lên tkinter
            # Tạo 1 cửa sổ mới như lúc call mess
            # Tắt cửa sổ thì gọi hàm stop_server và gửi "quit"
            '''
            cv2.imshow(str(address), frame)
            if cv2.waitKey(1) == ord(self.__quit_key):
                connection.close()
                break

            '''
            global canvas
            img = ImageTk.PhotoImage(Image.fromarray(frame))  
            self.tab7.main_label.configure(image=img) 
            self.tab7.main_label.image = img

            #----------TO DO----------





class Client(tk.Frame):





    #--------------------GENERAL----------------------------------------
    def __init__(self, root):
            self.root=root
            self.root.title("SUPER CONTROLER")
            self.root.geometry("700x500")
            self.root.resizable(False,False)
            self.root.grab_set()
            self.createWidgets()
            self.firstChanged = True

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Connection lost")
            return False
        else: return True

    def butConnectClick(self, event = None):
        test = True
        global clientSocket
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = self.ipConnect.get().strip()
            clientSocket.connect((self.host,PORT))
        except:
            print ("Fail to connect with the socket-server")
            clientSocket= None
            test = False
        if test:
            messagebox.showinfo("", "Success")
            for i in range(0,7):
                self.tabControl.tab(i,state="normal")
            self.tabControl.select(0)
            self.tabControl.bind('<<NotebookTabChanged>>', self.on_tab_change)
        else:
            messagebox.showinfo("Error", "Not connected to the server")
        a=None

    def butDisconnectClick(self, event = None):
        s = "EXIT"
        clientSocket.send(s.encode('utf-8'))
        for i in range(0,7):
                self.tabControl.tab(i,state="disabled")

    def on_tab_change(self,event=None):
        if self.firstChanged == False:
            clientSocket.send("quit".encode('utf-8'))
        else: self.firstChanged = False
        tabName = self.tabControl.tab(self.tabControl.select(),"text")
        if tabName == "APPS\nCONTROLER":
            s = "APP"
        elif tabName == "PROCESSES\nCONTROLER":
            s = "PROCESS"
        elif tabName == "FTP\nCONTROLER":
            s = "FTP"
        elif tabName == "KEYBOARD\nCONTROLER":
            s = "KEYBOARD"
        elif tabName == "MAC\n   ADDRESS  ":
            s = "MACADDRESS"
        elif tabName == "POWER\nCONTROLER":
            s = "POWER"
        elif tabName == "STREAMING\nCONTROLER":
            s = "STREAMING"
        clientSocket.send(s.encode('utf-8'))
        print(s)
        if s == "FTP":
            self.gettingStarted()





    #--------------------TAB1 2 APP PROCESS----------------------------------------
    def clearTreeView(self, tree):
        rows = tree.get_children()
        if rows != '()':
            for row in rows:
                tree.delete(row)
    
    def butRefreshClick(self):
        if not self.checkConnected():
           return
        s = "view"
        clientSocket.send(s.encode('utf-8'))
        size = int(clientSocket.recv(10).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        tabName = self.tabControl.tab(self.tabControl.select(),"text")
        if tabName == "APPS\nCONTROLER":
            tab = self.tab1
        elif tabName == "PROCESSES\nCONTROLER":
            tab = self.tab2
        tab.data = []
        buffer = "".encode("utf-8")
        while size > 0:
               data = clientSocket.recv(4096)
               size -= len(data)
               buffer += data
        tab.data = json.loads(buffer.decode("utf-8"))
        self.clearTreeView(tab.tv1)
        rows = tab.data
        for row in rows:
            tab.tv1.insert("", "end", values=row)

    def butKillClick(self, event = None):
        if not self.checkConnected():
            return
        s = "KillID"
        clientSocket.send(s.encode('utf-8'))
        tabName = self.tabControl.tab(self.tabControl.select(),"text")
        if tabName == "APPS\nCONTROLER":
            tab = self.tab1
        elif tabName == "PROCESSES\nCONTROLER":
            tab = self.tab2
        s = tab.killID.get().strip()
        clientSocket.send(s.encode('utf-8'))
        buffer = clientSocket.recv(4096)
        if not buffer:
            return
        message = buffer.decode('utf-8')
        messagebox.showinfo("", message,parent = self)

    def butStartClick(self, event = None):
        if not self.checkConnected():
            return
        s = "StartID"
        clientSocket.send(s.encode('utf-8'))
        tabName = self.tabControl.tab(self.tabControl.select(),"text")
        if tabName == "APPS\nCONTROLER":
            tab = self.tab1
        elif tabName == "PROCESSES\nCONTROLER":
            tab = self.tab2
        s = tab.startID.get().strip()
        clientSocket.send(s.encode('utf-8'))
        buffer = clientSocket.recv(4096)
        if not buffer:
            return
        message = buffer.decode('utf-8')
        messagebox.showinfo("", message, parent = self)





    #--------------------TAB3 FTP----------------------------------------
    def do_popup1(self,event):
        try:
            self.tab3.popup1.selection = self.tab3.tv1.set(self.tab3.tv1.identify_row(event.y))
            self.tab3.popup1.post(event.x_root, event.y_root)
        finally:
            self.tab3.popup1.grab_release()

    def do_popup2(self,event):
        try:
            self.tab3.popup2.selection = self.tab3.tv2.set(self.tab3.tv2.identify_row(event.y))
            self.tab3.popup2.post(event.x_root, event.y_root)
        finally:
            self.tab3.popup2.grab_release()

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

    def getFolderInfo(self, path):
        self.info = []
        for root, subfolder, files in os.walk(path):
            for i in files:
                dict = self.getFileMetadata(os.path.join(path,i),METADATA)
                self.info.append([dict['Name'], dict['Size'], dict['Item type']])
            for i in subfolder:
                self.info.append([i, '', 'File folder'])
            break
        return self.info

    def displayInfo(self, tree, infos):
        self.clearTreeView(tree)
        for info in infos:
            tree.insert("", "end", values=info)

    def displayDrive(self):
        drps = psutil.disk_partitions()
        self.tab3.clientPath = ""
        self.tab3.clientInfos = [[dp.device, '', 'File folder'] for dp in drps if dp.fstype == 'NTFS']
        self.displayInfo(self.tab3.tv1,self.tab3.clientInfos)
        self.tab3.clientPathtxt.configure(state="normal")
        self.tab3.clientPathtxt.delete('1.0', END)
        self.tab3.clientPathtxt.insert(END,self.tab3.clientPath)

    def gettingStarted(self):
        self.displayDrive()
        size = int(clientSocket.recv(10).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        buffer = "".encode("utf-8")
        while size > 0:
               data = clientSocket.recv(4096)
               size -= len(data)
               buffer += data
        self.tab3.serverPath = ""
        self.tab3.serverInfos = json.loads(buffer.decode("utf-8"))
        self.displayInfo(self.tab3.tv2,self.tab3.serverInfos)
        self.tab3.serverPathtxt.configure(state="normal")
        self.tab3.serverPathtxt.delete('1.0', END)
        self.tab3.serverPathtxt.insert(END,self.tab3.serverPath)

    def butClientPreviousPathClick(self, event = None):
        l = len(self.tab3.clientPath)
        if self.tab3.clientPath[l-2:-1] == ":":
            self.displayDrive()
            return
        elif self.tab3.clientPath =="": return
        self.tab3.clientPath, tail = os.path.split(self.tab3.clientPath)
        self.tab3.clientInfos = self.getFolderInfo(self.tab3.clientPath)
        self.displayInfo(self.tab3.tv1,self.tab3.clientInfos)
        self.tab3.clientPathtxt.configure(state="normal")
        self.tab3.clientPathtxt.delete('1.0', END)
        self.tab3.clientPathtxt.insert(END,self.tab3.clientPath)
        self.tab3.clientPathtxt.configure(state="disabled")

    def butServerPreviousPathClick(self, event = None):
        if not self.checkConnected():
            return
        s = "back"
        clientSocket.send(s.encode('utf-8'))
        size = int(clientSocket.recv(10).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        buffer = "".encode("utf-8")
        while size > 0:
               data = clientSocket.recv(4096)
               size -= len(data)
               buffer += data
        l = len(self.tab3.serverPath)
        if self.tab3.serverPath[l-2:-1] == ":":
            self.tab3.serverPath = ""
        else:
            self.tab3.serverPath, tail = os.path.split(self.tab3.serverPath)
        self.tab3.serverInfos = json.loads(buffer.decode("utf-8"))
        self.displayInfo(self.tab3.tv2,self.tab3.serverInfos)
        self.tab3.serverPathtxt.configure(state="normal")
        self.tab3.serverPathtxt.delete('1.0', END)
        self.tab3.serverPathtxt.insert(END,self.tab3.serverPath)
        self.tab3.serverPathtxt.configure(state="disabled")

    def clientOnDoubleClick(self, event = None):
        item = self.tab3.tv1.selection()[0]
        folderName = self.tab3.tv1.item(item,"value")[0]
        self.tab3.clientPath = os.path.join(self.tab3.clientPath,folderName)
        self.tab3.clientInfos = self.getFolderInfo(self.tab3.clientPath)
        self.displayInfo(self.tab3.tv1,self.tab3.clientInfos)
        self.tab3.clientPathtxt.configure(state="normal")
        self.tab3.clientPathtxt.delete('1.0', END)
        self.tab3.clientPathtxt.insert(END,self.tab3.clientPath)
        self.tab3.clientPathtxt.configure(state="disabled")

    def serverOnDoubleClick(self, event = None):
        if not self.checkConnected():
            return
        s = "view"
        clientSocket.send(s.encode('utf-8'))
        item = self.tab3.tv2.selection()[0]
        folderName = self.tab3.tv2.item(item,"value")[0]
        clientSocket.send(folderName.encode('utf-8'))
        self.tab3.serverPath = os.path.join(self.tab3.serverPath,folderName)
        size = int(clientSocket.recv(10).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        buffer = "".encode("utf-8")
        while size > 0:
               data = clientSocket.recv(4096)
               size -= len(data)
               buffer += data
        self.tab3.serverInfos = json.loads(buffer.decode("utf-8"))
        self.displayInfo(self.tab3.tv2,self.tab3.serverInfos)
        self.tab3.serverPathtxt.configure(state="normal")
        self.tab3.serverPathtxt.delete('1.0', END)
        self.tab3.serverPathtxt.insert(END,self.tab3.serverPath)
        self.tab3.serverPathtxt.configure(state="disabled")

    def copyToServer(self):
        if not self.checkConnected():
            return
        s = "copy2server"
        clientSocket.send(s.encode('utf-8'))
        info = self.tab3.popup1.selection["1"]
        clientSocket.send(info.encode('utf-8'))
        pathSend = os.path.join(self.tab3.clientPath,info)
        self.sendData(pathSend)

    def deleteFile(self):
        if not self.checkConnected():
            return
        s = "delete"
        clientSocket.send(s.encode('utf-8'))
        info = self.tab3.popup1.selection["1"]
        clientSocket.send(info.encode('utf-8'))

    def sendData(self, path):
        if(os.path.isfile(path)):
            head, relpath = os.path.split(path)
            self.sendFile(path, relpath)
        elif(os.path.isdir(path)):
            self.sendFolder(path)
        else:
            return

    def sendFile(self, fullPath, relpath):
        filesize = os.path.getsize(fullPath)
        self.__clientSocket.sendall(relpath.encode() + b'\n')
        self.__clientSocket.sendall(str(filesize).encode() + b'\n')

        # Message when need overwrite, rename or not
        check = self.__clientSocket.recv(10)

        if check == "exists":
            request = None
            #----------TO DO----------
            # hiện bảng lựa chọ người dùng muốn overwrite, rename hay hủy copy
            # trả về giá trị request = overwrite/rename/pause
            #----------TO DO----------

            self.__clientSocket.sendall(request.encode())
        else: 
            pass

        if request != "pause":
            with open(fullPath,'rb') as f:
                while True:
                    data = f.read(CHUNKSIZE)
                    if not data: break
                    self.__clientSocket.sendall(data)

    def sendFolder(self, srcPath):
        for path,subfolder,files in os.walk(srcPath):
            for file in files:
                fullPath = os.path.join(path,file)
                relpath = os.path.relpath(fullPath,srcPath)
                

                print(f'Sending {relpath}')
                self.sendFile(fullPath, relpath)





    #--------------------TAB4 KEY----------------------------------------
    def butLockClick(self):
        if not self.checkConnected():
           return
        s = "lock"
        clientSocket.send(s.encode('utf-8'))

    def butHookClick(self):
        if not self.checkConnected():
           return
        s = "hook"
        clientSocket.send(s.encode('utf-8'))
        
    def butUnhookClick(self):
        if not self.checkConnected():
           return
        s = "unhook"
        clientSocket.send(s.encode('utf-8'))
    
    def butPrintClick(self):
        if not self.checkConnected():
           return
        s = "print"
        clientSocket.send(s.encode('utf-8'))
        buffer = clientSocket.recv(4096).decode('utf-8')
        if not buffer or buffer=="No":
            return
        clientSocket.send("Ok".encode("utf-8"))
        self.tab4.KeyLog = clientSocket.recv(4096).decode("utf-8")

        self.tab4.KeyView.config(state="normal")
        self.tab4.KeyView.insert('end', self.tab4.KeyLog)
        self.tab4.KeyView.pack()
        self.tab4.KeyView.config(state="disabled")
        self.tab4.KeyLog = "" 

    def butDelClick(self):
        self.tab4.keyLog = ""
        self.tab4.KeyView.config(state="normal")
        self.tab4.KeyView.delete('1.0','end')
        self.tab4.KeyView.pack()
        self.tab4.KeyView.config(state="disabled")





    #--------------------TAB5 MAC----------------------------------------
    def butGetMACClick(self):
        if not self.checkConnected():
           return
        s = "macaddress"
        clientSocket.send(s.encode('utf-8'))
        size = int(clientSocket.recv(10).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        self.tab5.MACs = []
        buffer = "".encode("utf-8")
        while size > 0:
               data = clientSocket.recv(4096)
               size -= len(data)
               buffer += data
        self.tab5.MACs = json.loads(buffer.decode("utf-8"))
        self.tab5.MACView.delete('1.0', END)
        for MAC in self.tab5.MACs:
            for item in MAC:
                self.tab5.MACView.insert(INSERT, item)
                self.tab5.MACView.insert(INSERT, "\t")
            self.tab5.MACView.insert(INSERT, "\n\n")





    #--------------------TAB6 POWER----------------------------------------
    def butLogOutClick(self,event=None):
        if not self.checkConnected():
           return
        s = "logout"
        clientSocket.send(s.encode('utf-8'))
        messagebox.showinfo("", "The server logged out successfully.")

    def butShutDownClick(self,event=None):
        if not self.checkConnected():
           return
        s = "shutdown"
        clientSocket.send(s.encode('utf-8'))
        messagebox.showinfo("", "Server shut down after 60s.")





    #--------------------TAB7 STREAM----------------------------------------
    def butStartRecording(self):
        if not self.checkConnected():
           return
        streamSocket = StreamingServer("localhost", PORT_STREAM)
        streamSocket.start_server()        





    def createWidgets(self):
        




    #--------------------GENERAL----------------------------------------
        self.frame0 = tk.LabelFrame(self.root,bd=1,background="black")
        self.frame0.place(x=0, y=0, height=500, width=120)

        self.frame1 = tk.LabelFrame(self.root,bd=1,background="black")
        self.frame1.place(x=120, y=0, height=503, width=883)

        img = Image.open("F:\HCMUS-Năm 2\Học kì 2\Mạng máy tính\Controller-Application-Using-Socket\Client\logo.png")
        self.img=ImageTk.PhotoImage(img)
        self.theme=tk.Label(self.frame0,image=self.img,background="black")
        self.theme.place(x=25, y=45)
        img.close()

        self.ipConnect = tk.StringVar()
        self.ipConnect.set("Enter IP address")
        self.txtIP = tk.Entry(self.frame0, textvariable = self.ipConnect)
        self.txtIP.place(x=10, y=170, height=30, width=100)
        self.txtIP.configure(bg="black",fg="white",insertbackground="white",bd=3,font=("Lato",8))
        self.txtIP.bind("<Key-Return>", self.butConnectClick)
        
        #flat, groove, raised, ridge, solid, or sunken
        self.butConnect = tk.Button(self.frame0,text = "Connect",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.butConnect["command"] = self.butConnectClick
        self.butConnect.place(x=10, y=250, height=30, width=100)

        self.butDisconnect = tk.Button(self.frame0,text = "Disconnect",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.butDisconnect["command"] = self.butDisconnectClick
        self.butDisconnect.place(x=10, y=460, height=30, width=100)
        
        noteBookStyle = ttk.Style(self.frame1)
        noteBookStyle.theme_use('default')
        noteBookStyle.configure("TNotebook", background="black", tabposition='wn',cursor="circle")
        noteBookStyle.configure("TNotebook.Tab", font=('Lato', 8, BOLD), justify="center", background="black", foreground="white", ANCHOR="c",cursor="circle")
        noteBookStyle.map("TNotebook.Tab", background= [("selected", "white")],foreground=[("selected", "black")])

        tabFrameStyle = ttk.Style(self.frame1)
        tabFrameStyle.configure("TFrame", background="black")

        treeViewStyle = ttk.Style(self.frame1)
        treeViewStyle.configure("Treeview", background="black", foreground="white", fieldbackground="black")
        treeViewStyle.configure("Treeview.Heading", font=('Lato', 11, BOLD), background="black", foreground='white')
        
        self.tabControl = ttk.Notebook(self.frame1,style="TNotebook")
        self.tabControl.pack(expand=1,fill="both")
        

        


    #--------------------TAB1----------------------------------------APP
        self.tab1 = ttk.Frame(self.tabControl,style="TFrame")
        tab1Img = Image.open("F:\HCMUS-Năm 2\Học kì 2\Mạng máy tính\Controller-Application-Using-Socket\Client\\tab1.png")
        tab1Img = tab1Img.resize((40,40))
        self.tab1.img = ImageTk.PhotoImage(tab1Img)
        self.tabControl.add(self.tab1,text="APPS\nCONTROLER",image=self.tab1.img,compound=tk.TOP)


        self.tab1.frame0 = tk.Frame(self.tab1,background="black")
        self.tab1.frame0.place(x=0, y=0, height=440, width=500)
        self.tab1.tv1 = ttk.Treeview(self.tab1.frame0)
        self.tab1.tv1.place(relheight=1, relwidth=1)
        self.tab1.treescrolly = tk.Scrollbar(self.tab1.frame0, orient="vertical", command=self.tab1.tv1.yview)
        self.tab1.treescrolly.pack(side="right", fill="y")
        self.tab1.tv1["columns"] = ("1", "2", "3")
        self.tab1.tv1["show"] = "headings"
        self.tab1.tv1.heading(1, text = "Application 's Name")
        self.tab1.tv1.heading(2, text = "Application 's ID")
        self.tab1.tv1.heading(3, text = "Thread")
        self.tab1.tv1.column(1, width = 100)
        self.tab1.tv1.column(2, width = 75)
        self.tab1.tv1.column(3, width = 75)
        self.tab1.data = []
        
        self.tab1.butRefresh = tk.Button(self.tab1,text = "Refresh",font=("Lato",15),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab1.butRefresh["command"] = self.butRefreshClick
        self.tab1.butRefresh.place(x=0, y=440, height=60, width=150)

        self.tab1.killID = tk.StringVar()
        self.tab1.killID.set("Enter ID")
        self.tab1.KillIDEntry = tk.Entry(self.tab1, textvariable = self.tab1.killID)
        self.tab1.KillIDEntry.place(x=150, y=440, height=30, width=250)
        self.tab1.KillIDEntry.configure(font=("Lato",10),relief="groove",bg="black",fg="white",insertbackground="white")
        self.tab1.KillIDEntry.bind("<Key-Return>", self.butKillClick)

        self.tab1.butKill = tk.Button(self.tab1,text = "Kill",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab1.butKill["command"] = self.butKillClick
        self.tab1.butKill.place(x=400, y=440, height=30, width=100)

        self.tab1.startID = tk.StringVar()
        self.tab1.startID.set("Enter Name")
        self.tab1.StartIDEntry = tk.Entry(self.tab1, textvariable = self.tab1.startID)
        self.tab1.StartIDEntry.place(x=150, y=470, height=30, width=250)
        self.tab1.StartIDEntry.configure(font=("Lato",10),relief="groove",bg="black",fg="white",insertbackground="white")
        self.tab1.StartIDEntry.bind("<Key-Return>", self.butStartClick)

        self.tab1.butStart = tk.Button(self.tab1,text = "Start",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab1.butStart["command"] = self.butStartClick
        self.tab1.butStart.place(x=400, y=470, height=30, width=100)





    #--------------------TAB2----------------------------------------PROCESS
        self.tab2 = ttk.Frame(self.tabControl)
        tab2Img = Image.open("F:\HCMUS-Năm 2\Học kì 2\Mạng máy tính\Controller-Application-Using-Socket\Client\\tab2.png")
        tab2Img = tab2Img.resize((40,40))
        self.tab2.img = ImageTk.PhotoImage(tab2Img)
        self.tabControl.add(self.tab2,text="PROCESSES\nCONTROLER",image=self.tab2.img,compound=tk.TOP) 

        self.tab2.frame0 = tk.Frame(self.tab2,background="black")
        self.tab2.frame0.place(x=0, y=0, height=440, width=500)
        self.tab2.tv1 = ttk.Treeview(self.tab2.frame0)
        self.tab2.tv1.place(relheight=1, relwidth=1)
        self.tab2.treescrolly = tk.Scrollbar(self.tab2.frame0, orient="vertical", command=self.tab2.tv1.yview)
        self.tab2.treescrolly.pack(side="right", fill="y")
        self.tab2.tv1["columns"] = ("1", "2", "3")
        self.tab2.tv1["show"] = "headings"
        self.tab2.tv1.heading(1, text = "Process 's Name")
        self.tab2.tv1.heading(2, text = "Process 's ID")
        self.tab2.tv1.heading(3, text = "Thread")
        self.tab2.tv1.column(1, width = 100)
        self.tab2.tv1.column(2, width = 75)
        self.tab2.tv1.column(3, width = 75)
        self.tab2.data = []
        
        self.tab2.butRefresh = tk.Button(self.tab2,text = "Refresh",font=("Lato",15),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab2.butRefresh["command"] = self.butRefreshClick
        self.tab2.butRefresh.place(x=0, y=440, height=60, width=150)

        self.tab2.killID = tk.StringVar()
        self.tab2.killID.set("Enter ID")
        self.tab2.KillIDEntry = tk.Entry(self.tab2, textvariable = self.tab2.killID)
        self.tab2.KillIDEntry.place(x=150, y=440, height=30, width=250)
        self.tab2.KillIDEntry.configure(font=("Lato",10),relief="groove",bg="black",fg="white",insertbackground="white")
        self.tab2.KillIDEntry.bind("<Key-Return>", self.butKillClick)

        self.tab2.butKill = tk.Button(self.tab2,text = "Kill",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab2.butKill["command"] = self.butKillClick
        self.tab2.butKill.place(x=400, y=440, height=30, width=100)

        self.tab2.startID = tk.StringVar()
        self.tab2.startID.set("Enter Name")
        self.tab2.StartIDEntry = tk.Entry(self.tab2, textvariable = self.tab2.startID)
        self.tab2.StartIDEntry.place(x=150, y=470, height=30, width=250)
        self.tab2.StartIDEntry.configure(font=("Lato",10),relief="groove",bg="black",fg="white",insertbackground="white")
        self.tab2.StartIDEntry.bind("<Key-Return>", self.butStartClick)

        self.tab2.butStart = tk.Button(self.tab2,text = "Start",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab2.butStart["command"] = self.butStartClick
        self.tab2.butStart.place(x=400, y=470, height=30, width=100)





    #--------------------TAB3----------------------------------------FTP
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3,text="FTP\nCONTROLER")

        self.tab3.clientPath = "\\"
        self.tab3.clientPathtxt = tk.Text(self.tab3)
        self.tab3.clientPathtxt.insert(INSERT,self.tab3.clientPath)
        self.tab3.clientPathtxt.configure(font=("Lato",10),relief="groove",bg="black",fg="white",cursor="circle",state="disabled")
        self.tab3.clientPathtxt.place(x=0,y=0,height=30,width=250)

        self.tab3.serverPath = "\\"
        self.tab3.serverPathtxt = tk.Text(self.tab3)
        self.tab3.serverPathtxt.insert(INSERT,self.tab3.serverPath)
        self.tab3.serverPathtxt.configure(font=("Lato",10),relief="groove",bg="black",fg="white",cursor="circle",state="disabled")
        self.tab3.serverPathtxt.place(x=250,y=0,height=30,width=250)

        self.tab3.butClientPreviousPath=tk.Button(self.tab3,text = "Previous",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")        
        self.tab3.butClientPreviousPath["command"] = self.butClientPreviousPathClick
        self.tab3.butClientPreviousPath.place(x=0, y=30, height=30, width=100)

        self.tab3.butServerPreviousPath=tk.Button(self.tab3,text = "Previous",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")        
        self.tab3.butServerPreviousPath["command"] = self.butServerPreviousPathClick
        self.tab3.butServerPreviousPath.place(x=250, y=30, height=30, width=100)

        self.tab3.frame0 = tk.Frame(self.tab3,background="black")
        self.tab3.frame0.place(x=0, y=60, height=440, width=250)
        self.tab3.tv1 = ttk.Treeview(self.tab3.frame0)
        self.tab3.tv1.place(relheight=1, relwidth=1)
        self.tab3.treescrolly = tk.Scrollbar(self.tab3.frame0, orient="vertical", command=self.tab3.tv1.yview)
        self.tab3.treescrolly.pack(side="right", fill="y")
        self.tab3.tv1["columns"] = ("1", "2", "3")
        self.tab3.tv1["show"] = "headings"
        self.tab3.tv1.heading(1, text = "Filename")
        self.tab3.tv1.heading(2, text = "Filesize")
        self.tab3.tv1.heading(3, text = "Filetype")
        self.tab3.tv1.column(1, width = 70)
        self.tab3.tv1.column(2, width = 40)
        self.tab3.tv1.column(3, width = 40)
        self.tab3.clientInfos = []
        self.tab3.tv1.bind("<Double-1>", self.clientOnDoubleClick)
        # row=["Google Chorme","0000001","1234567"]
        # for i in range(10):
        #     self.tab3.tv1.insert("", "end", values=row, tags="a")
        #     self.tab3.tv1.tag_configure("a", background="black", foreground="white")

        self.tab3.popup1 = tk.Menu(self.tab3, tearoff=0)
        self.tab3.popup1.add_command(label="Copy", command=self.copyToServer)
        self.tab3.popup1.add_separator()
        self.tab3.tv1.bind("<Button-3>", self.do_popup1)

        self.tab3.frame1 = tk.Frame(self.tab3,background="black")
        self.tab3.frame1.place(x=250, y=60, height=440, width=250)
        self.tab3.tv2 = ttk.Treeview(self.tab3.frame1)
        self.tab3.tv2.place(relheight=1, relwidth=1)
        self.tab3.treescrolly = tk.Scrollbar(self.tab3.frame1, orient="vertical", command=self.tab3.tv2.yview)
        self.tab3.treescrolly.pack(side="right", fill="y")
        self.tab3.tv2["columns"] = ("1", "2", "3")
        self.tab3.tv2["show"] = "headings"
        self.tab3.tv2.heading(1, text = "Name")
        self.tab3.tv2.heading(2, text = "Size")
        self.tab3.tv2.heading(3, text = "Item type")
        self.tab3.tv2.column(1, width = 70)
        self.tab3.tv2.column(2, width = 40)
        self.tab3.tv2.column(3, width = 40)
        self.tab3.serverInfos = []
        self.tab3.tv2.bind("<Double-1>", self.serverOnDoubleClick)
        row=["Coc Coc","0000001","1234567"]
        for i in range(10):
            self.tab3.tv2.insert("", "end", values=row, tags="a")
            self.tab3.tv2.tag_configure("a", background="black", foreground="white")

        self.tab3.popup2 = tk.Menu(self.tab3, tearoff=0)
        self.tab3.popup2.add_command(label="Delete", command=self.deleteFile)
        self.tab3.popup2.add_separator()
        self.tab3.tv2.bind("<Button-3>", self.do_popup2)





    #--------------------TAB4----------------------------------------KEYBOARD
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4,text="KEYBOARD\nCONTROLER")

        self.tab4.butLock = tk.Button(self.tab4, text = "Lock",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butLock["command"] = self.butLockClick
        self.tab4.butLock.place(x=25, y=20, height=50, width=70)

        self.tab4.butHook = tk.Button(self.tab4, text = "Hook",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butHook["command"] = self.butHookClick
        self.tab4.butHook.place(x=120, y=20, height=50, width=70)

        self.tab4.butUnhook = tk.Button(self.tab4, text = "Unhook",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butUnhook["command"] = self.butUnhookClick
        self.tab4.butUnhook.place(x=215, y=20, height=50, width=70)

        self.tab4.butPrint = tk.Button(self.tab4, text = "Print",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butPrint["command"] = self.butPrintClick
        self.tab4.butPrint.place(x=310, y=20, height=50, width=70)
   
        self.tab4.butDel = tk.Button(self.tab4, text = "Delete",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butDel["command"] = self.butDelClick
        self.tab4.butDel.place(x=405, y=20, height=50, width=70)

        self.tab4.frame1 = tk.LabelFrame(self.tab4, text="")
        self.tab4.frame1.place(x=20, y=90, height=390, width=460)
        self.tab4.KeyView = tk.Text(self.tab4.frame1,font=("Lato",10),relief="groove",bg="black",fg="white",cursor="circle")
        self.tab4.KeyLog = ""
        self.tab4.KeyView.insert(INSERT, self.tab4.KeyLog)
        self.tab4.KeyView.config(state="disabled")
        self.tab4.KeyView.pack()





    #--------------------TAB5----------------------------------------MAC
        self.tab5 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab5,text="MAC\n   ADDRESS  ")

        self.tab5.frame1 = tk.LabelFrame(self.tab5, text="MAC Address",font=("Lato",10),relief="groove",bg="black",fg="white",cursor="circle")
        self.tab5.frame1.place(x=20, y=20, height=390, width=460)
        self.tab5.MACView = tk.Text(self.tab5.frame1,font=("Lato",8),relief="groove",bg="black",fg="white",cursor="circle",insertbackground="white")
        self.tab5.MACs = []
        self.tab5.MACView.pack()

        self.tab5.butGetMAC = tk.Button(self.tab5,text="Get MAC Address",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab5.butGetMAC["command"] = self.butGetMACClick
        self.tab5.butGetMAC.place(x=180, y=430, height=50, width=140)





    #--------------------TAB6----------------------------------------POWER
        self.tab6 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab6,text="POWER\nCONTROLER")

        self.tab6.butLogOut = tk.Button(self.tab6,text = "Log out",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab6.butLogOut["command"] = self.butLogOutClick
        self.tab6.butLogOut.place(x=10, y=10, height=30, width=100)

        self.tab6.butShutDown = tk.Button(self.tab6,text = "Shutdown",font=("Lato",10),relief="groove",bg="red",fg="white",justify="center",cursor="circle")
        self.tab6.butShutDown["command"] = self.butShutDownClick
        self.tab6.butShutDown.place(x=10, y=50, height=30, width=100)





    #--------------------TAB7----------------------------------------STREAMING
        self.tab7 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab7,text="STREAMING\nCONTROLER")

        self.tab7.main_label = Label(self.tab7)
        self.tab7.main_label.grid()
        self.tab7.main_label.place(x=0,y=0,height=380,width=500)
        self.tab7.main_label.configure(bg="grey",bd=2)

        self.tab7.butStartRecording = tk.Button(self.tab7,text = "Start Recording",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab7.butStartRecording["command"] = self.butStartRecording
        self.tab7.butStartRecording.place(x=200, y=400, height=50, width=100)




    #------------------------------------------------------------
        # for i in range(0,7):
        #     self.tabControl.tab(i,state="disabled")


root=tk.Tk()
#root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
controler=Client(root)
root.mainloop()