from snipssonos.entities.device import Device
from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException


class VolumeSetUseCase(UseCase):
    def __init__(self, device_discovery_service, device_transport_control_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service

    def process_request(self, request_object):
        devices = self.device_discovery_service.get_devices()

        if request_object.volume_level:
            for device in devices:
                device.volume = request_object.volume_level
                self.device_transport_control_service.set_volume(device)

        return ResponseSuccess()
