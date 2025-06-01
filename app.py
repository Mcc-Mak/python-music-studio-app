from json import dumps
import sys, os

if len(sys.argv) == 2:
    
    #
    # .\Scripts\python.exe app.py "願你國度降臨"
    #
    
    from lib import GetMusicSheet
    from _config import capo, no_of_tracks, no_of_channels, volume, duration, tempo, note_slip, lookup_track_name, lookup_program, __MUTE_COMPONENT__

    from midiutil import MIDIFile
    MyMIDI = MIDIFile(no_of_tracks)

    #
    # Argument:
    #
    #   1. <SongName> (e.g. 高唱入雲)
    #
    __SongName__ = sys.argv[1]

    start_time = 0
    # start_time = 4 * 2 + 16 * 4 + 16 * 4 + 4 *4 
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
        
elif len(sys.argv) == 3:
    
    #
    # .\Scripts\python.exe app.py "願你國度降臨" "3_2@3_3@3_4@6_1@6_2@6_3"
    #
    
    from _config import music_sheet_shorthand, default_content
    from lib import GenerateDefaultContent

    # 
    # Argument(s):
    #
    #   1. <SongName> (e.g. 高唱入雲)
    #
    __SongName__ = sys.argv[1]
    #
    #   2. <Track (1)>_<Channel (1)>@<Track (1)>_<Channel (2)>@...@<Track (n)>_<Channel (k)>
    #
    enabled_channels = sys.argv[2]
    track_channel = [pair for pair in enabled_channels.strip().split('@')]
    
    DIR_MUSIC_SHEET = f"MusicSheet/{__SongName__}"
    if os.path.exists(DIR_MUSIC_SHEET):
        print("[Warning] Pre-existing song! Terminating...")
        exit()
    os.mkdir(DIR_MUSIC_SHEET)
    print(f"[Info] Created folder: '{os.path.realpath(DIR_MUSIC_SHEET)}'")
    print()
    from _config import no_of_tracks, no_of_channels
    for track in range(no_of_tracks):
        track_1i = str(track+1)
        for channel in range(no_of_channels):
            channel_1i = str(channel+1)
            filepath = os.path.realpath(f'{DIR_MUSIC_SHEET}/{track_1i}_{channel_1i}.csv')
            print(f"[Info] Created '{DIR_MUSIC_SHEET}/{track_1i}_{channel_1i}.csv'")
            with open(filepath, 'a', encoding="utf-8") as f:
                f.write(
                    f'{default_content["header"]}\n{GenerateDefaultContent(music_sheet_shorthand, track, channel)}\n{default_content["footer"]%("True","2","-1")}'
                        if f"{track_1i}_{channel_1i}" in track_channel
                        else
                    f'{default_content["header"]}\n{default_content["footer"]%("False","-1","0")}'
                )
    import shutil
    src_file = f"MelodySheet/{__SongName__}.csv"
    if os.path.exists(src_file):
        shutil.copyfile(src_file, f"MusicSheet/{__SongName__}/2_5.csv")
    
    # Highly customized music sheet (non-melody)
    highly_customized_music_sheets = enabled_channels.split('@')
    for sheet in highly_customized_music_sheets:
        src_file = f"MusicSheetHighlyCustomized/{__SongName__}/{sheet}.csv"
        if os.path.exists(src_file):
            dest_file = f"MusicSheet/{__SongName__}/{sheet}.csv"
            shutil.copyfile(src_file, dest_file)
