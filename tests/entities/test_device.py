from snipssonos.entities.entities import Entity
from snipssonos.entities import device as d


def test_device_model_initialization():
    identifier = "RINCON_XXXXXX"
    name = "Antho's Sonos"
    volume = 10
    VOLUME_MAX = 100
    VOLUME_MIN = 0

    device = d.Device(identifier, name, volume)

    assert device.name == name
    assert device.identifier == identifier
    assert device.volume == volume
    assert device.VOLUME_MAX == VOLUME_MAX
    assert device.VOLUME_MIN == VOLUME_MIN


def test_device_model_initialization_with_dict():
    identifier = "RINCON_XXXXXX"
    name = "Antho's Sonos"
    volume = 20

    device = d.Device.from_dict(
        {
            'identifier': identifier,
            'name': name,
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


def test_device_set_volume_within_range():
    identifier = "RINCON_XXXXXXX"
    name = "Sonos device"
    volume = 10

    device = d.Device(identifier, name, volume)

    device.volume = 20

    assert device.volume == 20


def test_device_set_volume_higher_range():
    identifier = "RINCON_XXXXXXX"
    name = "Sonos device"
    volume = 10

    device = d.Device(identifier, name, volume)

    device.volume = 123456789

    assert device.volume == d.Device.VOLUME_MAX


def test_device_set_volume_lower_range():
    identifier = "RINCON_XXXXXXX"
    name = "Sonos device"
    volume = 10

    device = d.Device(identifier, name, volume)

    device.volume = -123456789

    assert device.volume == d.Device.VOLUME_MIN


def test_device_increment_volume_within_range():
    identifier = "RINCON_XXXXXXX"
    name = "Sonos device"
    volume = 10

    device = d.Device(identifier, name, volume)

    increment = 10
    device.increase_volume(increment)

    assert device.volume == 20


def test_device_increment_volume_exceeds_high_range():
    identifier = "RINCON_XXXXXXX"
    name = "Sonos device"
    volume = 92

    device = d.Device(identifier, name, volume)

    increment = 10
    device.increase_volume(increment)

    assert device.volume == d.Device.VOLUME_MAX


def test_device_decrement_volume_within_range():
    identifier = "RINCON_XXXX"
    name = "Sonos Device"
    volume = 50

    device = d.Device(identifier, name, volume)

    decrement = 25

    device.decrease_volume(decrement)

    assert device.volume == 25


def test_device_decrement_volume_exceeds_high_range():
    identifier = "RINCON_XXXXXXX"
    name = "Sonos device"
    volume = 20

    device = d.Device(identifier, name, volume)

    decrement = 100
    device.decrease_volume(decrement)

    assert device.volume == d.Device.VOLUME_MIN
