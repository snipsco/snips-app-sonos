from snipssonos.helpers.snips_config_parser import read_configuration_file


class Service(object):
    SERVICE_NAME = "SERVICE"  # This variable should be overridden 


class ConfigurableService(Service):

    def __init__(self, CONFIGURATION=None):
        self.CONFIGURATION = CONFIGURATION


class HTTPService(Service):
    PROTOCOL = "http://"
    SECURE_PROTOCOL = "https://"
    PORT = 80
    HOST = "localhost"


class ConfigurableHTTPService(ConfigurableService, HTTPService):
    def __init__(self, CONFIGURATION=None):
        super(ConfigurableHTTPService, self).__init__(CONFIGURATION)
        if CONFIGURATION:
            self.read_port_from_config()
            self.read_host_from_config()

    def read_port_from_config(self):
        self.PORT = self.CONFIGURATION['global']["{}_port".format(self.SERVICE_NAME)] if (
            self.CONFIGURATION['global']["{}_port".format(self.SERVICE_NAME)]) else self.PORT

    def read_host_from_config(self):
        self.HOST = self.CONFIGURATION['global']["{}_host".format(self.SERVICE_NAME)] if (
            self.CONFIGURATION['global']["{}_host".format(self.SERVICE_NAME)]) else self.HOST
