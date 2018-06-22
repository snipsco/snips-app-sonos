class SonosActionException(Exception):
    """An exception occurred with the Sonos Action."""


class ServiceException(SonosActionException):
    """An exception occurred within a service"""

# Request Objects
class RequestObjectException(SonosActionException):
    """An exception occurred with a request object"""


class RequestObjectInitializationException(RequestObjectException):
    """An exception occurred with a request object"""
    def __init__(self, invalid_request_object):
        self.invalid_request_object = invalid_request_object

# Device Discovery Service
class DeviceDiscoveryException(ServiceException):
    """An exception occurred with the device discovery service"""


class DeviceParsingException(DeviceDiscoveryException):
    """An error occurred while trying to parse a device"""


class NoReachableDeviceException(DeviceDiscoveryException):
    """No connected devices were found by the DeviceDiscovery service"""


# Music Search Service
class MusicSearchService(ServiceException):
    """An error occurred within the Music Search Service"""


class MusicSearchCredentialsError(MusicSearchService):
    """An error occurred with the credentials given to the Music Search Service"""


class MusicSearchProviderConnectionError(MusicSearchService):
    """A connection error occurred with the provider of the Music Search Service"""


class APIRequestError(Exception):
    """An exception occurred when interacting with Sonos API."""


class APIRequestWrongParams(APIRequestError):
    """The API was called with wrong parameters. """


# Spotify client
class SpotifyClientException(Exception):
    """An error occurred within the Spotify Client """


class SpotifyClientWrongEndpoint(SpotifyClientException):
    """The requested Spotify endpoint does not exist."""


# Spotify query builder
class SpotifyQueryBuilderException(Exception):
    """An error occurred within the Spotify Query Builder"""


class SpotifyQueryBuilderNonExistentTimeRange(SpotifyQueryBuilderException):
    """The time range used does not exist, please use valid time ranges:
    'long_term', 'medium_term', 'short_term'"""


class SpotifyQueryBuilderUserDataQueryNotSet(SpotifyQueryBuilderException):
    """Trying to set fields to request a user data query but the class has not been
    initialized to build this kind of query"""
