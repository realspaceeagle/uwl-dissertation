from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockchainUtils import BlockchainUtils
from app import app

node = None


class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, port):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='localhost', port=port)
        print("Nodeapi started")

    def injectNode(self, injectedNode):
        global node
        node = injectedNode
