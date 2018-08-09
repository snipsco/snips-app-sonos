import json

from snipssonos.entities.artist import Artist
from snipssonos.entities.track import Track
from snipssonos.entities.playlist import Playlist
from snipssonos.helpers.deezer_client import DeezerClient, DeezerAPIQueryBuilder


class DeezerCustomizationService:
    ENTITY_NUMBER_LIMIT = 50

    def __init__(self, app_id, secret, access_token):
        self.client = DeezerClient(app_id, secret, access_token)
        self.app_id = app_id
        self.secret = secret

    def fetch_entity(self, entity_type):
        get_top_entities_by_type_query = DeezerAPIQueryBuilder() \
            .set_user_data() \
            .set_entity_type(entity_type)\
            .limit(self.ENTITY_NUMBER_LIMIT)

        data = self.client.execute_query(get_top_entities_by_type_query)
        entities = [self.parse_entity(entity_type, entity_data) for entity_data in data]

        return entities


    @staticmethod
    def parse_entity(entity_type, entity_data):
        response = json.loads(entity_data)

        if entity_type == "artists":
            artists = [Artist(item['id'], item['name']) for item in response['data']]
            return artists

        elif entity_type == "tracks":
            tracks = [Track(item['id'], item['title']) for item in response['data']]
            return tracks

        elif entity_type == "playlists":
            playlists = response['data']
            filtered_playlists = filter(lambda playlist_data: not playlist_data['is_loved_track'], playlists)
            playlists = [Playlist(item['id'], item['title']) for item in filtered_playlists]
            return playlists

        else:
            return None
