from snipssonos.helpers.configuration_validator import ConfigurationValidator, MandatoryField, ValueField

AVAILABLE_MUSIC_SERVICES = ["spotify", "deezer"]
AVAILABLE_LANGUAGES = ["fr", "en"]


def validate_configuration_file(configuration_file, validator=None):
    if validator is None:  # That means we use the default validator, since none was provided
        validator = ConfigurationValidator()

        node_device_transport_control_port_mandatory_field = MandatoryField("global",
                                                                            "node_device_transport_control_port")
        node_device_transport_control_host_mandatory_field = MandatoryField("global",
                                                                            "node_device_transport_control_host")
        node_device_discovery_port_mandatory_field = MandatoryField("global", "node_device_discovery_port")
        node_device_discovery_host_mandatory_field = MandatoryField("global", "node_device_discovery_host")
        node_music_playback_port_mandatory_field = MandatoryField("global", "node_music_playback_port")
        node_music_playback_host_mandatory_field = MandatoryField("global", "node_music_playback_host")
        hostname_mandatory_field = MandatoryField("global", "hostname")
        music_provider_field = MandatoryField("global", "music_provider")

        language_field = ValueField("global", "language", AVAILABLE_LANGUAGES)

        secret_client_id = MandatoryField("secret", "client_id")
        secret_client_secret = MandatoryField("secret", "client_secret")

        validator.add_mandatory_fields(node_device_transport_control_port_mandatory_field,
                                   node_device_transport_control_host_mandatory_field,
                                   node_device_discovery_port_mandatory_field,
                                   node_device_discovery_host_mandatory_field,
                                   node_music_playback_port_mandatory_field,
                                   node_music_playback_host_mandatory_field,
                                   hostname_mandatory_field, music_provider_field)

        validator.add_field_values(language_field)

        validator.add_mandatory_fields(secret_client_id, secret_client_secret)

        return validator.validate_configuration(configuration_file)
