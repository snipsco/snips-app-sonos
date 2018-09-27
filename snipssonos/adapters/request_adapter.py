from snipssonos.use_cases.request_objects import VolumeUpRequestFactory, PlayTrackRequestFactory, \
    PlayArtistRequestFactory, \
    VolumeSetRequestFactory, VolumeDownRequestFactory, ResumeMusicRequestFactory, SpeakerInterruptRequestFactory, \
    MuteRequestFactory, PlayPlaylistRequestFactory, PlayAlbumRequestFactory, PlayMusicRequestFactory, \
    NextTrackRequestFactory, PreviousTrackRequestFactory, GetTrackInfoRequestFactory


class VolumeUpRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return VolumeUpRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        return dict()


class VolumeDownRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return VolumeDownRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        return dict()


class VolumeSetRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return VolumeSetRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        if len(intentMessage.slots.volume_set_percentage):
            return {'volume_level': int(intentMessage.slots.volume_set_percentage.first().value.split("%")[0])}
        elif len(intentMessage.slots.volume_set_absolute):
            return {'volume_level': int(intentMessage.slots.volume_set_absolute.first().value)}
        else:
            return dict()


class NextTrackRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return NextTrackRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        return dict()


class PreviousTrackRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return PreviousTrackRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        return dict()


class GetTrackInfoRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return GetTrackInfoRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        return dict()


class MuteRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return MuteRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        return dict()


class ResumeMusicRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return ResumeMusicRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        return dict()


class SpeakerInterruptRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return SpeakerInterruptRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        return dict()


class PlayTrackRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return PlayTrackRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        slots_dict = dict()

        if len(intentMessage.slots.song_name):
            slots_dict.update({'track_name': intentMessage.slots.song_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.artist_name):
            slots_dict.update({'artist_name': intentMessage.slots.artist_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.album_name):
            slots_dict.update({'album_name': intentMessage.slots.album_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.playlist_name):
            slots_dict.update({'playlist_name': intentMessage.slots.playlist_name.first().value.decode('utf-8')})

        return slots_dict


class PlayArtistRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return PlayArtistRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        slots_dict = dict()

        if len(intentMessage.slots.playlist_name):
            slots_dict.update({'playlist_name': intentMessage.slots.playlist_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.artist_name):
            slots_dict.update({'artist_name': intentMessage.slots.artist_name.first().value.decode('utf-8')})

        return slots_dict


class PlayPlaylistRequestAdapter(object):

    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return PlayPlaylistRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        slots_dict = dict()

        if len(intentMessage.slots.playlist_name):
            slots_dict.update({'playlist_name': intentMessage.slots.playlist_name.first().value.decode('utf-8')})

        return slots_dict


class PlayAlbumRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return PlayAlbumRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        slots_dict = dict()

        if len(intentMessage.slots.album_name):
            slots_dict.update({'album_name': intentMessage.slots.album_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.artist_name):
            slots_dict.update({'artist_name': intentMessage.slots.artist_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.playlist_name):
            slots_dict.update({'playlist_name': intentMessage.slots.playlist_name.first().value.decode('utf-8')})

        return slots_dict


class PlayMusicRequestAdapter(object):
    @classmethod
    def from_intent_message(cls, intentMessage):
        slots_dict = cls.extract_slots_dictionary(intentMessage)
        return PlayMusicRequestFactory.from_dict(slots_dict)

    @staticmethod
    def extract_slots_dictionary(intentMessage):
        slots_dict = dict()

        if len(intentMessage.slots.album_name):
            slots_dict.update({'album_name': intentMessage.slots.album_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.artist_name):
            slots_dict.update({'artist_name': intentMessage.slots.artist_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.playlist_name):
            slots_dict.update({'playlist_name': intentMessage.slots.playlist_name.first().value.decode('utf-8')})

        if len(intentMessage.slots.song_name):
            slots_dict.update({'track_name': intentMessage.slots.song_name.first().value.decode('utf-8')})

        return slots_dict
