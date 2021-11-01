import ctypes
from tkinter.constants import NONE
import psutil
import socket
import json

class MacAddress():
    def __init__(self, clientSocket):
        self.__client = clientSocket

    def startListening(self):
        request = ""
        while True:
            request = self.self.__client.recv(1024).decode("utf-8")
            if not request:
                break
            if request == "macaddress":
                self.sendMacAddress()
            else: #Quit
                return

    def getMacAddresses(self):
        for interface, snics in psutil.net_if_addrs().items():
            ip = None
            mac = None
            netmask = None
            for snic in snics:
                if snic.family == socket.AF_INET:
                    ip = snic.address
                    netmask = snic.netmask
                if snic.family == psutil.AF_LINK:
                    mac = snic.address
            yield (interface, mac, ip, netmask)

    def sendMacAddress(self):
        mac2ipv4 = list(self.getMacAddresses())
        dataToSend = json.dumps(mac2ipv4).encode('utf-8') 
        size = len(dataToSend)
        self.__client.sendall(str(size).encode('utf-8'))
        check = self.__client.recv(10)
        self.__client.sendall(dataToSend)
        

