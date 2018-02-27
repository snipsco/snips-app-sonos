from abc import ABC, ABCMeta,  abstractmethod

class A_ProviderPlayerTemplate(ABC):
    """
        Abstract Class to create a music provider as Spotify, Soundclound
        you have to create at least one of the play method and the __init__ method
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def play_artist(self, device, name, shuffle=False):
        """ 
            Play a music from a artist

            :param self: self
            :param device: the sonos speaker the skill is connected to
            :param name: artist name
            :param shuffle: do we need to shuffle the list of music
            :type device: soco.core.Soco
            :type name: string
            :type shuffle: Boolean
            :return: Did we succed to play a music
            :rtype: Boolean
        """
        return False

    @classmethod
    def play_track(self, device, name, shuffle=False):
        """ 
            Play a track with its name

            :param self: self
            :param device: the sonos speaker the skill is connected to
            :param name: track name
            :param shuffle: do we need to shuffle the list of music
            :type device: soco.core.Soco
            :type name: string
            :type shuffle: Boolean
            :return: Did we succed to play a music
            :rtype: Boolean
        """
        return False

    @classmethod
    def play_album(self, device, name, shuffle=False):
        """ 
            Play an album

            :param self: self
            :param device: the sonos speaker the skill is connected to
            :param name: album name
            :param shuffle: do we need to shuffle the list of music
            :type device: soco.core.Soco
            :type name: string
            :type shuffle: Boolean
            :return: Did we succed to play a music
            :rtype: Boolean
        """
        return False

    @classmethod
    def play_playlist(self, device, name, shuffle=False):
        """ 
            Play a playlist

            :param self: self
            :param device: the sonos speaker the skill is connected to
            :param name: playlist name
            :param shuffle: do we need to shuffle the list of music
            :type device: soco.core.Soco
            :type name: string
            :type shuffle: Boolean
            :return: Did we succed to play a music
            :rtype: Boolean
        """
        return False

    @classmethod
    def play_station(self, device, name, shuffle=False):
        """ 
            Play a radio station

            :param self: self
            :param device: the sonos speaker the skill is connected to
            :param name: radio station name
            :param shuffle: do we need to shuffle the list of music
            :type device: soco.core.Soco
            :type name: string
            :type shuffle: Boolean
            :return: Did we succed to play a music
            :rtype: Boolean
        """
        return False

    @classmethod
    def play_genre(self, device, name, shuffle=False):
        """ 
            Play a music genre

            :param self: self
            :param device: the sonos speaker the skill is connected to
            :param name: genre name
            :param shuffle: do we need to shuffle the list of music
            :type device: soco.core.Soco
            :type name: string
            :type shuffle: Boolean
            :return: Did we succed to play a music
            :rtype: Boolean
        """
        return False

    @classmethod
    def play_tag(self, device, name, shuffle=False):
        """ 
            Play music from its tag

            :param self: self
            :param device: the sonos speaker the skill is connected to
            :param name: tag name
            :param shuffle: do we need to shuffle the list of music
            :type device: soco.core.Soco
            :type name: string
            :type shuffle: Boolean
            :return: Did we succed to play a music
            :rtype: Boolean
        """
        return False
