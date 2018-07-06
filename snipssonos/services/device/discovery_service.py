from snipssonos.services.service import ConfigurableHTTPService


class DeviceDiscoveryService(ConfigurableHTTPService):
    def __init__(self, CONFIGURATION=None, device=None):
        super(DeviceDiscoveryService, self).__init__(CONFIGURATION)
        self.device = device

    def get(self):
        raise NotImplementedError("get() is not implemented")

    def get_devices(self):
        raise NotImplementedError("get_devices() is not implemented")
