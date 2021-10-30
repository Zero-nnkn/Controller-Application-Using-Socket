import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter.constants import END, INSERT

class EditRegistry(tk.Frame):
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
        self.__client.send(s.encode('utf-8'))
        content = self.Content.get('1.0', END)
        self.__client.send(content.encode('utf-8'))
        message = self.__client.recv(100).decode('utf-8')
        messagebox.showinfo("", message,parent = self)

    def butSend2Click(self, event = None):
        s = "Send"
        self.__client.send(s.encode('utf-8'))
        check = self.__client.recv(10)

        s = self.box1.get().strip()
        self.__client.send(s.encode('utf-8'))
        check = self.__client.recv(10)

        s = self.Path2.get("1.0", END).strip()
        self.__client.send(s.encode('utf-8'))
        check = self.__client.recv(10)

        s = self.Name.get("1.0", END).strip()
        self.__client.send(s.encode('utf-8'))
        check = self.__client.recv(10)

        s = self.Value.get("1.0", END).strip()
        self.__client.send(s.encode('utf-8'))
        check = self.__client.recv(10)

        s = self.box2.get().strip()
        self.__client.send(s.encode('utf-8'))

        message = self.__client.recv(1024).decode('utf-8')
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
 