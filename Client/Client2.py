from ctypes import alignment
import socket
import tkinter as tk
from tkinter import ttk
from tkinter import Image, messagebox
from tkinter import END,INSERT
from tkinter.constants import ANCHOR, CENTER, VERTICAL
from tkinter.font import BOLD
from typing import Text

from PIL import Image
from PIL import ImageTk

from tab1widget import createTab1Widget

PORT = 106

clientSocket = None

def CloseButton(root):
    s = "Quit"
    clientSocket.send(s.encode("utf-8"))
    root.destroy()

class Client(tk.Frame):

    def __init__(self, root):
            self.root=root
            self.root.title("SUPER CONTROLER")
            self.root.geometry("700x500")
            self.root.resizable(False,False)
            self.root.grab_set()
            self.createWidgets()

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Not connected to the server")
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
        else:
            messagebox.showinfo("Error", "Not connected to the server")

    def butDisconnectClick(self, event = None):
        # test = True
        # global clientSocket
        # try:
        #     clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     self.host = self.ipConnect.get().strip()
        #     clientSocket.connect((self.host,PORT))
        # except:
        #     print ("Fail to connect with the socket-server")
        #     clientSocket= None
        #     test = False
        # if test:
        #     messagebox.showinfo("", "Success")
        # else:
        #     messagebox.showinfo("Error", "Not connected to the server")
        a=None

    def butRefreshClick(self, event = None):

        a=None

    def butKillClick(self, event = None):
            # if not self.checkConnected():
            #    return
            # s = "KillID"
            # self.__client.send(s.encode('utf-8'))
            # s = self.ID.get().strip()
            # self.__client.send(s.encode('utf-8'))
            # buffer = self.__client.recv(4096)
            # if not buffer:
            #     return
            # message = buffer.decode('utf-8')
            # messagebox.showinfo("", message,parent = self)
            a = None

    def butStartClick(self, event = None):
        # if not self.checkConnected():
        #     return
        # s = "StartID"
        # self.__client.send(s.encode('utf-8'))
        # s = self.ID.get().strip()
        # self.__client.send(s.encode('utf-8'))
        # buffer = self.__client.recv(4096)
        # if not buffer:
        #     return
        # message = buffer.decode('utf-8')
        # messagebox.showinfo("", message, parent = self)
        a = None


    def createWidgets(self):

        self.frame0 = tk.LabelFrame(self.root,bd=1,background="black")
        self.frame0.place(x=0, y=0, height=500, width=120)

        self.frame1 = tk.LabelFrame(self.root,bd=1,background="black")
        self.frame1.place(x=120, y=0, height=503, width=883)

        img = Image.open("F:\HCMUS-Năm 2\Học kì 2\Mạng máy tính\Controller-Application-Using-Socket\Client\logo.jpg")
        #img = img.resize((100,100))
        self.img=ImageTk.PhotoImage(img)
        self.theme=tk.Label(self.frame0,image=self.img,background="black")
        self.theme.place(x=25, y=45)
        img.close()

        self.ipConnect = tk.StringVar()
        self.ipConnect.set("Enter IP address")
        self.txtIP = tk.Entry(self.frame0, textvariable = self.ipConnect)
        self.txtIP.place(x=10, y=200, height=22, width=100)
        self.txtIP.configure(background="white", relief="groove")
        self.txtIP.bind("<Key-Return>", self.butConnectClick)
        
        #flat, groove, raised, ridge, solid, or sunken
        self.butConnect = tk.Button(self.frame0,text = "Connect", relief="groove", bg="#d6d6d6")
        self.butConnect["command"] = self.butConnectClick
        self.butConnect.place(x=10, y=250, height=22, width=100)

        self.butDisconnect = tk.Button(self.frame0,text = "Disconnect", relief="groove", bg="#d6d6d6")
        self.butDisconnect["command"] = self.butDisconnectClick
        self.butDisconnect.place(x=10, y=468, height=22, width=100)
        
        noteBookStyle = ttk.Style(self.frame1)
        noteBookStyle.theme_use('default')
        noteBookStyle.configure("TNotebook", background="black", tabposition='wn')
        noteBookStyle.configure("TNotebook.Tab", font=('Lato', 8, BOLD), justify="center", background="black", foreground="white", ANCHOR="c")
        noteBookStyle.map("TNotebook.Tab", background= [("selected", "white")],foreground=[("selected", "black")])

        tabFrameStyle = ttk.Style(self.frame1)
        tabFrameStyle.configure("TFrame", background="black")

        treeViewStyle = ttk.Style(self.frame1)
        treeViewStyle.configure("Treeview", background="black", foreground="white", fieldbackground="black", )
        treeViewStyle.configure("Treeview.Heading", font=('Lato', 12, BOLD), background="black", foreground='white')
        treeViewStyle.configure("Treeview.Item", font=('Lato', 12), background="black", foreground='green')
        
        self.tabControl = ttk.Notebook(self.frame1,style="TNotebook")
        self.tabControl.pack(expand=1,fill="both")

        self.tab1 = ttk.Frame(self.tabControl,style="TFrame")
        self.tabControl.add(self.tab1,text="APPS\nCONTROLER") 
        #createTab1Widget(self.tab1)

        self.tab1.frame0 = tk.Frame(self.tab1,background="black")
        self.tab1.frame0.place(x=0, y=0, height=440, width=500)
        self.tab1.tv1 = ttk.Treeview(self.tab1.frame0)
        self.tab1.tv1.place(relheight=1, relwidth=1)
        self.tab1.treescrolly = tk.Scrollbar(self.tab1.frame0, orient="vertical", command=self.tab1.tv1.yview)
        self.tab1.treescrollx = tk.Scrollbar(self.tab1.frame0, orient="horizontal", command=self.tab1.tv1.xview)
        self.tab1.tv1.configure(xscrollcommand=self.tab1.treescrollx.set, yscrollcommand=self.tab1.treescrolly.set)
        self.tab1.treescrollx.pack(side="bottom", fill="x")
        self.tab1.treescrolly.pack(side="right", fill="y")
        self.tab1.tv1["columns"] = ("1", "2", "3")
        self.tab1.tv1["show"] = "headings"
        self.tab1.tv1.heading(1, text = "Application 's Name")
        self.tab1.tv1.heading(2, text = "Application 's ID")
        self.tab1.tv1.heading(3, text = "Thread")
        self.tab1.tv1.column(1, width = 100)
        self.tab1.tv1.column(2, width = 75)
        self.tab1.tv1.column(3, width = 75)
        self.tab1.apps = []
        # row=["Google Chorme","0000001","1234567"]
        # for i in range(100):
        #     self.tab1.tv1.insert("", "end", values=row, tags="a")
        #     self.tab1.tv1.tag_configure("a", background="black", foreground="white")
        

        self.tab1.butRefresh = tk.Button(self.tab1,text = "Refresh", relief="groove", bg="black",fg="white",font=("Lato",15))
        self.tab1.butRefresh["command"] = self.butRefreshClick
        self.tab1.butRefresh.place(x=0, y=440, height=60, width=150)

        self.tab1.killID = tk.StringVar()
        self.tab1.killID.set("Enter ID")
        self.tab1.KillIDEntry = tk.Entry(self.tab1, textvariable = self.tab1.killID)
        self.tab1.KillIDEntry.place(x=150, y=440, height=30, width=250)
        self.tab1.KillIDEntry.configure(bg="black",fg="white",insertbackground="white",bd=3,font=("Lato",10))
        self.tab1.KillIDEntry.bind("<Key-Return>", self.butKillClick)

        self.tab1.butKill = tk.Button(self.tab1,text = "Kill", relief="groove", bg="black",fg="white",font=("Lato",10))
        self.tab1.butKill["command"] = self.butKillClick
        self.tab1.butKill.place(x=400, y=440, height=30, width=100)

        self.tab1.startID = tk.StringVar()
        self.tab1.startID.set("Enter Name")
        self.tab1.StartIDEntry = tk.Entry(self.tab1, textvariable = self.tab1.startID)
        self.tab1.StartIDEntry.place(x=150, y=470, height=30, width=250)
        self.tab1.StartIDEntry.configure(bg="black",fg="white",insertbackground="white",bd=3,font=("Lato",10))
        self.tab1.StartIDEntry.bind("<Key-Return>", self.butStartClick)

        self.tab1.butStart = tk.Button(self.tab1,text = "Start", relief="groove", bg="black",fg="white",font=("Lato",10))
        self.tab1.butStart["command"] = self.butStartClick
        self.tab1.butStart.place(x=400, y=470, height=30, width=100)










        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2,text="PROCESSES\nCONTROLER") 

        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3,text="FTP\nCONTROLER")
        
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4,text="KEYBOARD\nCONTROLER")

        self.tab5 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab5,text="MAC\n   ADDRESS  ")

        self.tab6 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab6,text="POWER\nCONTROLER") 
               
        self.tab7 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab7,text="STREAMING\nCONTROLER")



root=tk.Tk()
#root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
controler=Client(root)
root.mainloop()