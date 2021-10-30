import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import END,INSERT

PORT = 106

clientSocket = None

def CloseButton(root):
    s = "Quit"
    clientSocket.send(s.encode("utf-8"))
    root.destroy()

class Client(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill = "both", expand = True)
        self.configure(background="black")
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

    def createWidgets(self):
        self.ipConnect = tk.StringVar()
        self.ipConnect.set("Enter IP address")
        self.txtIP = tk.Entry(self, textvariable = self.ipConnect)
        self.txtIP.place(x=10, y=10, height=22, width=240)
        self.txtIP.configure(background="white", relief="groove")
        self.txtIP.bind("<Key-Return>", self.butConnectClick)
        
        #flat, groove, raised, ridge, solid, or sunken
        self.butConnect = tk.Button(self,text = "Connect", relief="groove", bg="#d6d6d6")
        self.butConnect["command"] = self.butConnectClick
        self.butConnect.place(x=260, y=10, height=22, width=100)

        

root = tk.Tk()
app = Client(root)
app.master.title("Client")
app.master.minsize(370, 252)
app.mainloop()  