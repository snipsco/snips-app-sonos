import pytest

from snipssonos.helpers.configuration_validator import ConfigurationValidator, ConfigurationFileValidationException, \
    MandatoryField, ValueField


def test_validate_correct_configuration_file():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2'
        },
        'secret': {
        }
    }

    validator = ConfigurationValidator()
    mandatoryfield = MandatoryField("global", "field1")

    validator.add_mandatory_field(mandatoryfield)

    assert True is validator.validate_configuration(configuration_file)


def test_validate_incorrect_configuration_file():
    configuration_file = {
        'global': {
            'field2': 'value1',
            'field3': 'value2'
        },
        'secret': {
        }
    }

    validator = ConfigurationValidator()
    mandatoryfield = MandatoryField("global", "field1")

    validator.add_mandatory_field(mandatoryfield)

    with pytest.raises(ConfigurationFileValidationException):
        validator.validate_configuration(configuration_file)


def test_field_value_validation():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2',
            'music_provider': "deezer"
        },
        'secret': {
        }
    }

    validator = ConfigurationValidator()
    valfield = ValueField("global", "music_provider", ["deezer", "spotify"])

    validator.add_field_value(valfield)
    assert validator.validate_configuration(configuration_file) is True


def test_field_value_validation_incorrect():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2',
            'music_provider': "deezere"
        },
        'secret': {
        }
    }

    validator = ConfigurationValidator()
    valfield = ValueField("global", "music_provider", possible_values=["deezer", "spotify"])

    validator.add_field_value(valfield)
    with pytest.raises(ConfigurationFileValidationException):
        validator.validate_configuration(configuration_file)


def test_field_value_validation_incorrect_different_types():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2',
            'music_provider': 1
        },
        'secret': {
        }
    }

    validator = ConfigurationValidator()
    valfield = ValueField("global", "music_provider", possible_values=["deezer", "spotify"])

    validator.add_field_value(valfield)
    with pytest.raises(ConfigurationFileValidationException):
        validator.validate_configuration(configuration_file)


def test_field_value_and_mandatory_field_on_same_name_correct():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2',
            'music_provider': "spotify"
        },
        'secret': {
        }
    }

    validator = ConfigurationValidator()
    valfield = ValueField("global", "music_provider", possible_values=["deezer", "spotify"])
    mandatoryfield = MandatoryField("global", "music_provider")

    validator.add_field_value(valfield)
    validator.add_mandatory_field(mandatoryfield)

    assert validator.validate_configuration(configuration_file) is True


def test_mandatory_value_with_same_name_in_secret_and_global_field():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2',
            'music_provider': "spotify"
        },
        'secret': {
            'field1': 'secretvalue1',
            'music_provider' : "deezer"
        }
    }

    validator = ConfigurationValidator()
    mandatoryfield_global = MandatoryField("global", "music_provider")
    mandatoryfield_secret = MandatoryField("secret", "music_provider")

    validator.add_mandatory_field(mandatoryfield_global)
    validator.add_mandatory_field(mandatoryfield_secret)

    assert validator.validate_configuration(configuration_file) is True

def test_value_field_with_same_name_in_secret_and_global_field_and_same_values():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2',
            'music_provider': "spotify"
        },
        'secret': {
            'field1': 'secretvalue1',
            'music_provider' : "deezer"
        }
    }

    music_providers = ["spotify","deezer","napster"]
    validator = ConfigurationValidator()
    mandatoryfield_global = ValueField("global", "music_provider", music_providers)
    mandatoryfield_secret = ValueField("secret", "music_provider", music_providers)

    validator.add_field_value(mandatoryfield_global)
    validator.add_field_value(mandatoryfield_secret)

    assert validator.validate_configuration(configuration_file) is True


def test_value_field_with_same_name_in_secret_and_global_field_and_different_values():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2',
            'music_provider': "spotify"
        },
        'secret': {
            'field1': 'secretvalue1',
            'music_provider' : "soundcloud"
        }
    }

    validator = ConfigurationValidator()
    mandatoryfield_global = ValueField("global", "music_provider", ["spotify","deezer"])
    mandatoryfield_secret = ValueField("secret", "music_provider", ["apple_music","soundcloud"])

    validator.add_field_value(mandatoryfield_global)
    validator.add_field_value(mandatoryfield_secret)

    assert validator.validate_configuration(configuration_file) is True



def test_value_field_with_same_name_in_secret_and_global_field_and_different_values_incorrect():
    configuration_file = {
        'global': {
            'field1': 'value1',
            'field2': 'value2',
            'music_provider': "spotify"
        },
        'secret': {
            'field1': 'secretvalue1',
            'music_provider' : "napster"
        }
    }

    validator = ConfigurationValidator()
    mandatoryfield_global = ValueField("global", "music_provider", ["spotify","deezer"])
    mandatoryfield_secret = ValueField("secret", "music_provider", ["apple_music","soundcloud"])

    validator.add_field_value(mandatoryfield_global)
    validator.add_field_value(mandatoryfield_secret)

    with pytest.raises(ConfigurationFileValidationException):
        validator.validate_configuration(configuration_file)