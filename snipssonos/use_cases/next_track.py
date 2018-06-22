from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException

class NextTrackUseCase(UseCase):

    def __init__(self, device_discovery_service, device_transport_control_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service


    def process_request(self, request_object):
        device = self.device_discovery_service.get()
        self.device_transport_control_service.next_track(device)
        return ResponseSuccess()
