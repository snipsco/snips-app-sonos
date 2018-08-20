# -*-: coding utf-8 -*-
import logging

from snipssonos.exceptions import ConfigurationFileValidationException


class MandatoryField(object):
    def __init__(self, category, name):
        self.name = name
        self.category = category


class ValueField(object):
    def __init__(self, category, name, possible_values):
        self.name = name
        self.possible_values = possible_values
        self.category = category


class ConfigurationValidator(object):
    def __init__(self):
        self.mandatory_fields = list()
        self.value_fields = list()

    def add_mandatory_field(self, field):
        self.mandatory_fields.append(field)

    def add_field_value(self, field):
        self.value_fields.append(field)


    def add_field_values(self, *args):
        for field in args:
            self.value_fields.append(field)

    def add_mandatory_fields(self, *args):
        for field in args:
            self.mandatory_fields.append(field)

    def validate_configuration(self, configuration_dict):
        errors = list()

        for mandatory_field in self.mandatory_fields:
            if not (mandatory_field.name in configuration_dict[mandatory_field.category].keys()):
                errors.append("Missing field : In section [{}], field {} is missing config.ini file. ".format(mandatory_field.category, mandatory_field.name))

        for value_field in self.value_fields:
            if not (value_field.name in configuration_dict[value_field.category].keys()):
                errors.append("Missing field : In section [{}], field {} is missing config.ini file. ".format(value_field.category, value_field.name))
            else:
                value = configuration_dict[value_field.category][value_field.name]
                if value not in value_field.possible_values:
                    errors.append(
                        "Field {} has incorrect value : {}. Possible values : {}".format(value_field.name, value,
                                                                                         ", ".join(
                                                                                             [str(possible_value) for
                                                                                              possible_value in
                                                                                              value_field.possible_values])))

        if len(errors) > 0:
            error_message = ", ".join(errors)
            raise ConfigurationFileValidationException(errors)
        else:
            logging.info("The configuration file is valid.")
            return True
