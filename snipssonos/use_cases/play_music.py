from snipssonos.shared.use_case import UseCase

from snipssonos.shared.response_object import ResponseFailure

from snipssonos.use_cases.play_track import PlayTrackUseCase
from snipssonos.use_cases.play_artist import PlayArtistUseCase
from snipssonos.use_cases.play_album import PlayAlbumUseCase
from snipssonos.use_cases.play_playlist import PlayPlaylistUseCase

import logging

class PlayMusicUseCase(UseCase):

    def __init__(self,  device_discovery_service, music_search_service, music_playback_service):
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
        if not(track_name) and not(album_name) and not(artist_name) and playlist_name:
            logging.info('playlist')
            return PlayPlaylistUseCase(self.device_discovery_service, self.music_search_service,
                                       self.music_playback_service)

        if not(track_name) and not(album_name) and artist_name and not(playlist_name):
            logging.info('artist')
            return PlayArtistUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if not (track_name) and not (album_name) and artist_name and playlist_name:
            logging.info('artist-playlist')
            return PlayArtistUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if not(track_name) and album_name and not(artist_name) and not(playlist_name):
            logging.info('album')
            return PlayAlbumUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if not(track_name) and album_name and not(artist_name) and playlist_name:
            logging.info('album-playlist')
            return PlayAlbumUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if not(track_name) and album_name and artist_name and not(playlist_name):
            logging.info('album-artist')
            return PlayAlbumUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if not(track_name) and album_name and artist_name and playlist_name:
            logging.info('album-artist-playlist')
            return PlayAlbumUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if track_name and not(album_name) and not(artist_name) and not(playlist_name):
            logging.info('song')
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if track_name and not(album_name) and not(artist_name) and playlist_name:
            logging.info('song-playlist')
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if track_name and not(album_name) and artist_name and not(playlist_name):
            logging.info('song-artist')
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if track_name and not(album_name) and artist_name and playlist_name:
            logging.info('sont-artist-playlist')
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if track_name and album_name and not(artist_name) and not(playlist_name):
            logging.info('song-album')
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if track_name and album_name and not(artist_name) and playlist_name:
            logging.info('song-album-playlist')
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if track_name and album_name and artist_name and not(playlist_name):
            logging.info('song-album-artist')
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        if track_name and album_name and artist_name and playlist_name:
            logging.info('song-album-artist-playlist')
            return PlayTrackUseCase(self.device_discovery_service, self.music_search_service,
                                     self.music_playback_service)

        return PlayMusicInvalidUseCase()

class PlayMusicInvalidUseCase(UseCase):
    def process_request(self, request_object):
        return ResponseFailure.build_resource_error("An error occured")
