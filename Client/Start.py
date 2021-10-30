import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Start(tk.Frame):
    
    def __init__(self, clientSocket, master = None):
        self.__client = clientSocket
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if self.__client == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True

    def butStartClick(self, event = None):
        if not self.checkConnected():
           return
        s = "StartID"
        self.__client.send(s.encode('utf-8'))
        s = self.ID.get().strip()
        self.__client.send(s.encode('utf-8'))
        buffer = self.__client.recv(4096)
        if not buffer:
            return
        message = buffer.decode('utf-8')
        messagebox.showinfo("", message, parent = self)
        a = None

    def createWidgets(self):    
        self.ID = tk.StringVar()
        self.ID.set("Enter Name")
        self.StartID = tk.Entry(self, textvariable = self.ID)
        self.StartID.place(x=10, y=10, height=23, width=180)
        self.StartID.configure(background="white")
        self.StartID.bind("<Key-Return>", self.butStartClick)
        
        self.butStart = tk.Button(self,text = "Start", relief="groove", bg="#d6d6d6")
        self.butStart["command"] = self.butStartClick
        self.butStart.place(x=200, y=10, height=23, width=70)
