
import json
import jsonpickle
# transform our objects into a word structure


class BlockchainUtils:
    @staticmethod
    def encode(objectToEncode):
        return jsonpickle.encode(objectToEncode,unpicklable=True)


    @staticmethod
    def decode(encodedObject):
        return jsonpickle.decode(encodedObject)