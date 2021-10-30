import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import json
import Start
import Kill

class AppRunning(tk.Frame):
    def __init__(self, clientSocket, master=None):
        self.__client = clientSocket
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if self.__client == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True

    def CloseButton2(self):
        s = "Quit"
        self.__client.send(s.encode("utf-8"))
        self.destroy()

    def butKillClick(self):
        if not self.checkConnected():
           return
        s = "Kill"
        self.__client.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: self.CloseButton2(root))
        root.attributes("-topmost", True)
        kl = Kill(root)
        kl.master.title(s)
        kl.master.minsize(280, 43)
        
    def butViewClick(self):
        if not self.checkConnected():
           return
        s = "View"
        self.__client.send(s.encode('utf-8'))
        size = int(self.__client.recv(10).decode('utf-8'))
        self.__client.send("OK".encode('utf-8'))
        self.apps = []
        buffer = "".encode("utf-8")
        while size > 0:
               data = self.__client.recv(4096)
               size -= len(data)
               buffer += data
        self.apps = json.loads(buffer.decode("utf-8"))
        self.butDelClick()
        rows = self.apps
        for row in rows:
            self.tv1.insert("", "end", values=row)
    
    def butDelClick(self):
        rows = self.tv1.get_children()
        if rows != '()':
            for row in rows:
                self.tv1.delete(row)
        
    def butStartClick(self):
        if not self.checkConnected():
           return
        s = "Start"
        self.__client.send(s.encode('utf-8')) 
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: self.CloseButton2(root))
        root.attributes("-topmost", True)
        st = Start(root)
        st.master.title(s)
        st.master.minsize(280, 43) 

    def createWidgets(self):
        self.butKill = tk.Button(self, text = "Kill", relief="groove", bg="#d6d6d6")
        self.butKill["command"] = self.butKillClick
        self.butKill.place(x=10, y=10, height=50, width=60)

        self.butView = tk.Button(self, text = "View", relief="groove", bg="#d6d6d6")
        self.butView["command"] = self.butViewClick
        self.butView.place(x=80, y=10, height=50, width=60)

        self.butDel = tk.Button(self, text = "Delete", relief="groove", bg="#d6d6d6")
        self.butDel["command"] = self.butDelClick
        self.butDel.place(x=150, y=10, height=50, width=60)
   
        self.butStart = tk.Button(self, text = "Start", relief="groove", bg="#d6d6d6")
        self.butStart["command"] = self.butStartClick
        self.butStart.place(x=220, y=10, height=50, width=60)

        self.frame1 = tk.LabelFrame(self, text="")
        self.frame1.place(x=10, y=70, height=160, width=270)
        self.tv1 = ttk.Treeview(self.frame1)
        self.tv1.place(relheight=1, relwidth=1)
        self.treescrolly = tk.Scrollbar(self.frame1, orient="vertical", command=self.tv1.yview)
        self.treescrollx = tk.Scrollbar(self.frame1, orient="horizontal", command=self.tv1.xview)
        self.tv1.configure(xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set)
        self.treescrollx.pack(side="bottom", fill="x")
        self.treescrolly.pack(side="right", fill="y")
        self.tv1["columns"] = ("1", "2", "3")
        self.tv1["show"] = "headings"
        self.tv1.heading(1, text = "Application 's Name")
        self.tv1.heading(2, text = "Application 's ID")
        self.tv1.heading(3, text = "Thread")
        self.tv1.column(1, width = 100)
        self.tv1.column(2, width = 65)
        self.tv1.column(3, width = 75)
        self.apps = []
