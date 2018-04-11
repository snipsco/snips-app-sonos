import json
import os
from os.path import expanduser
from provider.node_player import NodePlayer
import requests
import subprocess
import time

class SnipsSonosNode:
    def __init__(self, node_server="0.0.0.0"):
        self.node_server = NodePlayer.start_server(node_server)
    
    def command(self, device, value):
        if (self.node_server is None):
            return False
        player_name = device.player_name
        r_str ='http://%s:5005/%s/%s'\
                % (self.node_server, player_name, value)
        print(r_str)
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
        return self.command(device, "previous")
    
    def play(self, device):
        return self.command(device, "play")

    def volume_down(self, device, level):
        return self.command(device, "volume/-%d" % level)
    
    def volume_up(self, device, level):
        return self.command(device, "volume/+%d" % level)

    def set_volume(self, device, value):
        return self.command(device, "volume/%d" % level)
