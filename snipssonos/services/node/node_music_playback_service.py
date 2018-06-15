import requests
import logging

from snipssonos.services.music.music_playback_service import MusicPlaybackService

class NodeMusicPlaybackService(MusicPlaybackService):  # TODO : Refactor this in next iteration ...

    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def play(self, device, music_item):
        self.device = device if device else self.device
        query_url = self._generate_play_now_query(music_item)
        req = requests.get(query_url)

        if req.ok:
            return True

    def queue(self, device, music_items):
        self.device = device if device else self.device

        results = list()

        for music_item in music_items:
            query_url = self._generate_queue_query(music_item)
            req = requests.get(query_url)
            results.append(req.ok)

        return all(results)


    def _generate_play_now_query(self, music_item):
        room_name = self.device.name
        uri = music_item.uri
        return "{}{}:{}/{}/spotify/now/{}".format(self.PROTOCOL, self.HOST, self.PORT, room_name, uri)

    def _generate_queue_query(self, music_item):
        room_name = self.device.name
        uri = music_item.uri
        return "{}{}:{}/{}/spotify/queue/{}".format(self.PROTOCOL, self.HOST, self.PORT, room_name, uri)
