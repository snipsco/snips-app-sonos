from .provider_player_template import A_ProviderPlayerTemplate
from soco.music_services import MusicService
import soco
import random
import requests
from soco.data_structures import DidlItem, DidlResource
from soco.compat import quote_url
import socket
from .spotify import SpotifyClient
from os.path import expanduser
import json
import subprocess
import socket

class NodePlayer(A_ProviderPlayerTemplate):

    @staticmethod
    def check_server(host, port):
        s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0

    def __init__(self, node_server="0.0.0.0", service_name=None):
        if (service_name is None):
            node_server = None
            return
        self.service_name = service_name
        self.node_server = node_server
        if (not NodePlayer.check_server(node_server, 5005)):
            if not (node_server == '0.0.0.0' or node_server == 'localhost'
                    or node_server == '127.0.0.1'
                    or node_server == socket.gethostname()):
                node_server = None
                return
            dir = expanduser("~") + '/node-sonos-http-api/'
            if (not os.path.isdir(dir)):
                node_server = None
                return
            p = subprocess.Popen(['npm', 'install', '--production'], cwd=dir)
            p.wait()
            p = subprocess.Popen(['npm', 'start'], cwd=dir, stdout=FNULL, stderr=subprocess.STDOUT)
            time.sleep(3)

    def play(self, device, name, shuffle=False, request=None):
        if (self.node_server is None):
            return False
        player_name = device.player_name
        name = name.replace(" ", "+")
        print(name)
        r_str ='http://%s:5005/%s/musicsearch/%s/%s/%s'\
                % (self.node_server, player_name,
                   self.service_name, request, name)
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
