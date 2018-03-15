from .provider_player_template import A_ProviderPlayerTemplate
from soco.music_services import MusicService
import soco
import random
from soco.data_structures import DidlItem, DidlResource
from soco.compat import quote_url
from .spotify import SpotifyClient

class SpotifyPlayer(A_ProviderPlayerTemplate):

    def __init__(self, spotify_refresh_token=None):
        try:
            self.spotify_service = MusicService('Spotify')
        except Exception:
            self.spotify_service = None
        if spotify_refresh_token is not None:
            self.spotify = SpotifyClient(spotify_refresh_token)
        else:
            self.spotify = None

    def play(self, device, name, shuffle=False, func=None):
        tracks = func(name)
        if tracks is None:
            return False
        device.stop()
        device.clear_queue()
        if shuffle:
            random.shuffle(tracks)
        for track in tracks:
            self.add_from_service(track['uri'], self.spotify_service, True, device)
        device.play_from_queue(0)
        return True

    def play_track(self, device, name, shuffle=False):
        if self.spotify is None:
            return False
        return self.play(device, name,shuffle, self.spotify.get_track)

    def play_artist(self, device, name, shuffle=False):
        if self.spotify is None:
            return False
        return self.play(device, name,shuffle, self.spotify.get_top_tracks_from_artist)

    def play_album(self, device, name, shuffle=False):
        if self.spotify is None:
            return False
        return self.play(device, name,shuffle, self.spotify.get_tracks_from_album)

    def play_playlist(self, device, name, shuffle=False):
        if self.spotify is None:
            return False
        return self.play(device, name,shuffle,self.spotify.get_tracks_from_playlist)

    def add_from_service(self, item_id, service, is_track=True, device=None):
        # The DIDL item_id is made of the track_id (url escaped), but with an 8
        # (hex) digit prefix. It is not clear what this is for, but it doesn't
        # seem to matter (too much) what it is. We can use junk (thought the
        # first digit must be 0 or 1), and the player seems to do the right
        # thing. Real DIDL items sent to a player also have a title and a
        # parent_id (usually the id of the relevant album), but they are not
        # necessary. The flow charts at http://musicpartners.sonos.com/node/421
        # and http://musicpartners.sonos.com/node/422 suggest that it is the job
        # of the player, not the controller, to call get_metadata with a track
        # id, so this might explain why no metadata is needed at this stage.

        # NB: quote_url will break if given unicode on Py2.6, and early 2.7. So
        # we need to encode.

        if device is None:
            return

        item_id = quote_url(item_id.encode('utf-8'))
        didl_item_id = "0fffffff{0}".format(item_id)

        # For an album:
        if not is_track:
            uri = 'x-rincon-cpcontainer:' + didl_item_id

        else:
            # For a track:
            uri = service.sonos_uri_from_id(item_id)

        res = [DidlResource(uri=uri, protocol_info="Snips")]
        didl = DidlItem(
            title="Snips",
            # This is ignored. Sonos gets the title from the item_id
            parent_id="Snips",  # Ditto
            item_id=didl_item_id,
            desc=service.desc,
            resources=res)

        device.add_to_queue(didl)
