from snipssonos.entities.entities import Entity
from snipssonos.entities import device as d

def test_device_model_initialization():
    identifier = "RINCON_XXXXXX"
    name = "Antho's Sonos"
    volume = 10

    device = d.Device(identifier, name, volume)

    assert device.name == name
    assert device.identifier == identifier
    assert device.volume == volume

def test_device_model_initialization_with_dict():
    identifier = "RINCON_XXXXXX"
    name = "Antho's Sonos"
    volume = 20

    device = d.Device.from_dict(
        {
            'identifier' : identifier,
            'name' : name,
            'volume': volume,
        }
    )

    assert device.name == name
    assert device.identifier == identifier
    assert device.volume == volume


def test_device_is_entity():
    identifier = "RINCON_XXXXXX"
    name = "Antho's Sonos"
    volume = 10

    device = d.Device(identifier, name, volume)
    assert isinstance(device, Entity)

