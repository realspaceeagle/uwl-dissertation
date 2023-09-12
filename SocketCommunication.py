import json

from p2pnetwork.node import Node
from PeerDiscoveryHandler import PeerDiscoveryHandler
from SocketConnector import SocketConnector
from BlockchainUtils import BlockchainUtils


class SocketCommunication(Node):

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        # super constructor is refereed to the constructor of the node class
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)

    def connectToFirstNode(self):
        if self.socketConnector.port != 10001:
            self.connect_with_node('localhost', 10001)
            # we are not the very first node we can connect to that node

    # open the port for communication
    def startSocketCommunication(self,node):
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()

    def inbound_node_connected(self, connected_node):
        # print('inbound connection')
        # you are a node if other node wants to connect to you , It is called inbound node connection
        # self.send_to_node(connected_node, 'Hi I am the node you connected to')
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        # print('outbound connection')
        # self.send_to_node(connected_node, 'I am the node initialized the connection')
        self.peerDiscoveryHandler.handshake(connected_node)

    def node_message(self, connected_node, message):
        message = BlockchainUtils.decode(json.dumps(message))
        if message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == 'TRANSACTION':
            transaction = message.data
            self.node.handleTransaction(transaction) # need to add chain in fo getting to know other each other chain

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)
