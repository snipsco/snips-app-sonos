import json
import requests

PROTOCOL = "http"
HOST = "localhost"
PORT = 5005

from exceptions import APIRequestWrongParams


class SnipsSonosClient:
    def __init__(self):
        pass

    def build_request(self, device, action, *args):
        """
        Builds a request for the Sonos API.

        :param device: an identifier for the Sonos speaker. For instance : Living Room
        :param action: an action string
        :params args : optional string parameters
        :return: a valid API route
        """
        if device is None or (len(device) == 0):
            raise APIRequestWrongParams("Missing 'device' parameter in the request to the Sonos API")

        if action is None or (len(action) == 0):
            raise APIRequestWrongParams("Missing 'action' parameter in the request to the Sonos API")

        if len(args):
            filtered_args = filter(lambda arg: arg is not None and len(arg), args)
            if len(filtered_args):
                optional_args_request = reduce(lambda a, arg: a + "/" + arg + "/", filtered_args)
                return "{}://{}:{}/{}/{}/{}".format(PROTOCOL, HOST, str(PORT), device, action, optional_args_request)
            else:
                raise APIRequestWrongParams("Wrong optional parameters in the request to the Sonos API")

        return "{}://{}:{}/{}/{}".format(PROTOCOL, HOST, str(PORT), device, action)

    def command(self, device, action):
        r_str = self.build_request(device, action)

        r = requests.get(r_str)
        if (r.status_code != requests.codes.ok):
            return False
        tmp = json.loads(r.text)
        if (tmp['status'] != 'success'):
            return False
        return True

    def pause(self, device):
        return self.command(device, "pause")

    def next_track(self, device):
        return self.command(device, "next")

    def previous(self, device):
        return self.command(device, "previous")

    def play(self, device):
        return self.command(device, "play")

    def volume_down(self, device, level):
        return self.command(device, "volume/-%d" % level)

    def volume_up(self, device, level):
        return self.command(device, "volume/+%d" % level)

    def set_volume(self, device, level):
        return self.command(device, "volume/%d" % level)
