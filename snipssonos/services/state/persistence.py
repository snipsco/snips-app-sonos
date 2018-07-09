from snipssonos.services.service import Service


class StatePersistence(Service):
    SERVICE_NAME = "STATE_PERSISTENCE"

    def __init__(self, layer):
        self.layer = layer

    def save(self, state):
        raise NotImplementedError("save() method not implemented")

    def get_all(self, entity_cls):
        raise NotImplementedError("get_all() method not implemented")

    def get(self, entity_cls):
        raise NotImplementedError("get() method not implemented")
