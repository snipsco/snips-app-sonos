from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject

class VolumeUpRequestObject(ValidRequestObject):
    def __init__(self,  volume_increase=None):
        self.volume_increase = volume_increase

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if 'volume_increase' in a_dictionary and not isinstance(a_dictionary['volume_increase'], int):
            invalid_request.add_error('volume_increase', 'must be an integer')

        if 'volume_increase' in a_dictionary and isinstance(a_dictionary['volume_increase'], int) and a_dictionary['volume_increase'] < 0:
            invalid_request.add_error('volume_increase', 'must be positive')

        if 'volume_increase' in a_dictionary and isinstance(a_dictionary['volume_increase'], int) and a_dictionary['volume_increase'] > 100:
            invalid_request.add_error('volume_increase', 'must be lower than 100')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            volume_increase=a_dictionary.get('volume_increase', None)
        )


class VolumeDownRequestObject(ValidRequestObject):
    def __init__(self,  volume_decrease=None):
        self.volume_decrease = volume_decrease

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if 'volume_decrease' in a_dictionary and not isinstance(a_dictionary['volume_decrease'], int):
            invalid_request.add_error('volume_decrease', 'must be an integer')

        if 'volume_decrease' in a_dictionary and isinstance(a_dictionary['volume_decrease'], int) and a_dictionary['volume_decrease'] < 0:
            invalid_request.add_error('volume_decrease', 'must be positive')

        if 'volume_decrease' in a_dictionary and isinstance(a_dictionary['volume_decrease'], int) and a_dictionary['volume_decrease'] > 100:
            invalid_request.add_error('volume_decrease', 'must be lower than 100')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            volume_decrease=a_dictionary.get('volume_decrease', None)
        )


class VolumeSetRequestObject(ValidRequestObject):
    def __init__(self,  volume_level=None):
        self.volume_level = volume_level

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if not('volume_level' in a_dictionary):
            invalid_request.add_error('volume_level', 'is missing')

        if 'volume_level' in a_dictionary and not isinstance(a_dictionary['volume_level'], int):
            invalid_request.add_error('volume_level', 'must be an integer')

        if 'volume_level' in a_dictionary and isinstance(a_dictionary['volume_level'], int) and a_dictionary['volume_level'] < 0:
            invalid_request.add_error('volume_level', 'must be positive')

        if 'volume_level' in a_dictionary and isinstance(a_dictionary['volume_level'], int) and a_dictionary['volume_level'] > 100:
            invalid_request.add_error('volume_level', 'must be lower than 100')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            volume_level=a_dictionary.get('volume_level', None)
        )


class MuteRequestObject(ValidRequestObject):

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if invalid_request.has_errors():
            return invalid_request

        return cls()


class ResumeMusicRequestObject(ValidRequestObject):

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if invalid_request.has_errors():
            return invalid_request

        return cls()


class SpeakerInterruptRequestObject(ValidRequestObject):

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if invalid_request.has_errors():
            return invalid_request
        return cls()


class PlayTrackRequestObject(ValidRequestObject):
    def __init__(self, track_name, artist_name=None, album_name=None, playlist_name=None):
        self.track_name = track_name
        self.artist_name = artist_name
        self.album_name = album_name
        self.playlist_name = playlist_name


    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if not('track_name' in a_dictionary):
            invalid_request.add_error('track_name','is missing')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            track_name=a_dictionary.get('track_name', None),
            artist_name=a_dictionary.get('artist_name', None),
            album_name=a_dictionary.get('album_name', None),
            playlist_name=a_dictionary.get('playlist_name', None),
        )


class PlayArtistRequestObject(ValidRequestObject):
    def __init__(self, artist_name, playlist_name=None):
        self.artist_name = artist_name
        self.playlist_name = playlist_name

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if not('artist_name' in a_dictionary):
            invalid_request.add_error('artist_name','is missing')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            artist_name=a_dictionary.get('artist_name', None),
            playlist_name=a_dictionary.get('playlist_name', None)
        )


class PlayPlaylistRequestObject(ValidRequestObject):
    def __init__(self, playlist_name):
        self.playlist_name = playlist_name

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if not('playlist_name' in a_dictionary):
            invalid_request.add_error('playlist_name','is missing')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            playlist_name=a_dictionary.get('playlist_name', None)
        )


class PlayAlbumRequestObject(ValidRequestObject):
    def __init__(self, album_name, artist_name=None, playlist_name=None):
        self.album_name = album_name
        self.artist_name = artist_name
        self.playlist_name = playlist_name

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if not('album_name' in a_dictionary):
            invalid_request.add_error('album_name','is missing')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            album_name=a_dictionary.get('album_name', None),
            artist_name=a_dictionary.get('artist_name', None),
            playlist_name=a_dictionary.get('playlist_name', None)
        )


class PlayMusicRequestObject(ValidRequestObject):
    def __init__(self, track_name=None, artist_name=None, album_name=None, playlist_name=None):
        self.track_name = track_name
        self.artist_name = artist_name
        self.album_name = album_name
        self.playlist_name = playlist_name


    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            track_name=a_dictionary.get('track_name', None),
            artist_name=a_dictionary.get('artist_name', None),
            album_name=a_dictionary.get('album_name', None),
            playlist_name=a_dictionary.get('playlist_name', None),
        )