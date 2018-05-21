import json
import requests

from snipssonos.exceptions import APIRequestWrongParams, APIRequestError
from snipssonos.shared import request_object as request


PROTOCOL = "http"
HOST = "localhost"
PORT = 5005

class SonosNodeAPIClient(object):
    def __init__(self):
        self.device = None

    def for_device(self, device):
        self.device = device

    def build_action_request(self, action):  # TODO, write tests
        if action and isinstance(action, str) and len(action):
            return "{}://{}:{}/{}".format(PROTOCOL, HOST, PORT, action)
        else:
            raise APIRequestWrongParams("Wrong parameters used in the request to the Node Sonos API")

    def build_device_request(self, device, action, *args):
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

    def execute(self, device, action):
        r_str = self.build_device_request(device, action)

        r = requests.get(r_str)
        if (r.status_code != requests.codes.ok):
            return False
        tmp = json.loads(r.text)
        if (tmp['status'] != 'success'):
            return False
        return True

    def query(self, req):
        req_result = requests.get(req)
        if (req_result.status_code == requests.codes.ok):
            return json.loads(req_result.text)
        else:
            raise APIRequestError("Error while requesting the Node HTTP API ...")
