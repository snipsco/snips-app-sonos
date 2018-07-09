from snipssonos.services.state.persistence import StatePersistence

import copy
import logging


class HermesStatePersistence(StatePersistence):
    SERVICE_NAME = "HERMES_STATE_PERSISTENCE"

    def __init__(self, layer):
        super(HermesStatePersistence, self).__init__(layer)

    def save(self, state):
        state_ = copy.deepcopy(state)
        logging.debug("state={}".format(state_))
        self.layer.update(state_)

    def get_all(self, entity_cls):
        entities = list()
        for key, _entities in self.layer.iteritems():
            entities.extend(_entities.values())

        return filter(lambda potential_entity: isinstance(potential_entity, entity_cls), entities)

    def get(self, entity_cls):
        return self.get_all(entity_cls)[0]

    def clear(self):
        self.layer = dict()
