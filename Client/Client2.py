import socket
import tkinter as tk
from tkinter import Image, messagebox
from tkinter import END,INSERT

from PIL import Image
from PIL import ImageTk

PORT = 106

clientSocket = None

def CloseButton(root):
    s = "Quit"
    clientSocket.send(s.encode("utf-8"))
    root.destroy()

class Client(tk.Frame):

    def __init__(self, root):
            self.root=root
            self.root.title("ONLINE LIBRARY")
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

    def createWidgets(self):

        self.frame0 = tk.LabelFrame(self.root,bd=1,background="black")
        self.frame0.place(x=0, y=0, height=500, width=200)

        self.frame1 = tk.LabelFrame(self.root,bd=1,background="black")
        self.frame1.place(x=200, y=0, height=500, width=500)

        img = Image.open("F:\HCMUS-Năm 2\Học kì 2\Mạng máy tính\Controller-Application-Using-Socket\Client\logo.jpg")
        img = img.resize((100,100))
        self.img=ImageTk.PhotoImage(img)
        self.theme=tk.Label(self.frame0,image=self.img,background="black")
        self.theme.place(x=45, y=45)
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
        self.butConnect.place(x=50, y=250, height=22, width=100)

        

root=tk.Tk()
#root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
controler=Client(root)
root.mainloop()