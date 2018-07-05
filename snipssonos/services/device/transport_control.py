from snipssonos.services.service import Service


class DeviceTransportControlService(Service):  # TODO : Make this class abstract
    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def __init__(self):
        self.PORT = self.CONFIGURATION['global']['music_service_port'] if (
            self.CONFIGURATION['global']['music_service_port']) else self.PORT

        self.HOST = self.CONFIGURATION['global']['music_service_hostname'] if (
            self.CONFIGURATION['global']['music_service_hostname']) else self.HOST

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
