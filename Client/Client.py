import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import END,INSERT

import ProcessRunning
import AppRunning
import ScreenShot
import KeyStroke
import EditRegistry
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

    def butProcessClick(self):
        if not self.checkConnected():
           return
        s = "PROCESS"
        clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        root.attributes("-topmost", True)
        pr = ProcessRunning.ProcessRunning(clientSocket, root)
        s = "Process Running"
        pr.master.title(s)
        pr.master.minsize(290, 240)
        pr.mainloop()
        
    def butAppClick(self):
        if not self.checkConnected():
           return
        s = "APP"
        clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        root.attributes("-topmost", True)
        ar= AppRunning.AppRunning(clientSocket, root)
        s = "Application running"
        ar.master.title(s)
        ar.master.minsize(290, 240)

    def butShutdownClick(self):
        if not self.checkConnected():
           return
        s = "SHUTDOWN"
        clientSocket.send(s.encode('utf-8'))
        messagebox.showinfo("", "Server shut down after 60s")

    def butScreenshotClick(self):
        if not self.checkConnected():
           return
        s = "SCREENSHOT"
        clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        ss = ScreenShot.Screenshot(clientSocket, root)
        s = "Screenshot"
        ss.master.title("Screenshot")
        ss.master.minsize(400, 271)

    def butEditRegClick(self):
        # if not self.checkConnected():
        #    return
        s = "REGISTRY"
        # clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        root.attributes("-topmost", True)
        er = EditRegistry.EditRegistry(clientSocket, root)
        s = "Edit Registry"
        er.master.title(s)
        er.master.minsize(470, 431)

    def butKeystrokeClick(self):    
        if not self.checkConnected():
           return
        s = "KEYSTROKE"
        clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        root.attributes("-topmost", True)
        ks = KeyStroke.KeyStroke(clientSocket, root)
        s = "Keystroke"
        ks.master.title(s)
        ks.master.minsize(290, 240)

    def butExitClick(self):
        if not self.checkConnected():
           self.quit()
        else:
            s = "EXIT"
            clientSocket.send(s.encode('utf-8'))
            clientSocket.close()
            self.quit()
            
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

        self.butProcess = tk.Button(self,text = "Process\nRunning", relief="groove", bg="#d6d6d6")
        self.butProcess["command"] = self.butProcessClick
        self.butProcess.place(x=10, y=42, height=200, width=80)

        self.butApp = tk.Button(self,text = "App Running", relief="groove", bg="#d6d6d6")
        self.butApp["command"] = self.butAppClick
        self.butApp.place(x=100, y=42, height=60, width=150)

        self.butShutdown = tk.Button(self,text = "Shut\nDown", relief="groove", bg="#d6d6d6")
        self.butShutdown["command"] = self.butShutdownClick
        self.butShutdown.place(x=100, y=112, height=60, width=50)

        self.butScreenshot = tk.Button(self,text = "Screenshot", relief="groove", bg="#d6d6d6")
        self.butScreenshot["command"] = self.butScreenshotClick
        self.butScreenshot.place(x=160, y=112, height=60, width=90)

        self.butEditReg = tk.Button(self,text = "Edit Registry", relief="groove", bg="#d6d6d6")
        self.butEditReg["command"] = self.butEditRegClick
        self.butEditReg.place(x=100, y=182, height=60, width=190)

        self.butKeystroke = tk.Button(self,text = "Keystroke", relief="groove", bg="#d6d6d6")
        self.butKeystroke["command"] = self.butKeystrokeClick
        self.butKeystroke.place(x=260, y=42, height=130, width=100)

        self.butExit = tk.Button(self,text = "Exit", relief="groove", bg="#d6d6d6")
        self.butExit["command"] = self.butExitClick
        self.butExit.place(x=300, y=182, height=60, width=60)
        
root = tk.Tk()
app = Client(root)
app.master.title("Client")
app.master.minsize(370, 252)
app.mainloop()  