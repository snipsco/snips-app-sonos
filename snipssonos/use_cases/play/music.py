from snipssonos.shared.use_case import UseCase

from snipssonos.shared.response_object import ResponseFailure

from snipssonos.use_cases.play.track import PlayTrackUseCase
from snipssonos.use_cases.play.artist import PlayArtistUseCase
from snipssonos.use_cases.play.album import PlayAlbumUseCase
from snipssonos.use_cases.play.playlist import PlayPlaylistUseCase

import logging
logger = logging.getLogger(__name__)


class PlayMusicUseCase(UseCase):

    def __init__(self, device_discovery_service, music_search_service, music_playback_service):
        self.device_discovery_service = device_discovery_service
        self.music_search_service = music_search_service
        self.music_playback_service = music_playback_service

    def process_request(self, request_object):

        track_name = request_object.track_name if request_object.track_name else None
        artist_name = request_object.artist_name if request_object.artist_name else None
        album_name = request_object.album_name if request_object.album_name else None
        playlist_name = request_object.playlist_name if request_object.playlist_name else None

        sub_use_case = self.extract_sub_use_case_from_parameters(track_name, artist_name, album_name, playlist_name)
        return sub_use_case.process_request(request_object)

    def extract_sub_use_case_from_parameters(self, track_name, artist_name, album_name, playlist_name):
        if not (track_name) and not (album_name) and not (artist_name) and playlist_name:
            logger.info('Use case selected : Playlist', extra={'playlist': playlist_name})
            return PlayPlaylistUseCase(self.device_discovery_service, self.music_search_service,
                                       self.music_playback_service)

        if not (track_name) and not (album_name) and artist_name and not (playlist_name):
            logger.info('Use case selected : Artist', extra={'artist': artist_name, 'playlist': playlist_name})
            return PlayArtistUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if not (track_name) and not (album_name) and artist_name and playlist_name:
            logger.info('Use case selected : Artist-Playlist', extra={'artist':artist_name, 'playlist': playlist_name})
            return PlayArtistUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if not (track_name) and album_name and not (artist_name) and not (playlist_name):
            logger.info('Use case selected : Album', extra={'album':album_name})
            return PlayAlbumUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if not (track_name) and album_name and not (artist_name) and playlist_name:
            logger.info('Use case selected : Album-Playlist', extra={'album':album_name, 'playlist':playlist_name})
            return PlayAlbumUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if not (track_name) and album_name and artist_name and not (playlist_name):
            logger.info('Use case selected : Album-Artist', extra={'album':album_name, 'artist':artist_name})
            return PlayAlbumUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if not (track_name) and album_name and artist_name and playlist_name:
            logger.info('Use case selected : Album-Artist-Playlist', extra={'album': album_name, 'artist':artist_name, 'playlist':playlist_name})
            return PlayAlbumUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if track_name and not (album_name) and not (artist_name) and not (playlist_name):
            logger.info('Use case selected : Song', extra={'track':track_name})
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if track_name and not (album_name) and not (artist_name) and playlist_name:
            logger.info('Use case selected : Song-Playlist', extra={'track': track_name, 'playlist':playlist_name})
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if track_name and not (album_name) and artist_name and not (playlist_name):
            logger.info('Use case selected : Song-Artist', extra={'track':track_name, 'artist':artist_name})
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if track_name and not (album_name) and artist_name and playlist_name:
            logger.info('song-artist-playlist', extra={'track': track_name, 'artist':artist_name, 'playlist': playlist_name})
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if track_name and album_name and not (artist_name) and not (playlist_name):
            logger.info('Use case selected : Song-Album', extra={'track':track_name, 'album': album_name})
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if track_name and album_name and not (artist_name) and playlist_name:
            logger.info('Use case selected : Song-Album-Playlist', extra={'track':track_name, 'album':album_name, 'playlist':playlist_name})
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if track_name and album_name and artist_name and not (playlist_name):
            logger.info('Use case selected : Song-Album-Artist', extra={'track:':track_name, 'album':album_name, 'artist':artist_name})
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)

        if track_name and album_name and artist_name and playlist_name:
            logger.info('Use case selected : Song-Album-Artist-Playlist', extra={'track':track_name, 'album':album_name, 'artist':artist_name, 'playlist':playlist_name})
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                    self.music_playback_service)
        
        logger.info('Use case selected : InvalidUseCase')
        return PlayMusicInvalidUseCase()


class PlayMusicInvalidUseCase(UseCase):
    def process_request(self, request_object):
        return ResponseFailure.build_resource_error("")
