class SonosActionException(Exception):
    """An exception occured with the Sonos Action."""


class ServiceException(SonosActionException):
    """An exception occured within a service"""


class DeviceDiscoveryException(ServiceException):
    """An exceptio occured with the device discovery service"""

class DeviceParsingException(DeviceDiscoveryException):
    """An error occured while trying to parse a device"""


class NoReachableDeviceException(DeviceDiscoveryException):
    """No connected devices were found by the DeviceDiscovery service"""


class APIRequestError(Exception):
    """An exception occured when interacting with Sonos API."""


class APIRequestWrongParams(APIRequestError):
    """The API was called with wrong parameters. """
