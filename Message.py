class Message:

    def __init__(self, senderConnector, messageType, data):
        # senderConnector = combimnation of ipaddress and port
        self.senderConnector = senderConnector
        self.messageType = messageType
        self.data = data
