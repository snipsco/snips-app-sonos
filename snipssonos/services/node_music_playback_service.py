import requests

from snipssonos.services.music_playback_service import MusicPlaybackService

class NodeMusicPlaybackService(MusicPlaybackService): # TODO : Refactor this in next iteration ...

    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def play(self, music_item):

        query_url = self._generate_play_now_query(music_item)
        req = requests.get(query_url)

        if req.ok:
            return True


    def _generate_play_now_query(self, music_item):
        room_name = self.device.name
        uri = music_item.uri
        return "{}{}:{}/{}/spotify/now/{}".format(self.PROTOCOL, self.HOST, self.PORT, room_name, uri)




