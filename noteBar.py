def marger(P, pref, loop=2):
    note = dict()
    keys = {'C': 'C', 'CS': 'C#', 'D': 'D', 'DS': 'D#',
            'E': 'E', 'F': 'F', 'FS': 'F#', 'G': 'G',
            'GS': 'G#', 'A': 'A', 'AS': 'A#', 'B': 'B'}
    for i in range(loop):
        for K, key in keys.items():
            pk = P + str(i + 1) + K
            if P != 'M':
                keyname = pref * (i + 1) + key
            else:
                keyname = pref + str(i+1) + key
            # print(pk, ':', keyname)
            note[pk] = keyname
    return note


def makeNoteTable(lh=3):
    note = dict()
    prefs = {'H': 'hi', 'M': 'mid', 'L': 'low'}
    for P, pref in prefs.items():
        if P != 'M':
            note.update(marger(P, pref, lh))
        else:
            note.update(marger(P, pref))
    return note


def main():
    notes = makeNoteTable(4)
    for note, note_val in notes.items():
        print(note,note_val)


if __name__ == '__main__':
    main()
