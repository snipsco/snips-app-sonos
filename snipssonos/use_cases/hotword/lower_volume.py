from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException
from snipssonos.use_cases.request_objects import VolumeSetRequestObject
from snipssonos.use_cases.volume.set import VolumeSetUseCase


class HotwordLowerVolumeUseCase(UseCase):
    DEFAULT_LOW_VOLUME = 8

    def __init__(self, device_discovery_service, device_transport_control_service, state_persistence_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service
        self.state_persistence_service = state_persistence_service

    def process_request(self, request_object):
        devices = self.device_discovery_service.get_devices()

        states = dict()
        states['devices'] = {device.identifier: device for device in devices}

        self.state_persistence_service.save(states)

        min_device_volume = min([device.volume for device in devices])
        volume_set_use_case = VolumeSetUseCase(self.device_discovery_service, self.device_transport_control_service)
        volume_set_request_object = VolumeSetRequestObject(min(self.DEFAULT_LOW_VOLUME, min_device_volume))

        response = volume_set_use_case.execute(volume_set_request_object)

        return ResponseSuccess() if response else response
