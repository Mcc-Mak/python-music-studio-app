
from _config import music_sheet_shorthand, default_content
from lib import GenerateDefaultContent

import sys, os
# 
# Argument(s):
#   1. <SongName> (e.g. 高唱入雲)
song_name = sys.argv[1]
#   2. <Track (1)>_<Channel (1)>@<Track (1)>_<Channel (2)>@...@<Track (n)>_<Channel (k)>
enabled_channels = sys.argv[2]
track_channel = [pair for pair in enabled_channels.strip().split('@')]
#
#
#
DIR_MUSIC_SHEET = f"MusicSheet/{song_name}"
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
shutil.copyfile(f"MelodySheet/{song_name}.csv", f"MusicSheet/{song_name}/2_5.csv")
# 3. Highly customized music sheet (non-melody)
highly_customized_music_sheets = enabled_channels.split('@')
for sheet in highly_customized_music_sheets:
    src_file = f"MusicSheetHighlyCustomized/{song_name}/{sheet}.csv"
    if os.path.exists(src_file):
        dest_file = f"MusicSheet/{song_name}/{sheet}.csv"
        shutil.copyfile(src_file, dest_file)
