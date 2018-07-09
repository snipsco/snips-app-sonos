from snipssonos.entities.device import Device
from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException
from snipssonos.use_cases.request_objects import VolumeSetRequestObject
from snipssonos.use_cases.volume.set import VolumeSetUseCase


class HotwordRestoreVolumeUseCase(UseCase):

    def __init__(self, device_discovery_service, device_transport_control_service, state_persistence_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service
        self.state_persistence_service = state_persistence_service

    def process_request(self, request_object):
        devices = self.state_persistence_service.get_all(Device)
        if len(devices):
            FIRST_DEVICE_VOLUME = devices[0].volume

            volume_set_request_object = VolumeSetRequestObject(FIRST_DEVICE_VOLUME)
            volume_set_use_case = VolumeSetUseCase(self.device_discovery_service, self.device_transport_control_service)

            response = volume_set_use_case.execute(volume_set_request_object)

            self.state_persistence_service.clear() # We clear the state.

            return ResponseSuccess() if response else response
        else:
            return ResponseFailure.build_resource_error("Could not retrieve devices in the state ") # TODO : Change me.
