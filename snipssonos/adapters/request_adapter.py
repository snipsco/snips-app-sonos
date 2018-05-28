from snipssonos.use_cases.request_objects import VolumeUpRequestObject

class VolumeUpRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return VolumeUpRequestObject.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        if len(intentMessage.slots.volume_increase):
            return {'volume_increase': intentMessage.slots.volume_increase.first().value}
        else:
            return dict()