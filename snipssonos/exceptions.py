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


class ExternalDeviceDiscoveryUnreachable(DeviceDiscoveryException):
    """An error occurred with the device discovery driver """


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


# Client
class ClientException(Exception):
    """An exception occured with the web client"""


# Spotify client
class SpotifyClientException(ClientException):
    """An error occurred within the Spotify Client """


class DeezerClientException(ClientException):
    """An error occured within the Deezer Client """


class SpotifyClientAuthException(SpotifyClientException):
    """An error occured when trying to auth the user from Spotify"""


class SpotifyClientAuthorizationException(SpotifyClientAuthException):
    """An error occured when retrieving authorization code from Spotify"""


class SpotifyClientAuthRefreshAccessTokenException(SpotifyClientAuthException):
    """An error occured when retrieving authorization code from Spotify"""


# Deezer client
class DeezerClientAuthorizationException(DeezerClientException):
    """An error occured when retrieving auth code from Deezer"""


class DeezerClientAuthRefreshAccessTokenException(DeezerClientException):
    """An error occured when retrieving code from Spotify"""


# Spotify query builder
class SpotifyQueryBuilderException(Exception):
    """An error occurred within the Spotify Query Builder"""


class SpotifyQueryBuilderNonExistentTimeRange(SpotifyQueryBuilderException):
    """The time range used does not exist, please use valid time ranges:
    'long_term', 'medium_term', 'short_term'"""


# Adapters exceptions
class AdapterException(SonosActionException):
    """Something wrong happened in the Interface Adapter layer"""


# Node query builder
class NodeQueryBuilderException(Exception):
    """An error occurred within the Node Query Builder"""


class NodeQueryBuilderUnavailableMusicService(NodeQueryBuilderException):
    """The music service is not implemented"""


class NodeQueryBuilderMissingQueryData(NodeQueryBuilderException):
    """Result type and/or field filters have not been provided"""


# Deezer search and play
class DeezerSearchServiceException(ServiceException):
    """An error occurred within the Deezer Search service"""


# Device Discovery Service
class DeviceDiscoveryServiceException(ServiceException):
    """An error occurred within the Device Discovery Service"""


# Configuration File Parsing
class ConfigurationFileValidationException(Exception):
    pass
