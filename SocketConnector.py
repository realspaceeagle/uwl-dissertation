
class SocketConnector:
    # used to store safe the ip and port of connection

    def __init__(self ,ip ,port):
        self.ip = ip
        self.port = port

    def equals(self ,connector):
        if connector.ip == self.ip and connector.port == self.port:
            return True
        else:
            return False
