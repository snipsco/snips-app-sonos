import pytest
from mock import mock

from snipssonos.entities.device import Device

from snipssonos.use_cases.play_artist import PlayArtistUseCase
from snipssonos.use_cases.request_objects import PlayArtistRequestObject

from snipssonos.exceptions import NoReachableDeviceException


@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )

def test_use_case_empty_parameters(connected_device):
    device_discovery_service = mock.Mock()
    music_search_service = mock.Mock()
    music_playback_service = mock.Mock()

    play_artist_uc = PlayArtistUseCase(device_discovery_service, music_search_service, music_playback_service)

    play_artist_request = PlayArtistRequestObject.from_dict({})
    result_object = play_artist_uc.execute(play_artist_request)

    assert bool(play_artist_request) is False
    assert bool(result_object) is False

@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    music_playback_service = mock.Mock()

    play_artist_uc = PlayArtistUseCase(device_discovery_service, device_transport_control_service,
                                       music_playback_service)

    play_artist_request = PlayArtistRequestObject.from_dict({})
    result_obj = play_artist_uc.execute(play_artist_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"


@pytest.mark.skip(reason="I didn't have time to do proper mocking. Let's wait for next iteration")
def test_use_case_with_wrong_parameter():
    assert True is False


@pytest.mark.skip(reason="I didn't have time to do proper mocking. Let's wait for next iteration")
def test_use_case_with_parameter_out_of_range(connected_device):
    assert True is False


@pytest.mark.skip(reason="I didn't have time to do proper mocking. Let's wait for next iteration")
def test_use_case_with_positive_percentage(connected_device):
    assert True is False


@pytest.mark.skip(reason="I didn't have time to do proper mocking. Let's wait for next iteration")
def test_use_case_with_negative_percentage(connected_device):
    assert True is False


@pytest.mark.skip(reason="I didn't have time to do proper mocking. Let's wait for next iteration")
def test_use_case_with_positive_integer(connected_device):
    assert True is False


@pytest.mark.skip(reason="I didn't have time to do proper mocking. Let's wait for next iteration")
def test_use_case_with_negative_integer(connected_device):
    assert True is False


@pytest.mark.skip(reason="I didn't have time to do proper mocking. Let's wait for next iteration")
def test_use_case_with_maximum_volume(connected_device):
    assert True is False
