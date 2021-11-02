import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def checkConnected(self):
        if self.__client == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True

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

def createTab1Widget(self):

    # style = ttk.Style(self)
    # style.theme_use("clam")
    # style.configure(".", font=('Lato', 7),background="black", foreground="purple",tabposition='wn')
    # style.configure("Treeview", background="black", foreground="white", fieldbackground="black", )
    # style.configure("Treeview.Heading", font=('Lato', 12), background="black", foreground='green')

    # self.frame = tk.LabelFrame(self, text="",background="black")
    # self.frame.place(x=0, y=0, height=500, width=500)
    # self.tv1 = ttk.Treeview(self.frame)
    # self.tv1.place(relheight=1, relwidth=1)
    # self.treescrolly = tk.Scrollbar(self.frame, orient="vertical", command=self.tv1.yview)
    # self.treescrollx = tk.Scrollbar(self.frame, orient="horizontal", command=self.tv1.xview)
    # self.tv1.configure(xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set)
    # self.treescrollx.pack(side="bottom", fill="x")
    # self.treescrolly.pack(side="right", fill="y")
    # self.tv1["columns"] = ("1", "2", "3")
    # self.tv1["show"] = "headings"
    # self.tv1.heading(1, text = "Application 's Name")
    # self.tv1.heading(2, text = "Application 's ID")
    # self.tv1.heading(3, text = "Thread")
    # self.tv1.column(1, width = 100)
    # self.tv1.column(2, width = 65)
    # self.tv1.column(3, width = 75)
    # self.apps = []
    # row=["a","v","b"]
    # self.tv1.insert("", "end", values=row)

    # self.frame1 = tk.LabelFrame(self, text="",background="black")
    # self.frame1.place(x=0, y=0, height=500, width=500)

    # self.ID = tk.StringVar()
    # self.ID.set("Enter ID")
    # self.KillID = tk.Entry(self, textvariable = self.ID)
    # self.KillID.place(x=10, y=10, height=23, width=180)
    # self.KillID.configure(background="white")
    # self.KillID.bind("<Key-Return>", butKillClick)

    # self.butKill = tk.Button(self,text = "Kill", relief="groove", bg="#d6d6d6")
    # self.butKill["command"] = butKillClick
    # self.butKill.place(x=200, y=10, height=23, width=70)

    # self.ID = tk.StringVar()
    # self.ID.set("Enter Name")
    # self.StartID = tk.Entry(self, textvariable = self.ID)
    # self.StartID.place(x=10, y=10, height=23, width=180)
    # self.StartID.configure(background="white")
    # self.StartID.bind("<Key-Return>", butStartClick)

    # self.butStart = tk.Button(self,text = "Start", relief="groove", bg="#d6d6d6")
    # self.butStart["command"] = butStartClick
    # self.butStart.place(x=200, y=10, height=23, width=70)

    a= None
