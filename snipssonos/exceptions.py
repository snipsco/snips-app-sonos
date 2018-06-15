class SonosActionException(Exception):
    """An exception occured with the Sonos Action."""


class ServiceException(SonosActionException):
    """An exception occured within a service"""


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
