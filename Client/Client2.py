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

    #GENERAL
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

    def on_tab_change(self,event=None):
        #tab = event.widget.tab('current')['text']
        # if tab == 'Tab1':
        #     #canvas3.unbind_all() 
        #     #canvas2.bind_all('<MouseWheel>', lambda event: canvas2.yview_scroll(int(-1 * (event.delta / 120)),"units"))
        # elif tab == 'Tab2':
        #     #canvas2.unbind_all()
        #     #canvas3.bind_all('<MouseWheel>', lambda event: canvas3.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        #print(tab)
        print(self.tabControl.tab(self.tabControl.select(),"text"))
       
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




    #TAB1 2 APP PROCESS
    def butRefreshClick(self, event = None):

        a=None

    def butKillClick(self, event = None):
            # if not self.checkConnected():
            #    return
            # s = "KillID"
            # clientSocket.send(s.encode('utf-8'))
            # s = self.ID.get().strip()
            # clientSocket.send(s.encode('utf-8'))
            # buffer = clientSocket.recv(4096)
            # if not buffer:
            #     return
            # message = buffer.decode('utf-8')
            # messagebox.showinfo("", message,parent = self)
            a = None

    def butStartClick(self, event = None):
        # if not self.checkConnected():
        #     return
        # s = "StartID"
        # clientSocket.send(s.encode('utf-8'))
        # s = self.ID.get().strip()
        # clientSocket.send(s.encode('utf-8'))
        # buffer = clientSocket.recv(4096)
        # if not buffer:
        #     return
        # message = buffer.decode('utf-8')
        # messagebox.showinfo("", message, parent = self)
        a = None




    #TAB3 FTP
    def butClientPreviousPathClick(self, event = None):

        a= None

    def butServerPreviousPathClick(self, event = None):

        a= None

    def do_popup1(self,event):
        try:
            self.tab3.popup1.selection = self.tab3.tv1.set(self.tab3.tv1.identify_row(event.y))
            self.tab3.popup1.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.tab3.popup1.grab_release()

    def do_popup2(self,event):
        try:
            self.tab3.popup2.selection = self.tab3.tv1.set(self.tab3.tv1.identify_row(event.y))
            self.tab3.popup2.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.tab3.popup2.grab_release()

    def copyToServer(self):


        print (self.tab3.popup1.selection)

    def deteteFile(self):

        print (self.tab3.popup1.selection)




    #TAB4 KEY
    def butHookClick(self):
        if not self.checkConnected():
           return
        s = "Hook"
        clientSocket.send(s.encode('utf-8'))
        
    def butUnhookClick(self):
        if not self.checkConnected():
           return
        s = "Unhook"
        clientSocket.send(s.encode('utf-8'))
    
    def butPrintClick(self):
        if not self.checkConnected():
           return
        s = "Print"
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





    #TAB5 MAC

    def butGetMACClick(self):

        a=None



    #TAB6 POWER
    def butLogOutClick(self,event=None):
        
        
        a=None

    def butShutDownClick(self,event=None):
        
        
        a=None




    #TAB7 STREAM

    def createWidgets(self):

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
        #treeViewStyle.configure("Treeview.Item", font=('Lato', 12), background="black", foreground='green')
        
        self.tabControl = ttk.Notebook(self.frame1,style="TNotebook")
        self.tabControl.pack(expand=1,fill="both")

        

        self.tabControl.bind('<<NotebookTabChanged>>', self.on_tab_change)
        

        
        self.tab1 = ttk.Frame(self.tabControl,style="TFrame")
        self.tabControl.add(self.tab1,text="APPS\nCONTROLER")

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
        row=["Google Chorme","0000001","1234567"]
        for i in range(10):
            self.tab1.tv1.insert("", "end", values=row, tags="a")
        
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





        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2,text="PROCESSES\nCONTROLER") 

        self.tab2.frame0 = tk.Frame(self.tab2,background="black")
        self.tab2.frame0.place(x=0, y=0, height=440, width=500)
        self.tab2.tv1 = ttk.Treeview(self.tab2.frame0)
        self.tab2.tv1.place(relheight=1, relwidth=1)
        self.tab2.treescrolly = tk.Scrollbar(self.tab2.frame0, orient="vertical", command=self.tab2.tv1.yview)
        self.tab2.treescrollx = tk.Scrollbar(self.tab2.frame0, orient="horizontal", command=self.tab2.tv1.xview)
        self.tab2.tv1.configure(xscrollcommand=self.tab2.treescrollx.set, yscrollcommand=self.tab2.treescrolly.set)
        self.tab2.treescrollx.pack(side="bottom", fill="x")
        self.tab2.treescrolly.pack(side="right", fill="y")
        self.tab2.tv1["columns"] = ("1", "2", "3")
        self.tab2.tv1["show"] = "headings"
        self.tab2.tv1.heading(1, text = "Process 's Name")
        self.tab2.tv1.heading(2, text = "Process 's ID")
        self.tab2.tv1.heading(3, text = "Thread")
        self.tab2.tv1.column(1, width = 100)
        self.tab2.tv1.column(2, width = 75)
        self.tab2.tv1.column(3, width = 75)
        self.tab2.processes = []
        row=["Coc Coc","0000002","4348398"]
        for i in range(10):
            self.tab2.tv1.insert("", "end", values=row, tags="a")
        
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





        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3,text="FTP\nCONTROLER")

        self.tab3.clientPath = "F\\"
        self.tab3.clientPathtxt = tk.Text(self.tab3)
        self.tab3.clientPathtxt.insert(INSERT,self.tab3.clientPath)
        self.tab3.clientPathtxt.configure(font=("Lato",10),relief="groove",bg="black",fg="white",cursor="circle",state="disabled")
        self.tab3.clientPathtxt.place(x=0,y=0,height=30,width=250)

        self.tab3.serverPath = "C:\\"
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
        # self.tab3.treescrollx = tk.Scrollbar(self.tab3.frame0, orient="horizontal", command=self.tab3.tv1.xview)
        # self.tab3.tv1.configure(xscrollcommand=self.tab3.treescrollx.set, yscrollcommand=self.tab3.treescrolly.set)
        # self.tab3.treescrollx.pack(side="bottom", fill="x")
        self.tab3.treescrolly.pack(side="right", fill="y")
        self.tab3.tv1["columns"] = ("1", "2", "3")
        self.tab3.tv1["show"] = "headings"
        self.tab3.tv1.heading(1, text = "Filename")
        self.tab3.tv1.heading(2, text = "Filesize")
        self.tab3.tv1.heading(3, text = "Filetype")
        self.tab3.tv1.column(1, width = 70)
        self.tab3.tv1.column(2, width = 40)
        self.tab3.tv1.column(3, width = 40)
        self.tab3.clientFolders = []
        row=["Google Chorme","0000001","1234567"]
        for i in range(10):
            self.tab3.tv1.insert("", "end", values=row, tags="a")
            self.tab3.tv1.tag_configure("a", background="black", foreground="white")

        self.tab3.popup1 = tk.Menu(self.tab3, tearoff=0)
        self.tab3.popup1.add_command(label="Copy", command=self.copyToServer)
        self.tab3.popup1.add_separator()
        self.tab3.tv1.bind("<Button-3>", self.do_popup1)

        self.tab3.frame1 = tk.Frame(self.tab3,background="black")
        self.tab3.frame1.place(x=250, y=60, height=440, width=250)
        self.tab3.tv2 = ttk.Treeview(self.tab3.frame1)
        self.tab3.tv2.place(relheight=1, relwidth=1)
        self.tab3.treescrolly = tk.Scrollbar(self.tab3.frame1, orient="vertical", command=self.tab3.tv2.yview)
        # self.tab3.treescrollx = tk.Scrollbar(self.tab3.frame1, orient="horizontal", command=self.tab3.tv2.xview)
        # self.tab3.tv2.configure(xscrollcommand=self.tab3.treescrollx.set, yscrollcommand=self.tab3.treescrolly.set)
        # self.tab3.treescrollx.pack(side="bottom", fill="x")
        self.tab3.treescrolly.pack(side="right", fill="y")
        self.tab3.tv2["columns"] = ("1", "2", "3")
        self.tab3.tv2["show"] = "headings"
        self.tab3.tv2.heading(1, text = "Filename")
        self.tab3.tv2.heading(2, text = "Filesize")
        self.tab3.tv2.heading(3, text = "Filetype")
        self.tab3.tv2.column(1, width = 70)
        self.tab3.tv2.column(2, width = 40)
        self.tab3.tv2.column(3, width = 40)
        self.tab3.serverFolder = []
        row=["Google Chorme","0000001","1234567"]
        for i in range(10):
            self.tab3.tv2.insert("", "end", values=row, tags="a")
            self.tab3.tv2.tag_configure("a", background="black", foreground="white")

        self.tab3.popup2 = tk.Menu(self.tab3, tearoff=0)
        self.tab3.popup2.add_command(label="Delete", command=self.copyToServer)
        self.tab3.popup2.add_separator()
        self.tab3.tv2.bind("<Button-3>", self.do_popup2)





        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4,text="KEYBOARD\nCONTROLER")

        self.tab4.butHook = tk.Button(self.tab4, text = "Hook",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butHook["command"] = self.butHookClick
        self.tab4.butHook.place(x=20, y=20, height=50, width=100)

        self.tab4.butUnhook = tk.Button(self.tab4, text = "Unhook",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butUnhook["command"] = self.butUnhookClick
        self.tab4.butUnhook.place(x=140, y=20, height=50, width=100)

        self.tab4.butPrint = tk.Button(self.tab4, text = "Print",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butPrint["command"] = self.butPrintClick
        self.tab4.butPrint.place(x=260, y=20, height=50, width=100)
   
        self.tab4.butDel = tk.Button(self.tab4, text = "Delete",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab4.butDel["command"] = self.butDelClick
        self.tab4.butDel.place(x=380, y=20, height=50, width=100)

        self.tab4.frame1 = tk.LabelFrame(self.tab4, text="")
        self.tab4.frame1.place(x=20, y=90, height=390, width=460)
        self.tab4.KeyView = tk.Text(self.tab4.frame1,font=("Lato",10),relief="groove",bg="black",fg="white",cursor="circle")
        self.tab4.KeyLog = ""
        self.tab4.KeyView.insert(INSERT, self.tab4.KeyLog)
        self.tab4.KeyView.config(state="disabled")
        self.tab4.KeyView.pack()





        self.tab5 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab5,text="MAC\n   ADDRESS  ")

        self.tab5.frame1 = tk.LabelFrame(self.tab5, text="")
        self.tab5.frame1.place(x=20, y=20, height=390, width=460)
        self.tab5.KeyView = tk.Text(self.tab5.frame1,font=("Lato",10),relief="groove",bg="black",fg="white",cursor="circle",insertbackground="white")
        self.tab5.KeyLog = "1443\n43434\n43434"
        self.tab5.KeyView.insert(INSERT, self.tab5.KeyLog)
        self.tab5.KeyView.pack()

        self.tab5.butGetMAC = tk.Button(self.tab5,text="Get MAC Address",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.tab5.butGetMAC["command"] = self.butGetMACClick
        self.tab5.butGetMAC.place(x=180, y=430, height=50, width=140)









        self.tab6 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab6,text="POWER\nCONTROLER")

        self.butLogOut = tk.Button(self.tab6,text = "Log out",font=("Lato",10),relief="groove",bg="black",fg="white",justify="center",cursor="circle")
        self.butLogOut["command"] = self.butLogOutClick
        self.butLogOut.place(x=10, y=10, height=30, width=100)

        self.butShutDown = tk.Button(self.tab6,text = "Shutdown",font=("Lato",10),relief="groove",bg="red",fg="white",justify="center",cursor="circle")
        self.butShutDown["command"] = self.butShutDownClick
        self.butShutDown.place(x=10, y=50, height=30, width=100)





        self.tab7 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab7,text="STREAMING\nCONTROLER")



root=tk.Tk()
#root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
controler=Client(root)
root.mainloop()