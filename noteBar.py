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


def noteToNumber(note_id):
    keys = {'C': 0, 'CS': 1, 'D': 2, 'DS': 3,
            'E': 4, 'F': 5, 'FS': 6, 'G': 7,
            'GS': 8, 'A': 9, 'AS': 10, 'B': 11}
    prefs = {'H': 1, 'M': 0, 'L': -1}
    p = prefs[note_id[:1]]
    n = int(note_id[1:2])
    key = keys[note_id[2:]]
    if p == prefs['H']:
        return 12 * (p + n) + key
    elif p == prefs['M']:
        return 12 * (n - 1) + key
    elif p == prefs['L']:
        return 12 * p * n + key


def noteDistance(note_id1, note_id2):
    return abs(noteToNumber(note_id1)-noteToNumber(note_id2))


def getMaleKey(note_id):
    return noteToNumber(note_id)-5


def numberToNote(number):
    keys = {0: 'C', 1: 'CS', 2: 'D', 3: 'DS',
            4: 'E', 5: 'F', 6: 'FS', 7: 'G',
            8: 'GS', 9: 'A', 10: 'AS', 11: 'B'}
    prefs = {1: 'H', 0: 'M', -1: 'L'}
    pref = int(number / 12)
    key = number % 12
    if pref < 0:
        p = prefs[-1]
        n = -1 * pref + 1
    elif pref < 2:
        p = prefs[0]
        n = pref + 1
    else:
        p = prefs[1]
        n = pref - 1
    return p + str(n) + keys[key]


def main():
    note1 = 'H2AS'
    note2 = 'L3B'
    print(note1, noteToNumber(note1))
    print(numberToNote(getMaleKey(note1)),
          noteToNumber(numberToNote(getMaleKey(note1))))


if __name__ == '__main__':
    main()
