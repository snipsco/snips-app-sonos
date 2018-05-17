#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

from snipssonos.snipssonos_node import SnipsSonosClient

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

HOSTNAME = "raspi-dev-antho.local"

HERMES_HOST = "{}:1883".format(HOSTNAME)
MOPIDY_HOST = HOSTNAME

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def addSong_callback(hermes, intentMessage):
    pass

def getInfos_callback(hermes, intentMessage):
    pass


def playAlbum_callback(hermes, intentMessage):
    pass

def playArtist_callback(hermes, intentMessage):
    pass

def playPlaylist_callback(hermes, intentMessage):
    pass

def playSong_callback(hermes, intentMessage):
    pass



# Playback functions
def radioOn_callback(hermes, intentMessage):
    pass

def previousSong_callback(hermes, intentMessage):
    pass

def nextSong_callback(hermes, intentMessage):
    pass

def resumeMusic_callback(hermes, intentMessage):
    hermes.skill.play("Antho Room")

def speakerInterrupt_callback(hermes, intentMessage):
    hermes.skill.pause("Antho Room")

def volumeDown_callback(hermes, intentMessage):
    pass

def volumeUp_callback(hermes, intentMessage):
    pass


if __name__ == "__main__":

    with Hermes(HERMES_HOST) as h:

        h.skill = SnipsSonosClient()

        h\
            .subscribe_intent("volumeUp", volumeUp_callback) \
            .subscribe_intent("previousSong", previousSong_callback) \
            .subscribe_intent("playSong", playSong_callback) \
            .subscribe_intent("playArtist", playArtist_callback) \
            .subscribe_intent("getInfos", getInfos_callback) \
            .subscribe_intent("speakerInterrupt", speakerInterrupt_callback) \
            .subscribe_intent("resumeMusic", resumeMusic_callback) \
            .subscribe_intent("addSong", addSong_callback) \
            .subscribe_intent("nextSong", nextSong_callback) \
            .subscribe_intent("radioOn", radioOn_callback) \
            .subscribe_intent("playAlbum", playAlbum_callback) \
            .subscribe_intent("volumeDown", volumeDown_callback) \
            .subscribe_intent("playPlaylist", playPlaylist_callback) \
            .loop_forever()
