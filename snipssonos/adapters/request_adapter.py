from snipssonos.use_cases.request_objects import VolumeUpRequestObject, PlayTrackRequestObject, PlayArtistRequestObject

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
        if len(intentMessage.slots.song_name_FR):
            return {'track_name': intentMessage.slots.song_name_FR.first().value }
        else:
            return dict()

class PlayArtistRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return PlayArtistRequestObject.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        slots_dict = dict()

        if len(intentMessage.slots.song_name_FR):
            slots_dict.update({'track_name': intentMessage.slots.song_name_FR.first().value })

        if len(intentMessage.slots.artist_name_FR):
            slots_dict.update({'artist_name': intentMessage.slots.artist_name_FR.first().value})

        return slots_dict