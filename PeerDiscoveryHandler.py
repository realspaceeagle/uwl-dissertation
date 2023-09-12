import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils


class PeerDiscoveryHandler:
    # this class will broadcast all the nodes in to the network to exchange information
    def __init__(self, node):
        self.socketCommunication = node
        # Peer discovery will talk with the property of socketCommunication

    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=())
        discoveryThread.start()

    def status(self):
        while True:
            print('Current Connections')
            for peer in self.socketCommunication.peers:
                print(str(peer.ip) + ':' + str(peer.port))
            time.sleep(5)

    def discovery(self):
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            print('discovery working')
            time.sleep(10)

    def handshake(self, connected_node):
        # handshake exchange of information between nodes is more or less just the nodes which they know on their own
        # we have to find  a way on how to exchange these informations and these nodes amongst the new connected nodes
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connected_node, handshakeMessage)

    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data = ownPeers
        messageType = 'DISCOVERY'
        message = Message(ownConnector, messageType, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage

    # this method is used to connect with other nodes in the peer list
    def handleMessage(self, message):
        peersSocketConnector = message.senderConnector
        peersPeerList = message.data
        newPeer = True
        for peer in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False
        if newPeer:
            self.socketCommunication.peers.append(peersSocketConnector)
        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True
            if not peerKnown and not peersPeer.equals(self.socketCommunication.socketConnector):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)
