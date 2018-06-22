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


# Entities injection service
class EntityInjectionService(ServiceException):
    """An error occurred within the Entity Injection Service"""


# Entities injection service
class InvalidEntitySlotName(EntityInjectionService):
    """An unknown entity slot name has been used to build the payload"""


# Spotify client
class SpotifyClientException(Exception):
    """An error occurred within the Spotify Client """


# Spotify query builder
class SpotifyQueryBuilderException(Exception):
    """An error occurred within the Spotify Query Builder"""


class SpotifyQueryBuilderNonExistentTimeRange(SpotifyQueryBuilderException):
    """The time range used does not exist, please use valid time ranges:
    'long_term', 'medium_term', 'short_term'"""

