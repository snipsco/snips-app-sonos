from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject, RequestObjectFactory
from snipssonos.exceptions import RequestObjectInitializationException


class VolumeUpRequestObject(ValidRequestObject):
    @classmethod
    def from_dict(cls, a_dictionary):
        return cls()


class VolumeUpRequestFactory(RequestObjectFactory):
    request_object_class = VolumeUpRequestObject


class VolumeDownRequestObject(ValidRequestObject):
    @classmethod
    def from_dict(cls, a_dictionary):
        return cls()


class VolumeDownRequestFactory(RequestObjectFactory):
    request_object_class = VolumeDownRequestObject


class NextTrackRequestObject(ValidRequestObject):
    @classmethod
    def from_dict(cls, adict):
        return cls()


class NextTrackRequestFactory(RequestObjectFactory):
    request_object_class = NextTrackRequestObject


class PreviousTrackRequestObject(ValidRequestObject):
    @classmethod
    def from_dict(cls, adict):
        return cls()


class PreviousTrackRequestFactory(RequestObjectFactory):
    request_object_class = PreviousTrackRequestObject


class VolumeSetRequestObject(ValidRequestObject):
    def __init__(self, volume_level):
        self.volume_level = volume_level

    @property
    def volume_level(self):
        return self._volume_level

    @volume_level.setter
    def volume_level(self, volume_level):
        invalid_request = InvalidRequestObject()

        if not isinstance(volume_level, int):
            invalid_request.add_error('volume_level', 'must be an integer')

        if isinstance(volume_level, int) and volume_level < 0:
            invalid_request.add_error('volume_level', 'must be positive')

        if isinstance(volume_level, int) and volume_level > 100:
            invalid_request.add_error('volume_level', 'must be lower than 100')

        if invalid_request.has_errors():
            raise RequestObjectInitializationException(invalid_request)

        self._volume_level = volume_level

    @classmethod
    def from_dict(cls, a_dictionary):
        return cls(
            volume_level=a_dictionary.get('volume_level', None)
        )


class VolumeSetRequestFactory(RequestObjectFactory):
    request_object_class = VolumeSetRequestObject


class MuteRequestObject(ValidRequestObject):

    @classmethod
    def from_dict(cls, a_dictionary):
        return cls()


class MuteRequestFactory(RequestObjectFactory):
    request_object_class = MuteRequestObject


class ResumeMusicRequestObject(ValidRequestObject):

    @classmethod
    def from_dict(cls, a_dictionary):
        return cls()


class ResumeMusicRequestFactory(RequestObjectFactory):
    request_object_class = ResumeMusicRequestObject


class SpeakerInterruptRequestObject(ValidRequestObject):

    @classmethod
    def from_dict(cls, a_dictionary):
        return cls()


class SpeakerInterruptRequestFactory(RequestObjectFactory):
    request_object_class = SpeakerInterruptRequestObject


class PlayTrackRequestObject(ValidRequestObject):
    def __init__(self, track_name, artist_name=None, album_name=None, playlist_name=None):
        self.track_name = track_name
        self.artist_name = artist_name
        self.album_name = album_name
        self.playlist_name = playlist_name

    @property
    def track_name(self):
        return self._track_name

    @track_name.setter
    def track_name(self, track_name):
        invalid_request_object = InvalidRequestObject()

        if isinstance(track_name, str):
            self._track_name = track_name
        else:
            invalid_request_object.add_error('track_name', 'is missing')
            raise RequestObjectInitializationException(invalid_request_object)

    @classmethod
    def from_dict(cls, a_dictionary):

        return cls(
            track_name=a_dictionary.get('track_name', None),
            artist_name=a_dictionary.get('artist_name', None),
            album_name=a_dictionary.get('album_name', None),
            playlist_name=a_dictionary.get('playlist_name', None),
        )


class PlayTrackRequestFactory(RequestObjectFactory):
    request_object_class = PlayTrackRequestObject


class PlayArtistRequestObject(ValidRequestObject):
    def __init__(self, artist_name, playlist_name=None):
        self.artist_name = artist_name
        self.playlist_name = playlist_name

    @property
    def artist_name(self):
        return self._artist_name

    @artist_name.setter
    def artist_name(self, artist_name):
        invalid_request = InvalidRequestObject()

        if isinstance(artist_name, str):
            self._artist_name = artist_name

        else:
            invalid_request.add_error('artist_name', 'is missing')

        if invalid_request.has_errors():
            raise RequestObjectInitializationException(invalid_request)

    @classmethod
    def from_dict(cls, a_dictionary):

        return cls(
            artist_name=a_dictionary.get('artist_name', None),
            playlist_name=a_dictionary.get('playlist_name', None)
        )


