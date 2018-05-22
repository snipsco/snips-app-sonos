from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException

class VolumeUpUseCase(object):
    def __init__(self, device_discovery_service, device_transport_control_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service


    def execute(self, request):
        if bool(request):
            try:
                device = self.device_discovery_service.get()
                self.device_transport_control_service.volume_up(device, request.volume_increase_in_percent)
                return ResponseSuccess()

            except NoReachableDeviceException as e:
                return ResponseFailure.build_resource_error(e)
        else:
            return ResponseFailure.build_from_invalid_request_object(request)