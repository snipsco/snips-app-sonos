import pytest

from snipssonos.entities.device import Device
from snipssonos.services.hermes.state_persistence import HermesStatePersistence


@pytest.fixture
def connected_device():
    return Device.from_dict({
        'identifier': 'RINCON_7828CA10127001400',
        'name': 'Antho Room',
        'volume': 18
    })


@pytest.fixture
def configuration():
    return {
        'global': {
            'node_device_discovery_port': 5005,
            'node_device_discovery_host': 'localhost'
        }
    }


@pytest.mark.skip("schnek")
def test_service_initialization():
    service = HermesStatePersistence(dict())
    assert isinstance(service.layer, dict)


def test_service_persists(connected_device):
    service = HermesStatePersistence(dict())

    states = {'devices': {connected_device.identifier: connected_device}}

    service.save(states)

    assert len(service.layer.get('devices').values()) == 1
    assert len(service.get_all(Device)) == 1
    assert service.get(Device).name == connected_device.name


def test_service_persistence_for_empty_object():
    service = HermesStatePersistence(dict())

    states = {}

    service.save(states)
    assert len(service.get_all(Device)) == 0


def test_retrieve_multiple_entities(connected_device):
    service = HermesStatePersistence(dict())

    states = {'devices': {
        connected_device.identifier: connected_device,
        connected_device.name: connected_device
    },
        'test_entities': {}}

    service.save(states)

    assert 2 == len(service.get_all(Device))


def test_retrieve_single_entity(connected_device):
    service = HermesStatePersistence(dict())

    states = {'devices': {connected_device.identifier: connected_device},
              'test_entities': {}}

    service.save(states)

    assert service.get(Device).name == connected_device.name
