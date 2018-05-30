from snipssonos.use_cases.request_objects import VolumeUpRequestObject, PlayTrackRequestObject

class VolumeUpRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return VolumeUpRequestObject.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        if len(intentMessage.slots.volume_higher):
            return {'volume_increase': int(intentMessage.slots.volume_higher.first().value)}
        else:
            return dict()

class PlayTrackRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return PlayTrackRequestObject.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        if len(intentMessage.slots.song):
            return {'track_name': intentMessage.slots.song.first().value }
        else:
            return dict()