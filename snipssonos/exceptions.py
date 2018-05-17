class SonosClientException(Exception):
    """An exception occured the Sonos client."""


class APIRequestError(Exception):
    """An exception occured when interacting with Sonos API."""

class APIRequestWrongParams(APIRequestError):
    """The API was called with wrong parameters. """
