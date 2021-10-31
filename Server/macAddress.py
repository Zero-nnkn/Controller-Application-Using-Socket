import ctypes
from tkinter.constants import NONE
import psutil
import socket

class MacAddress():
    def __init__(self, clientSocket):
        self.__client = clientSocket

    def getMacAddresses(self,family):
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == family:
                    yield (interface, (snic.address, snic.netmask))

    def sendMacAddress(self):

        ipv4s = dict(self.getMacAddresses(socket.AF_INET))
        macs = list(self.getMacAddresses(psutil.AF_LINK))
        mac2ipv4 = {macs[k][0]: ipv4s[k] for k in set(macs) & set(ipv4s)}

        print(macs)
        
        



