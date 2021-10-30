import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.constants import END, INSERT

from PIL import Image, ImageTk

class Screenshot(tk.Frame):
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

    def butTakeClick(self):
        if not self.checkConnected():
           return
        s = "Take"
        self.__client.send(s.encode('utf-8'))
        size = int(self.__client.recv(32).decode('utf-8'))
        self.__client.send("OK".encode('utf-8'))
        width = int(self.__client.recv(32).decode('utf-8'))
        self.__client.send("OK".encode('utf-8'))
        height = int(self.__client.recv(32).decode("utf-8"))
        self.__client.send("OK".encode('utf-8'))

        img = "".encode('utf-8')
        while size > 0:
           data = self.__client.recv(4096)
           size -= len(data)
           img += data
        self.img = Image.frombytes("RGB", (width,height), img)
        self.img = self.img.resize((1920, 1080))
        imgToView = self.img.resize((300, 250))
        self.imgTk = ImageTk.PhotoImage(imgToView)
        pic = tk.Label(self, image=self.imgTk)
        pic.image = self.imgTk
        pic.place(x=7, y=7)

        end = None

    def butSaveClick(self):
        if not self.checkConnected():
           return
        s = "Save"
        sfile = filedialog.asksaveasfilename(initialdir=os.getcwd(), title=s,defaultextension = ".png", filetypes=[("BMP File",".bmp"),("JPG File",".jpg"),("PNG File",".png")], parent = self)
        if sfile == None:
            return
        self.img.save(sfile)
        os.startfile(sfile)
        
    def createWidgets(self):
        self.butTakeClick()

        self.butTake = tk.Button(self, text = "Screenshot", relief="groove", bg="#d6d6d6")
        self.butTake["command"] = self.butTakeClick
        self.butTake.place(x=320, y=10, height=170, width=70)
        
        self.butSave = tk.Button(self, text = "Save", relief="groove", bg="#d6d6d6")
        self.butSave["command"] = self.butSaveClick
        self.butSave.place(x=320, y=190, height=70, width=70)
