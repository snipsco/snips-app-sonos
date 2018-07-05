from snipssonos.helpers.snips_config_parser import read_configuration_file


class Service(object):
    CONFIG = "config.ini"
    CONFIGURATION = read_configuration_file(CONFIG)
