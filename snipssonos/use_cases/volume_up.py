from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException

class VolumeUpUseCase(object):
    DEFAULT_VOLUME_INCREMENT = 10
    def __init__(self, device_discovery_service, device_transport_control_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service


    def execute(self, request):
        if bool(request):
            try:
                device = self.device_discovery_service.get()
                if request.volume_increase:
                    self.device_transport_control_service.volume_up(device, request.volume_increase)
                    device.volume = device.volume + request.volume_increase
                else:
                    device.volume = device.volume + self.DEFAULT_VOLUME_INCREMENT
                    self.device_transport_control_service.volume_up(device, request.volume_increase)
                return ResponseSuccess()

            except NoReachableDeviceException as e:
                return ResponseFailure.build_resource_error(e)
        else:
            return ResponseFailure.build_from_invalid_request_object(request)