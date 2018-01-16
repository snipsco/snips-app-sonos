#! /usr/bin/env python
# encoding: utf-8

import argparse
import codecs
import soco

from soco.music_services import MusicService

def dump_item_list(sonos_ip_adress, mode, output_file):
    if mode not in ['artists', 'tracks', 'albums', 'playlists']:
            raise ValueError("mode argument should be 'artists', 'tracks', 'albums' or 'playlists'")
    
    device = soco.core.SoCo(sonos_ip_adress)
    my_library = soco.music_library.MusicLibrary(device)
    
    items = my_library.get_music_library_information(mode, complete_result=True)
    items_title = map(lambda a: a.title, items)
    with codecs.open(output_file, 'w', 'utf-8') as f:
            f.write(u"\n".join(items_title))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sonos_ip_adress",
        help="The local ip adress for one of your sonos speakers"
    )
    parser.add_argument(
        "artist_file",
        help="Name of file to dump artists (e.g. artists.txt)"
    )
    parser.add_argument(
        "track_file",
        help="Name of file to dump tracks (e.g. tracks.txt)"
    )
    parser.add_argument(
        "playlist_file",
        help="Name of file to dump playlists (e.g. playlists.txt)"
    )
    parser.add_argument(
        "album_file",
        help="Name of file to dump albums (e.g. albums.txt)"
    )
    args = parser.parse_args()    
    
    print "Dumping all artists to {}".format(args.artist_file)
    dump_item_list(args.sonos_ip_adress, 'artists', args.artist_file)
    
    
    print "Dumping all tracks to {}".format(args.track_file)
    dump_item_list(args.sonos_ip_adress, 'tracks', args.track_file)
    
    print "Dumping all playlists to {}".format(args.playlist_file)
    dump_item_list(args.sonos_ip_adress, 'sonos_playlists', args.playlist_file)
    
    print "Dumping all albums to {}".format(args.album_file)
    dump_item_list(args.sonos_ip_adress, 'albums', args.album_file)


if __name__ == '__main__':
    main()