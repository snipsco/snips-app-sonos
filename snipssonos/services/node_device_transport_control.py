import requests

from snipssonos.services.device_transport_control import DeviceTransportControlService

class NodeDeviceTransportControlService(DeviceTransportControlService):

    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def volume_up(self, device, volume_increment):
        room_name = device.name

        query_url = self.generate_volume_up_query(room_name, volume_increment)

        req = requests.get(query_url)
        if req.ok:
            return True
        return False

    def generate_volume_up_query(self, room_name, volume_increment):
        return "{}{}:{}/{}/volume/{}".format(self.PROTOCOL, self.HOST, self.PORT, room_name, volume_increment)

