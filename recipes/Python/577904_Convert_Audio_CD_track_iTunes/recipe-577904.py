#!/usr/bin/env python
#coding=utf-8
import os
import sys

from time import sleep
from win32com.client import Dispatch


def exit(message):
    confirm = raw_input(message)
    sys.exit(1)

def main():
    itunes = Dispatch("iTunes.Application")
    for source in itunes.Sources:
        if source.Kind == 3:
            break
    else:
        exit("audio CD not found. Enter to exit.")
    if itunes.CurrentEncoder.Name.lower() != "lossless encoder":
        exit("Bad encoder, switch to ALAC please. Enter to exit.")
    playlist = source.Playlists[0]
    # convert tracks in audio cd.
    status = itunes.ConvertTracks(playlist.Tracks)
    while status.InProgress:
        sleep(1)

    all_tracks = itunes.LibraryPlaylist.Tracks
    album_name = playlist.Name
    for cd_track in playlist.Tracks:
        for track in reversed(all_tracks):
            if track.Name == cd_track.Name and track.Album == album_name:
                print track.Duration == cd_track.Duration, track.Name, track.Duration, cd_track.Duration
                if track.Duration != cd_track.Duration:
                    # Convert again. 
                    retry = 0
                    while track.Duration != cd_track.Duration and retry < 10:
                        # delete bad converted track.
                        print "retrying %s, count=%s" % (track.Name, retry)
                        retry += 1
                        os.remove(track.Location)
                        track.Delete()
                        # Convert again.
                        status = itunes.ConvertTrack(cd_track)
                        while status.InProgress:
                            sleep(0.5)
                        for t in reversed(all_tracks):
                            if t.Name == cd_track.Name and t.Album == album_name:
                                track = t
                                break
                        else:
                            print "track '%s' not found." % track.Name
                    if retry >= 10:
                        confirm = raw_input("'%s' not converted." % track.Name)
                break
        else:
            print "track '%s' not found." % track.Name

    raw_input("all done.")


if __name__ == "__main__":
    main()
