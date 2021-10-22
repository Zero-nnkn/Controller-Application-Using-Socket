import uuid

class macAddress():
    def __init__(self, clientSocket):
        self.client = clientSocket

    def getMac():
        return hex(uuid.getnode())