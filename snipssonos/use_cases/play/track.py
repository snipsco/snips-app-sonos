from snipssonos.services.node.query_builder import NodeQueryBuilder

from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure


class PlayTrackUseCase(UseCase):

    def __init__(self, device_discovery_service, music_search_service, music_playback_service, feedback_service):
        self.device_discovery_service = device_discovery_service
        self.music_search_service = music_search_service
        self.music_playback_service = music_playback_service
        self.feedback_service = feedback_service

    def process_request(self, request_object):

        device = self.device_discovery_service.get()

        track_name = request_object.track_name if request_object.track_name else None
        artist_name = request_object.artist_name if request_object.artist_name else None
        album_name = request_object.album_name if request_object.album_name else None
        playlist_name = request_object.playlist_name if request_object.playlist_name else None

        results_tracks = list()

        if track_name and album_name and artist_name and playlist_name:  # Track - Album - Artist - Playlist
            results_tracks = self.music_search_service.search_track_for_album_and_for_artist_and_for_playlist(
                track_name, album_name, artist_name, playlist_name)

        if track_name and album_name and artist_name:  # Track - Album - Artist
            results_tracks = self.music_search_service.search_track_for_album_and_for_artist

        if track_name and album_name and playlist_name:  # Track - Album - Playlist
            results_tracks = self.music_search_service.search_track_for_album_and_for_playlist

        if track_name and artist_name and playlist_name:  # Track - Artist - Playlist
            results_tracks = self.music_search_service.search_track_for_artist_and_for_playlist

        if track_name and playlist_name:  # Track - Playlist
            results_tracks = self.music_search_service.search_track_for_playlist()

        if track_name and artist_name:  # Track - Artist
            results_tracks = self.music_search_service.search_track_for_artist

        if track_name and album_name:  # Track - Album
            results_tracks = self.music_search_service.search_track_for_album

        # Track
        if track_name and not (artist_name or playlist_name or album_name):
            results_tracks = self.music_search_service.search_track(request_object.track_name)

        if len(results_tracks):
            first_result = results_tracks[0]
            self.music_playback_service.clear_queue(device)
            self.music_playback_service.play(device, first_result)
            artist_names = self.feedback_service.concatenate_artists_in_string(first_result.artists)
            tts_feedback = self.feedback_service.get_track_template()\
                .format(first_result.name, artist_names)
            return ResponseSuccess(feedback=tts_feedback)

        return ResponseFailure.build_resource_error(self.feedback_service.get_generic_error_message())