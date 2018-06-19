class SonosActionException(Exception):
    """An exception occured with the Sonos Action."""


class ServiceException(SonosActionException):
    """An exception occured within a service"""

# Request Objects
class RequestObjectException(SonosActionException):
    """An exception occured with a request object"""


class RequestObjectInitializationException(RequestObjectException):
    """An exception occured with a request object"""
    def __init__(self, invalid_request_object):
        self.invalid_request_object = invalid_request_object

# Device Discovery Service
class DeviceDiscoveryException(ServiceException):
    """An exceptio occured with the device discovery service"""


class DeviceParsingException(DeviceDiscoveryException):
    """An error occured while trying to parse a device"""


class NoReachableDeviceException(DeviceDiscoveryException):
    """No connected devices were found by the DeviceDiscovery service"""


# Music Search Service
class MusicSearchService(ServiceException):
    """An error occured within the Music Search Service"""


class MusicSearchCredentialsError(MusicSearchService):
    """An error occured with the credentials given to the Music Search Service"""


class MusicSearchProviderConnectionError(MusicSearchService):
    """A connection error occured with the provider of the Music Search Service"""


class APIRequestError(Exception):
    """An exception occured when interacting with Sonos API."""


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
