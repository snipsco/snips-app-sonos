#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import logging
import time

from snipssonos.use_cases.request_objects import InjectEntitiesRequestFactory
from snipssonos.helpers.snips_config_parser import read_configuration_file
from snipssonos.services.spotify.music_customization_service import SpotifyCustomizationService
from snipssonos.services.entities_injection_service import EntitiesInjectionService
from snipssonos.use_cases.inject_entities import InjectEntitiesUseCase

HERMES_HOST = "localhost"
SECONDS_IN_A_DAY = 86400.0

ENTITIES = {
    "artists": "snips/artist",
    "tracks": "snips/song",
    "playlists": "playlistNameFR",
}

# Config & Logging
CONFIGURATION = read_configuration_file("config.ini")
LOG_LEVEL = CONFIGURATION['global']['log_level']
if LOG_LEVEL == "info":
    logging.basicConfig(level=logging.INFO)
elif LOG_LEVEL == "debug":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    client_id = CONFIGURATION['secret']['client_id']
    client_secret = CONFIGURATION['secret']['client_secret']
    refresh_token = CONFIGURATION['secret']['refresh_token']

    entities = {
        'entities': ENTITIES
    }
    music_customization_service = SpotifyCustomizationService(client_id, client_secret, refresh_token)
    entities_injection_service = EntitiesInjectionService(HERMES_HOST)

    starttime = time.time()
    # Code for scheduling taken from: https://stackoverflow.com/a/25251804
    # TODO first call get all top user data for the different time ranges
    # then in the loop just keep getting short term top data
    while True:
        inject_entities_request = InjectEntitiesRequestFactory\
            .from_dict(entities)

        use_case = InjectEntitiesUseCase(music_customization_service, entities_injection_service)

        response = use_case.execute(inject_entities_request)
        logging.info("Response: {}".format(bool(response)))

        time.sleep(SECONDS_IN_A_DAY - ((time.time() - starttime) % SECONDS_IN_A_DAY))
