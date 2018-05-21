from device_discovery import DeviceDiscoveryService
from device_discovery import Device
from snipssonos.adapters.sonos_node_api_client import SonosNodeAPIClient


class NodeDevice(Device):
    def __init__(self, identifier, name):
        super(NodeDevice, self).__init__(identifier, name)

class NodeDeviceDiscoveryService(DeviceDiscoveryService, SonosNodeAPIClient):

    def get_zones(self):
        return self.query(self.build_action_request("zones"))


    def get_device(self):
        devices = self.get_devices()
        if len(devices) > 0:
            return devices[0]
        else:
            return None

    def get_devices(self):
        zones = self.get_zones()
        return map(lambda zone: NodeDevice(zone.get("uuid"), zone.get("coordinator").get("roomName")), zones)

