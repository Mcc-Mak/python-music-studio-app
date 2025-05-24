from basics import *
from _config import lookup_program

def GenerateDefaultContent(music_sheet_shorthand, track, channel):
    track_1i,channel_1i = str(track+1),str(channel+1)
    # track
    if lookup_program[f"Track_{track_1i}"] in [0,1,24]:
        volume_option = ["25","10","0"]
        duration_option = ["1", "1", "1"]
    elif lookup_program[f"Track_{track_1i}"] in [19]:
        volume_option = ["-15","-30","-50"]
        duration_option = ["4","2","1"]
    elif lookup_program[f"Track_{track_1i}"] in [42,43]:
        volume_option = ["15","0","-10"]
        duration_option = ["2","1.5","1"]
    else:
        volume_option = ["25","10","0"]
        duration_option = ["1", "1", "1"]
    # note_order
    if channel_1i == "1": note_order="0"
    elif channel_1i == "2": note_order="1"
    elif channel_1i == "3": note_order="2"
    elif channel_1i == "4": note_order="0"
    else: note_order="0"

    _silent = f"1,..,,,True,"

    content = []
    for note_grp in music_sheet_shorthand:
        content_grp = []
        if type(note_grp) is not list:
            content_grp += [
                # f"-1,,,,False,# {'... '*17}",
                f"-1,,,,False,# {note_grp}",
                # f"-1,,,,False,# {'... '*17}",
            ]
        else:
            for note in note_grp:
                _note,_beat = note.split('.')
                if _note == "":
                    content_grp += [f"{_beat},..,,,True,"]
                else:
                    if _beat == "4":
                        std4 = [
                            f"1,{_note}.{note_order}.,{volume_option[0]},{duration_option[0]},True,",
                            f"1,{_note}.{note_order}.,{volume_option[2]},{duration_option[2]},True,",
                            f"1,{_note}.{note_order}.,{volume_option[1]},{duration_option[1]},True,",
                            f"1,{_note}.{note_order}.,{volume_option[2]},{duration_option[2]},True,",
                        ]
                        if channel_1i == "1":
                            content_grp += std4
                        elif channel_1i == "2":
                            content_grp += [
                                std4[0],
                                _silent,
                                std4[2],
                                _silent
                            ]
                        elif channel_1i in ["3", "4"]:
                            content_grp += [
                                std4[0],
                                _silent,
                                _silent,
                                _silent,
                            ]
                        else:
                            content_grp += [
                                _silent,
                                _silent,
                                _silent,
                                _silent,
                            ]
                    elif _beat == "2":
                        std2 = [
                            f"1,{_note}.{note_order}.,{volume_option[0]},{duration_option[0]},True,",
                            f"1,{_note}.{note_order}.,{volume_option[2]},{duration_option[2]},True,",
                        ]
                        if channel_1i == "1":
                            content_grp += std2
                        elif channel_1i == "2":
                            content_grp += [
                                std2[0],
                                _silent,
                            ]
                        else:
                            content_grp += [
                                _silent,
                                _silent,
                            ]
        content += ['\n'.join(content_grp)]
    result = "\n".join(content)
    return result

def GetMusicSheet(song_name, track, channel, jdata={}):
    result = []
    track_1i = str(track+1)
    channel_1i = str(channel+1)
    filepath = f"MusicSheet/{song_name}/{track_1i}_{channel_1i}.csv"
    with open(filepath, 'r', encoding="utf8") as f:
        data = f.read().strip('\n').split('\n')
    _EnabledChannel,_ChannelDefaultPitch,_ChannelVolumeOffset = data[-1].split(':')[1].split(',')
    acc_time = 0
    for note in data[:-1]:
        if note[0] == "#": continue
        _Time, _PitchObj, _VolumeOffset, _DurationOffset, Enabled, Comment = note.split(',')
        # Example: ('1', 'C.0.', '0', '1', 'True', '')
        if Enabled != "True":
            if _Time == "-1":
                data = [acc_time, -1, None, None, None, Comment]
            else:
                data = [acc_time, -2, None, None, None, Comment]
        else:
            _arrPitch = _PitchObj.split('.')
            if _arrPitch[0] != "":
                if _arrPitch[1] == "":
                    _Pitch = _arrPitch[0]
                else:
                    if _arrPitch[2] == "":
                        _Pitch = f"{chords[_arrPitch[0]][int(_arrPitch[1])]}{_ChannelDefaultPitch}"
                    else:
                        _Pitch = f"{chords[_arrPitch[0]][int(_arrPitch[1])]}{_arrPitch[2]}"
                data = [
                    acc_time,
                    float(_Time),
                    jdata["_capo"] + GetMIDINote(_Pitch),
                    jdata["_volume"] + int(_ChannelVolumeOffset) + int(_VolumeOffset),
                    jdata["_duration"] + float(_DurationOffset),
                    Comment
                ]
            else:
                _Pitch = "C3"
                data = [
                    acc_time,
                    float(_Time),
                    GetMIDINote(_Pitch) + jdata["_capo"],
                    None,
                    None,
                    Comment
                ]
            acc_time += float(_Time)
        result += [data]
    return result
        