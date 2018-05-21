import json

class Device(object):
    def __init__(self, identifier, name):
        self.name = name
        self.id = identifier