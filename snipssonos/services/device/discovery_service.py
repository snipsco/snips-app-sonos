from snipssonos.services.service import Service


class DeviceDiscoveryService(Service):
    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def __init__(self, device=None):
        self.device = device

        self.PORT = self.CONFIGURATION['global']['music_service_port'] if (
            self.CONFIGURATION['global']['music_service_port']) else self.PORT

        self.HOST = self.CONFIGURATION['global']['music_service_hostname'] if (
            self.CONFIGURATION['global']['music_service_hostname']) else self.HOST

    def get(self):
        raise NotImplementedError("get() is not implemented")

    def get_devices(self):
        raise NotImplementedError("get_devices() is not implemented")
