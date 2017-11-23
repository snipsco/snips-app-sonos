#! /usr/bin/env python
# encoding: utf-8

import argparse

from snipssonos.spotify import SpotifyClient

SNIPS_SPOTIFY_APP_URL = "https://snips-spotify-login.herokuapp.com/"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "spotify_refresh_token",
        help="Spotify refresh token. Get one from {}".format(
            SNIPS_SPOTIFY_APP_URL)
    )
    parser.add_argument(
        "artist_file",
        help="Name of file to dump favorite artists (e.g. artists.txt)"
    )
    parser.add_argument(
        "track_file",
        help="Name of file to dump favorite tracks (e.g. tracks.txt)"
    )
    parser.add_argument(
        "playlist_file",
        help="Name of file to dump favorite playlists (e.g. playlists.txt)"
    )
    args = parser.parse_args()
    client = SpotifyClient(args.spotify_refresh_token)
    print "Dumping favorite artists to {}".format(args.artist_file)
    client.dump_favorite('artists', float("Inf"), args.artist_file)
    print "Dumping favorite tracks to {}".format(args.track_file)
    client.dump_favorite('tracks', float("Inf"), args.track_file)
    print "Dumping favorite playlists to {}".format(args.playlist_file)
    client.dump_playlists(args.playlist_file)


if __name__ == '__main__':
    main()
