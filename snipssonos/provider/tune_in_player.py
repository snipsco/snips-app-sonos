from .provider_player_template import A_ProviderPlayerTemplate
from soco.music_services import MusicService

class TuneInPlayer(A_ProviderPlayerTemplate):

    def __init__(self):
        try:
            self.tunein_service = MusicService('TuneIn')
        except Exception:
            self.tunein_service = None

    def play_station(self, device, name, shuffle=False):
        if self.tunein_service is None:
            return False
        res = self.tunein_service.search('stations', term=name)
        if 'mediaMetadata' not in res:
            return "radio not found"
        if isinstance(res['mediaMetadata'], list):
            radio_id = res['mediaMetadata'][0]['id']
        elif isinstance(res['mediaMetadata'], dict):
            radio_id = res['mediaMetadata']['id']
        else:
            raise TypeError("Unknown type for tune in search metadata")
        radio_uri = self.tunein_service.get_media_uri(radio_id)
        try:
            device.play_uri(radio_uri.replace('http', 'x-rincon-mp3radio'))
        except Exception:
            # unknown problem playing radio uri...
            return False
        return True
