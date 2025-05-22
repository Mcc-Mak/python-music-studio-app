import mingus.core.scales as mingus_scales
chromatic = mingus_scales.Chromatic("C").ascending()

import mingus.core.chords as mingus_chords
chords={}
chords.update({
    f"{note}": mingus_chords.major_triad(note)
        for note in chromatic
})
chords.update({
    f"{note}m": mingus_chords.minor_triad(note)
        for note in chromatic
})
chords.update({
    f"{note}7": mingus_chords.major_seventh(note)
        for note in chromatic
})
chords.update({
    f"{note}m7": mingus_chords.minor_seventh(note)
        for note in chromatic
})

import mingus.core.notes as mingus_notes
GetMIDINote = lambda note: 24+12*int(note[-1])+mingus_notes.note_to_int(note[:-1])

from json import dumps
print("\n".join([
    "",
    f"chromatic: {dumps(chromatic)}",
    "",
    f"chords: {dumps(chords)}",
    "",
]))
