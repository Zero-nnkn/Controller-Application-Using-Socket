import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import END,INSERT
from PIL import Image
from PIL import ImageTk
import json
import os

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
        pr = ProcessRunning(root)
        s = "Process Running"
        pr.master.title(s)
        pr.master.minsize(290, 240)
        
    def butAppClick(self):
        if not self.checkConnected():
           return
        s = "APP"
        clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        root.attributes("-topmost", True)
        ar= AppRunning(root)
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
        ss = Screenshot(root)
        s = "Screenshot"
        ss.master.title("Screenshot")
        ss.master.minsize(400, 271)

    def butEditRegClick(self):
        if not self.checkConnected():
           return
        s = "REGISTRY"
        clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        root.attributes("-topmost", True)
        er = EditRegistry(root)
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
        ks = KeyStroke(root)
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

class ProcessRunning(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True

    def butKillClick(self):
        if not self.checkConnected():
           return
        s = "Kill"
        clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        root.attributes("-topmost", True)
        kl = Kill(root)
        kl.master.title(s)
        kl.master.minsize(280, 43)
        
    def butViewClick(self):
        if not self.checkConnected():
           return
        s = "View"
        clientSocket.send(s.encode('utf-8'))
        size = int(clientSocket.recv(10).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        self.processes = []
        buffer = "".encode("utf-8")
        while size > 0:
               data = clientSocket.recv(4096)
               size -= len(data)
               buffer += data
        self.processes = json.loads(buffer.decode("utf-8"))
        self.butDelClick()
        rows = self.processes
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
        clientSocket.send(s.encode('utf-8')) 
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
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
        self.tv1.heading(1, text = "Process 's Name")
        self.tv1.heading(2, text = "Process 's ID")
        self.tv1.heading(3, text = "Thread")
        self.tv1.column(1, width = 100)
        self.tv1.column(2, width = 65)
        self.tv1.column(3, width = 75)
        self.processes = []

class AppRunning(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True

    def butKillClick(self):
        if not self.checkConnected():
           return
        s = "Kill"
        clientSocket.send(s.encode('utf-8'))
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
        root.attributes("-topmost", True)
        kl = Kill(root)
        kl.master.title(s)
        kl.master.minsize(280, 43)
        
    def butViewClick(self):
        if not self.checkConnected():
           return
        s = "View"
        clientSocket.send(s.encode('utf-8'))
        size = int(clientSocket.recv(10).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        self.apps = []
        buffer = "".encode("utf-8")
        while size > 0:
               data = clientSocket.recv(4096)
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
        clientSocket.send(s.encode('utf-8')) 
        root = tk.Toplevel()
        root.protocol('WM_DELETE_WINDOW', lambda: CloseButton(root))
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

class Screenshot(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True

    def butTakeClick(self):
        if not self.checkConnected():
           return
        s = "Take"
        clientSocket.send(s.encode('utf-8'))
        size = int(clientSocket.recv(32).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        width = int(clientSocket.recv(32).decode('utf-8'))
        clientSocket.send("OK".encode('utf-8'))
        height = int(clientSocket.recv(32).decode("utf-8"))
        clientSocket.send("OK".encode('utf-8'))

        img = "".encode('utf-8')
        while size > 0:
           data = clientSocket.recv(4096)
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

class EditRegistry(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True
    
    def butBrowseClick(self, event = None):
        s = "Browse"
        sfile = filedialog.askopenfilename(initialdir=os.getcwd(), title=s, filetypes=[("reg file",".reg"), ("all file",".*")], parent = self)
        self.Path1.config(state="normal")
        self.Path1.delete("1.0", END)
        self.Path1.insert("1.0", sfile)
        self.Path1.place(x=0, y=0, height=22, width=335)
        self.Path1.config(state="disabled")
        if sfile == "":
            return
        try:
            f = open(sfile, "r")
        except:
            messagebox.showinfo("Error", "Error",parent = self)
        content = f.read()
        if content == None:
            return
        self.Content.delete("1.0", END)
        self.Content.insert("1.0", content)
        f.close()
        
    def butSend1Click(self, event = None):
        s = "Reg"
        clientSocket.send(s.encode('utf-8'))
        content = self.Content.get('1.0', END)
        clientSocket.send(content.encode('utf-8'))
        message = clientSocket.recv(100).decode('utf-8')
        messagebox.showinfo("", message,parent = self)

    def butSend2Click(self, event = None):
        s = "Send"
        clientSocket.send(s.encode('utf-8'))
        check = clientSocket.recv(10)

        s = self.box1.get().strip()
        clientSocket.send(s.encode('utf-8'))
        check = clientSocket.recv(10)

        s = self.Path2.get("1.0", END).strip()
        clientSocket.send(s.encode('utf-8'))
        check = clientSocket.recv(10)

        s = self.Name.get("1.0", END).strip()
        clientSocket.send(s.encode('utf-8'))
        check = clientSocket.recv(10)

        s = self.Value.get("1.0", END).strip()
        clientSocket.send(s.encode('utf-8'))
        check = clientSocket.recv(10)

        s = self.box2.get().strip()
        clientSocket.send(s.encode('utf-8'))

        message = clientSocket.recv(1024).decode('utf-8')
        self.resView.config(state = "normal")
        self.resView.insert(END, message + "\n")
        self.resView.config(state = "disable")

    def butDelClick(self, event = None):
        self.resView.config(state = "normal")
        self.resView.delete("1.0", END)
        self.resView.config(state = "disable")

    def chooseFunc(self, event = None):
        func = self.box1.get().strip()
        if func == "Get value":
            self.Name.config(state = "normal")
            self.Value.config(state = "disabled")
            self.box2.config(state = "disabled")
        elif func == "Set value":
            self.Name.config(state = "normal")
            self.Value.config(state = "normal")
            self.box2.config(state = "normal")
        elif func == "Delete value":
            self.Name.config(state = "normal")
            self.Value.config(state = "disabled")
            self.box2.config(state = "disabled")
        elif func == "Create key":
            self.Name.config(state = "disabled")
            self.Value.config(state = "disabled")
            self.box2.config(state = "disabled")
        elif func == "Delete key":
            self.Name.config(state = "disabled")
            self.Value.config(state = "disabled")
            self.box2.config(state = "disabled")
        else:
            return

    def createWidgets(self):
        self.frame0 = tk.LabelFrame(self)
        self.frame0.place(x=10, y=10, height=27, width=340)
        self.Path1 = tk.Text(self.frame0)
        self.Path1.insert(INSERT, "File path...")
        self.Path1.place(x=0, y=0, height=22, width=335)
        self.treescrolly1 = tk.Scrollbar(self.frame0, orient="vertical", command=self.Path1.yview)
        self.Path1.config(yscrollcommand=self.treescrolly1.set)
        self.treescrolly1.pack(side="right", fill="y")
        self.Path1.config(state="disabled")
        
        self.butBrowse = tk.Button(self, text = "Browse", relief="groove", bg="#d6d6d6")
        self.butBrowse["command"] = self.butBrowseClick
        self.butBrowse.place(x=360, y=10, height=22, width=100)

        self.Content = tk.Text(self)
        self.Content.insert(INSERT, "File 's content")
        self.Content.place(x=10, y=42, height=100, width=340)
        
        self.butSend1 = tk.Button(self, text = "Send content", relief="groove", bg="#d6d6d6")
        self.butSend1["command"] = self.butSend1Click
        self.butSend1.place(x=360, y=42, height=100, width=100)

        self.frame1 = tk.LabelFrame(self, text="Edit value directly")
        self.frame1.place(x=10, y=152, height=267, width=450)

        func = ('Get value', 'Set value', 'Delete value', 'Create key', 'Delete key')
        self.func = tk.StringVar()
        self.func.set("Choose function")
        self.box1 = ttk.Combobox(self.frame1, textvariable=self.func)
        self.box1['values'] = func
        self.box1.place(x=10, y=10, height = 22, width=425)
        self.box1.bind('<<ComboboxSelected>>', self.chooseFunc)

        self.Path2 = tk.Text(self.frame1)
        self.Path2.insert(INSERT, "Input file path")
        self.Path2.place(x=10, y=42, height=22, width=425)  

        self.Name = tk.Text(self.frame1)
        self.Name.insert(INSERT, "Name value")
        self.Name.place(x=10, y=74, height=22, width=135)

        self.Value = tk.Text(self.frame1)
        self.Value.insert(INSERT, "Value")
        self.Value.place(x=155, y=74, height=22, width=135)
        
        dataType = ('String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String')
        self.dataType = tk.StringVar()
        self.dataType.set("Data 's type")
        self.box2 = ttk.Combobox(self.frame1, textvariable=self.dataType)
        self.box2['values'] = dataType
        self.box2.place(x=300, y=74, height = 22, width=135)

        self.frame2 = tk.LabelFrame(self.frame1)
        self.frame2.place(x=10, y=106, height=100, width=425)
        self.resView = tk.Text(self.frame2)
        self.resView.insert(INSERT, "")
        self.resView.place(x=0, y=0, height=100, width=425)
        self.treescrolly2 = tk.Scrollbar(self.frame2, orient="vertical", command=self.resView.yview)
        self.resView.config(yscrollcommand=self.treescrolly2.set)
        self.treescrolly2.pack(side="right", fill="y")
        self.resView.config(state = "disable")

        self.butSend2 = tk.Button(self.frame1, text = "Send", relief="groove", bg="#d6d6d6")
        self.butSend2["command"] = self.butSend2Click
        self.butSend2.place(x=98, y=216, height=22, width=100)

        self.butDel = tk.Button(self.frame1, text = "Delete", relief="groove", bg="#d6d6d6")
        self.butDel["command"] = self.butDelClick
        self.butDel.place(x=248, y=216, height=22, width=100)
        
class KeyStroke(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True
    
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
        self.KeyLog = clientSocket.recv(4096).decode("utf-8")

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

class Kill(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True

    def butKillClick(self, event = None):
        if not self.checkConnected():
           return
        s = "KillID"
        clientSocket.send(s.encode('utf-8'))
        s = self.ID.get().strip()
        clientSocket.send(s.encode('utf-8'))
        buffer = clientSocket.recv(4096)
        if not buffer:
            return
        message = buffer.decode('utf-8')
        messagebox.showinfo("", message,parent = self)
        a = None

    def createWidgets(self):
        self.ID = tk.StringVar()
        self.ID.set("Enter ID")
        self.KillID = tk.Entry(self, textvariable = self.ID)
        self.KillID.place(x=10, y=10, height=23, width=180)
        self.KillID.configure(background="white")
        self.KillID.bind("<Key-Return>", self.butKillClick)
        
        self.butKill = tk.Button(self,text = "Kill", relief="groove", bg="#d6d6d6")
        self.butKill["command"] = self.butKillClick
        self.butKill.place(x=200, y=10, height=23, width=70)

class Start(tk.Frame):
    
    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.createWidgets()

    def checkConnected(self):
        if clientSocket == None:
            messagebox.showinfo("Error", "Connection errors",parent = self)
            return False
        else: return True

    def butStartClick(self, event = None):
        if not self.checkConnected():
           return
        s = "StartID"
        clientSocket.send(s.encode('utf-8'))
        s = self.ID.get().strip()
        clientSocket.send(s.encode('utf-8'))
        buffer = clientSocket.recv(4096)
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

root = tk.Tk()
app = Client(root)
app.master.title("Client")
app.master.minsize(370, 252)
app.mainloop()  