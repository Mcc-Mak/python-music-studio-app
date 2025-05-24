# Music Studio (Python)
## Pre-requisite(s)
- *OS Windows* with *PowerShell*
- Installed *Python3* (as well as python_package:*virtualenv*)
## Installation
1. Download zip for this git project, and then unzip it to *<DIR_DEPLOYMENT>* (an absolute path)
2. Run `python3 -m venv <DIR_PROJECT>` (an absolute path)
3. Copy *.\MelodySheet\*, *.\MusicSheet\*, *.\OutputAudio\*, *.\\\*.py* and *.\requirements.txt* from *<DIR_DEPLOYMENT>\* into *<DIR_PROJECT>\*
4. Change the working directory to *<DIR_PROJECT>\*
5. Run `.\Scripts\Activate.ps1`
6. Run `.\Scripts\python.exe -m pip install --upgrade pip`
7. Run `.\Scripts\python.exe -m pip install -r requirements.txt`
8. (If available) Remove the directory of `.\MusicSheet\高唱入雲\` 
  - format: `.\MusicSheet\<SONG_NAME>\`
## SOP for Song Production
### Generate music sheet(s)
1. Change the working directory to *<DIR_PROJECT>*
2. Prepare `.\MelodySheet\高唱入雲.csv` as the melody file (format: `.\MelodySheet\<SONG_NAME>.csv`)
3. Run `.\Scripts\python.exe GenerateDemo.py 高唱入雲 "6_1@6_2@6_3@5_2@7_1"` (format: `.\Scripts\python.exe GenerateDemo.py "<SONG_NAME>" "<TRACK_i>_<CHANNEL_j>@..."`, where *<TRACK_i>*_*<CHANNEL_j>* pattern is repeatable (separated by *@*))
### Generate "MIDI" file
1. Change the working directory to *<DIR_PROJECT>*
2. Fine-tune the notes in *.\MusicSheet\<*
3. Run `.\Scripts\python.exe app.py 高唱入雲` (format: `.\Scripts\python.exe app.py <SONG_NAME>`)
## Settings
### for Song Production
- Configuration File
  - *.\_config.py*
    - capo (default: +3)
    - volume (default: 70)
    - duration (default: 1)
    - tempo  (default: 130)
    - lookup_track_name
    - lookup_program (ref: "General MIDI Program")
    - **music_sheet_shorthand (effective to the product by `.\Scripts\python.exe GenerateDemo.py "<SONG_NAME>" "<TRACK_i>_<CHANNEL_j>@..."`)
- Music Sheet
  - *MelodySheet\<SONG_NAME>.csv* (effective to the product of *MusicSheet\<SONG_NAME>\2_1.csv* by `.\Scripts\python.exe GenerateDemo.py "<SONG_NAME>" "<TRACK_i>_<CHANNEL_j>@..."`)
  - *MusicSheet\<SONG_NAME>\<Track_1-indexed>_<Channel_1-indexed>.csv* (effective to the product of *.\OutputAudio\<SONG_NAME>.midi*)
### for Music Sheet
- As metadata for song
  - Syntax: Last line
  - Usage: `Footer:<attr1>,<attr2>,<attr3>`
  - Notice
    - Set <attr1> to "True" to be in effective
- As data for song
  - Syntax: `<Time>,<Pitch>,<NoteVolumeOffset>,<NoteDurationOffset>,<NoteEnable>,<Comment>`
  - Attribute(s)
    - &lt;Time&gt;
      - equal "-1": Not effective to production (due to no weight in beat). Not even a note.
      - other: beat (in float) [1 is the note of 1/4]
    - &lt;Pitch&gt;
      - Syntax: `<attr1>.<attr2>.<attr3>`
        - &lt;attr1&gt;: *chord (e.g. C, G)* or *pitch (e.g. C3, G6)*
        - &lt;attr2&gt;: empty string if &lt;attr1&gt; as *pitch*. represent order in chord note if &lt;attr1&gt; as *chord*.
        - &lt;attr3&gt;: optional to change pitch for this note if &lt;attr1&gt; not as *pitch*.
          - Priority for pitch:
            1. Follow *&lt;attr1&gt;* (if *&lt;attr1&gt;* as *pitch*)
            2. Follow *&lt;attr3&gt;*
            3. Follow *metadata:&lt;attr2&gt;*
  - Notice
    - <NoteVolumeOffset>, <NoteDurationOffset> must be any *float* if <Time> not equal "-1"
    - <NoteEnable> must be "True if <Time> not equal "-1"
- As comment
  - Syntax: line starting by "#"

|Attribute|Usage|Description|
|---|---|---|
|META_DATA|&lt;attr1|True<br/>False|Enable this channel|
|META_DATA|&lt;attr2&gt;|Integer<br/>(i.e. 0,1,2,3,4,5,6,7)|Pitch for Note|
|META_DATA|&lt;attr3&gt;|-|(Reservation)|
|DATA|&lt;Time&gt;|e.g. -1, 0.25, 0.5, 1, 2, 1.3333, 0.6667|Time as beat&lt;br/&gt;(i.e. 1 refers to "note of 1/4")|
|DATA|&lt;Pitch&gt;|e.g.&lt;br/&gt;C.0.3&lt;br/&gt;C.0.&lt;br/&gt;C3..&lt;br/&gt;..|Lookup for a note|
|DATA|&lt;NoteVolumeOffset&gt;|Float|Adjust volume for this note|
|DATA|&lt;NoteDurationOffset&gt;|Float|Adjust duration for this note|
|DATA|&lt;NoteEnable&gt;|True&lt;br/&gt;False|Enable this note|
|DATA|&lt;Comment&gt;|String|Represent a comment visible to python data object|
## Documentation
#### Production
1. 高唱入雲 (Highly customized for "4_4@5_2")
2. [WIP] 願你國度降臨
#### General MIDI Program
|Category|Program|Instrument(s)|
|---|---|---|
|Piano|0|Acoustic Grand Piano|
|Piano|1|Bright Acoustic Piano|
|Organ|19|Church Organ|
|Guitar|24|Acoustic Guitar|
|Guitar|26|Electric Guitar|
|Bass|32|Acoustic Bass|
|Strings|40|Violin|
|Strings|42|Cello|
|Strings|43|Contrabass|
|Percussive|112|Tinkle Bell|
#### Reference
- General MIDI Program
  - https://computermusicresource.com/GM.Programs.html
- Music Note to Frequency
  - https://mixbutton.com/music-tools/frequency-and-pitch/music-note-to-frequency-chart
- Python Package
  - MIDIUtil
    - https://midiutil.readthedocs.io/en/1.2.1/#:~:text=MIDIUtil%20is%20a%20pure%20Python%20library%20that%20allows,1%20and%20format%202%20files%20are%20now%20supported%29.
  - Mingus
    - https://bspaans.github.io/python-mingus/