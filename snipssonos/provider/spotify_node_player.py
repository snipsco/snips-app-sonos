from .provider_player_template import A_ProviderPlayerTemplate
from soco.music_services import MusicService
import soco
import random
import requests
from soco.data_structures import DidlItem, DidlResource
from soco.compat import quote_url
from .spotify import SpotifyClient
from pynpm import NPMPackage
from os.path import expanduser
import json

class SpotifyNodePlayer(A_ProviderPlayerTemplate):

    def __init__(self, node_server="0.0.0.0"):
        self.node_server = node_server
        #home = expanduser("~")
        #pkg = NPMPackage('%s/node-sonos-http-api/package.json' % home)
        #pkg.install()
        #pkg.start(wait = False)

    def play(self, device, name, shuffle=False, request=None):
        player_name = device.player_name
        name = name.replace(" ", "+")
        print(name)
        r_str ='http://%s:5005/%s/musicsearch/spotify/%s/%s'\
                % (self.node_server, player_name, request, name)
        print(r_str)
        r = requests.get(r_str)
        if (r.status_code != requests.codes.ok):
            return False
        tmp = json.loads(r.text)
        if (tmp['status'] != 'success'):
            return False
        return True

    def play_track(self, device, name, shuffle=False):
        return self.play(device, name,shuffle, "song")

    def play_artist(self, device, name, shuffle=False):
        return self.play(device, name,shuffle, "song")

    def play_album(self, device, name, shuffle=False):
        return self.play(device, name,shuffle, "album")

    def play_playlist(self, device, name, shuffle=False):
        return self.play(device, name,shuffle, "playlist")
