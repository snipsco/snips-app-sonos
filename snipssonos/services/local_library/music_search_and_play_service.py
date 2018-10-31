from __future__ import unicode_literals

from snipssonos.entities.playlist import Playlist
from snipssonos.services.node.query_builder import LocalLibraryNodeQueryBuilder
from snipssonos.services.deezer.music_search_and_play_service import DeezerMusicSearchService

class LocalLibraryMusicSearchService(DeezerMusicSearchService):
    """
    This service is able to search and directly play music on the Sonos device. The middleware we are
    using to search and play is the Node Sonos server and  it does not offer a way to play songs coming from
    a local library through an ID. What it does offer is an endpoint to be able to do the search and then
    play the results directly.
    """
    SERVICE_NAME = "localLibrary"
    
    def __init__(self, device_discovery_service):
        self.device_discovery_service = device_discovery_service
        first_device = self.device_discovery_service.get()
        self.query_builder = LocalLibraryNodeQueryBuilder(first_device.name)
    
    def search_playlist(self, playlist_name):
        search_query = self.query_builder.generate_search_playlist_query(playlist_name)
        self.execute_query(search_query)
        return [Playlist("", playlist_name)]
