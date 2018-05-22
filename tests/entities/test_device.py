from snipssonos.entities.entities import Entity
from snipssonos.entities import device as d

def test_device_model_initialization():
    identifier = "RINCON_XXXXXX"
    name = "Antho's Sonos"

    device = d.Device(identifier, name)

    assert device.name == name
    assert device.identifier == identifier

def test_device_model_initialization_with_dict():
    identifier = "RINCON_XXXXXX"
    name = "Antho's Sonos"

    device = d.Device.from_dict(
        {
            'identifier' : identifier,
            'name' : name,
        }
    )

    assert device.name == name
    assert device.identifier == identifier


def test_device_is_entity():
    identifier = "RINCON_XXXXXX"
    name = "Antho's Sonos"

    device = d.Device(identifier, name)
    assert isinstance(device, Entity)

