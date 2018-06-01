from snipssonos.entities.entities import Entity
from snipssonos.entities.track import Track


def test_track_initialization():
    uri = "uri"

    track = Track(uri)

    assert track.uri == uri


def test_device_model_initialization_with_dict():
    uri = "uri"

    track = Track.from_dict(
        {
            'uri': uri,
        }
    )
    assert track.uri == uri

def test_track_is_entity():
    track = Track("uri")
    assert isinstance(track, Entity)
