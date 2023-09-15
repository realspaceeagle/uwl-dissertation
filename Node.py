from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Blockchain import Blockchain


class Node():

    def __init__(self, ip, port):
        # get the transactions and store them
        # we don't need them because file uploading one transaction stored as one block
        # self.transactionPool = TransactionPool()
        # we dont need wallet also
        # self.allet = Wallet()

        # node without ability to conncect with other node is useless so we initialized
        self.p2p = None
        self.ip = ip
        self.port = port
        # we need block chain itself
        self.blockchain = Blockchain()

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self,apiPort):
        self.api = NodeAPI()
        self.api.start(apiPort)
        self.api.injectNode(self) # GET TO KNOW ABOUT WORKING NODE
        print("startAPI working")

