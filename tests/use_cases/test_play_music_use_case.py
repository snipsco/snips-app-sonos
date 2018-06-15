import pytest
from mock import mock

from snipssonos.entities.device import Device

from snipssonos.use_cases.play_music import PlayMusicUseCase
from snipssonos.use_cases.play_track import PlayTrackUseCase
from snipssonos.use_cases.play_artist import PlayArtistUseCase

from snipssonos.use_cases.request_objects import PlayMusicRequestObject
from snipssonos.use_cases.request_objects import PlayArtistRequestObject
from snipssonos.use_cases.request_objects import PlayTrackRequestObject

from snipssonos.exceptions import NoReachableDeviceException


@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )

@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_empty_parameters(connected_device):
    device_disco_service = None
    music_playback_service = None
    music_search_service = None

    play_artist_uc = PlayArtistUseCase(device_disco_service, music_search_service, music_playback_service)

    play_artist_request = PlayArtistRequestObject.from_dict({})

    result_object = play_artist_uc.execute(play_artist_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.volume_up.assert_called()

    device_transport_control_service.volume_up.assert_called_with(connected_device)

    assert bool(result_object) is True
    assert connected_device.volume == initial_volume + VolumeUpUseCase.DEFAULT_VOLUME_INCREMENT


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject()
    result_obj = volume_up_uc.execute(volume_up_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_wrong_parameter():
    volume_level_is_a_string = "duh"

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({'volume_increase': volume_level_is_a_string})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_parameter_out_of_range(connected_device):
    volume_increase_in_percentage = 123456789

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({'volume_increase': volume_increase_in_percentage})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10

@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_positive_percentage(connected_device):
    volume_increase_in_percentage = 10
    initial_volume = connected_device.volume

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({'volume_increase': volume_increase_in_percentage})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is True
    device_transport_control_service.volume_up.assert_called_with(connected_device)
    assert connected_device.volume == initial_volume + volume_increase_in_percentage

@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_negative_percentage(connected_device):
    volume_increase_in_percentage = -10

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({'volume_increase': volume_increase_in_percentage})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10

@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_positive_integer(connected_device):
    volume_increase_integer = 10
    initial_volume = connected_device.volume

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({'volume_increase': volume_increase_integer})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is True
    device_transport_control_service.volume_up.assert_called_with(connected_device)
    assert connected_device.volume == initial_volume + volume_increase_integer

@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_negative_integer(connected_device):
    volume_increase_integer = -10

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({'volume_increase': volume_increase_integer})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10

@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_maximum_volume(connected_device):
    volume_increase_integer = 91

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({'volume_increase': volume_increase_integer})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is True
    assert connected_device.volume == 100
