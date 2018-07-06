from snipssonos.services.service import ConfigurableHTTPService


class DeviceTransportControlService(ConfigurableHTTPService):  # TODO : Make this class abstract
    NAME = "device_transport_control"

    def __init__(self, CONFIGURATION=None):
        super(DeviceTransportControlService, self).__init__(CONFIGURATION)

    def pause(self, device):
        raise NotImplementedError("pause() is not implemented")

    def resume(self, device):
        raise NotImplementedError("resume() is not implemented")

    def volume_up(self, device):
        raise NotImplementedError("volume_up() is not implemented")

    def volume_down(self, device):
        raise NotImplementedError("volume_down() is not implemented")

    def set_volume(self, device):
        raise NotImplementedError("set_volume() is not implemented")

    def mute(self, device):
        raise NotImplementedError("mute() is not implemented")

    def next_track(self, device):
        raise NotImplementedError("next_track() is not implemented")

    def previous_track(self, device):
        raise NotImplementedError("previous_track() is not implemented")
