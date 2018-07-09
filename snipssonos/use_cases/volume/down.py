from snipssonos.entities.device import Device
from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess


class VolumeDownUseCase(UseCase):
    DEFAULT_VOLUME_DECREMENT = 10

    def __init__(self, device_discovery_service, device_transport_control_service, state_persistence_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service
        self.state_persistence_service = state_persistence_service

    def process_request(self, request_object):
        # We first check if the volume was lowered during hotword detection
        if self.has_devices_persisted():
            devices = self.state_persistence_service.get_all(Device)
        else:
            devices = self.device_discovery_service.get_devices()

        for device in devices:
            device.decrease_volume(self.DEFAULT_VOLUME_DECREMENT)
            self.device_transport_control_service.volume_down(device)

        return ResponseSuccess()

    def has_devices_persisted(self):
        return True if len(self.state_persistence_service.get_all(Device)) > 0 else False
