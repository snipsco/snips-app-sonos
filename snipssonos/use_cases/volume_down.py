from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException

class VolumeDownUseCase(UseCase):
    DEFAULT_VOLUME_DECREMENT = 10

    def __init__(self, device_discovery_service, device_transport_control_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service


    def process_request(self, request_object):
        device = self.device_discovery_service.get()
        volume_decrease = request_object.volume_decrease
        if volume_decrease:
            device.decrease_volume(volume_decrease)
            self.device_transport_control_service.volume_down(device)
        else:
            device.decrease_volume(self.DEFAULT_VOLUME_DECREMENT)
            self.device_transport_control_service.volume_down(device)
        return ResponseSuccess()
