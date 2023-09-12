from Node import Node
import sys
from Node import Node

if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])
    node = Node(ip, port)
    node.startP2P()#
    print("spi starting")
    node.startAPI(apiPort)
