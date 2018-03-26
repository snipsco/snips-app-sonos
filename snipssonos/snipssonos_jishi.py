import os
from os.path import expanduser
from provider.node_player import NodePlayer
import requests
import subprocess
import time

class SnipsSonosJishi:
    def __init__(self, node_server="0.0.0.0"):
        self.node_server = node_server
        if (not NodePlayer.check_server(node_server, 5005)):
            if not (node_server == '0.0.0.0' or node_server == 'localhost'
                    or node_server == '127.0.0.1'
                    or node_server == socket.gethostname()):
                self.node_server = None
                return
            dir = expanduser("/home/pi") + '/node-sonos-http-api/'
            if (not os.path.isdir(dir)):
                self.node_server = None
                return
            p = subprocess.Popen(['npm', 'install', '--production'], cwd=dir)
            p.wait()
            FNULL = open(os.devnull, 'w')
            p = subprocess.Popen(['npm', 'start'], cwd=dir, stdout=FNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
    
    def command(self, device, value):
        if (self.node_server is None):
            return False
        player_name = device.player_name
        r_str ='http://%s:5005/%s/%s'\
                % (self.node_server, player_name, value)
        r = requests.get(r_str)
        if (r.status_code != requests.codes.ok):
            return False
        tmp = json.loads(r.text)
        if (tmp['status'] != 'success'):
            return False
        return True

    def pause(self, device):
        return self.command(device, "pause")
    
    def next(self, device):
        return self.command(device, "next")
    
    def previous(self, device):
        return self.command(device, "next")
    
    def play(self, device):
        return self.command(device, "play")

    def volume_down(self, device, level):
        return self.command(device, "volume/-%s" % level)
    
    def volume_up(self, device, level):
        return self.command(device, "volume/+%s" % level)

    def set_volume(self, device, value):
        return self.command(device, "volume/%s" % level)
