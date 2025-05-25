from lib import GetMusicSheet
from _config import capo, no_of_tracks, no_of_channels, volume, duration, tempo, note_slip, lookup_track_name, lookup_program, __MUTE_COMPONENT__

from json import dumps

from midiutil import MIDIFile
MyMIDI = MIDIFile(no_of_tracks)

import sys
# __SongName__ = "願你國度降臨"
__SongName__ = sys.argv[1]

start_time = 19+56+16+16
for track in range(no_of_tracks):
    track_1i = str(track+1)
    MyMIDI.addTrackName(track, 0, lookup_track_name[f"Track_{track_1i}"])
    MyMIDI.addTempo(track, 0, tempo)
    for channel in range(no_of_channels):
        channel_1i = str(channel+1)
        music_sheet = GetMusicSheet(
            __SongName__,
            track,
            channel,
            jdata = {
                "_capo": capo,
                "_volume": volume,
                "_duration": duration,
            }
        )
        if not music_sheet or track_1i in __MUTE_COMPONENT__["Track"] or channel_1i in __MUTE_COMPONENT__["Channel"]:
            print(f"[INFO] Disabled: Track-{track_1i}, Channel-{channel_1i}")
        else:
            for note in music_sheet:
                # print(note)
                if note[1] > 0:
                    if note[0] <= start_time: continue
                    MyMIDI.addProgramChange(track, channel, note[0]-start_time, lookup_program[f'Track_{track_1i}'])
                    slip=channel*note_slip
                    if note[3] == None:
                        MyMIDI.addNote(track, channel, note[2], note[0]-start_time+slip, 1, 1)
                    else:
                        MyMIDI.addNote(track, channel, note[2], note[0]-start_time+slip, note[4], note[3])
                        # print(note[2], note[0], note[4], note[3])
            print(f"[INFO] Enabled: Track-{track_1i}, Channel-{channel_1i}; Program: {lookup_program[f'Track_{track_1i}']}; Beat (Total): {note[0]}")
    print()

with open(f"OutputAudio/{__SongName__}.midi", 'wb') as output_file:
    MyMIDI.writeFile(output_file)