class PlayArtistRequestFactory(RequestObjectFactory):
    request_object_class = PlayArtistRequestObject


class PlayPlaylistRequestObject(ValidRequestObject):
    def __init__(self, playlist_name):
        self.playlist_name = playlist_name

    @property
    def playlist_name(self):
        return self._playlist_name

    @playlist_name.setter
    def playlist_name(self, playlist_name):
        invalid_request = InvalidRequestObject()

        if isinstance(playlist_name, str):
            self._playlist_name = playlist_name
        else:
            invalid_request.add_error('playlist_name', 'is missing')

        if invalid_request.has_errors():
            raise RequestObjectInitializationException(invalid_request)

    @classmethod
    def from_dict(cls, a_dictionary):

        return cls(
            playlist_name=a_dictionary.get('playlist_name', None)
        )


class PlayPlaylistRequestFactory(RequestObjectFactory):
    request_object_class = PlayPlaylistRequestObject


class PlayAlbumRequestObject(ValidRequestObject):
    def __init__(self, album_name, artist_name=None, playlist_name=None):
        self.album_name = album_name
        self.artist_name = artist_name
        self.playlist_name = playlist_name

    @property
    def album_name(self):
        return self._album_name

    @album_name.setter
    def album_name(self, album_name):
        invalid_request = InvalidRequestObject()

        if isinstance(album_name, str):
            self._album_name = album_name
        else:
            invalid_request.add_error('album_name', 'is missing')

        if invalid_request.has_errors():
            raise RequestObjectInitializationException(invalid_request)

    @classmethod
    def from_dict(cls, a_dictionary):

        return cls(
            album_name=a_dictionary.get('album_name', None),
            artist_name=a_dictionary.get('artist_name', None),
            playlist_name=a_dictionary.get('playlist_name', None)
        )


class PlayAlbumRequestFactory(RequestObjectFactory):
    request_object_class = PlayAlbumRequestObject


class PlayMusicRequestObject(ValidRequestObject):
    def __init__(self, track_name=None, artist_name=None, album_name=None, playlist_name=None):
        self.track_name = track_name
        self.artist_name = artist_name
        self.album_name = album_name
        self.playlist_name = playlist_name

    @classmethod
    def from_dict(cls, a_dictionary):
        return cls(
            track_name=a_dictionary.get('track_name', None),
            artist_name=a_dictionary.get('artist_name', None),
            album_name=a_dictionary.get('album_name', None),
            playlist_name=a_dictionary.get('playlist_name', None),
        )


class PlayMusicRequestFactory(RequestObjectFactory):
    request_object_class = PlayMusicRequestObject


class InjectEntitiesRequestObject(ValidRequestObject):
    VALID_ENTITY_NAMES = ["artists", "tracks", "playlists"]

    def __init__(self, entity_name, entity_slot_name):
        self.entity_name = entity_name
        self.entity_slot_name = entity_slot_name

    @property
    def entity_name(self):
        return self._entity_name

    @property
    def entity_slot_name(self):
        return self._entity_slot_name

    @entity_name.setter
    def entity_name(self, entity_name):
        invalid_request = InvalidRequestObject()
        if isinstance(entity_name, str):
            if entity_name in self.VALID_ENTITY_NAMES:
                self._entity_name = entity_name
            else:
                invalid_request\
                    .add_error('entity_name', 'has to be a valid entity name {}'
                               .format([entity_name for entity_name in self.VALID_ENTITY_NAMES]))
        else:
            invalid_request.add_error('entity_name', 'has to be a string')

        if invalid_request.has_errors():
            raise RequestObjectInitializationException(invalid_request)

    @entity_slot_name.setter
    def entity_slot_name(self, entity_slot_name):
        invalid_request = InvalidRequestObject()
        # TODO once entity names are set in stone figure validation here
        if isinstance(entity_slot_name, str):
            self._entity_slot_name = entity_slot_name
        else:
            invalid_request.add_error('entity_slot_name', 'has to be a string')
        if invalid_request.has_errors():
            raise RequestObjectInitializationException(invalid_request)

    @classmethod
    def from_dict(cls, a_dictionary):

        return cls(
            entity_name=a_dictionary.get('entity_name', None),
            entity_slot_name=a_dictionary.get('entity_slot_name', None)
        )


class InjectEntitiesRequestFactory(RequestObjectFactory):
    request_object_class = InjectEntitiesRequestObject
