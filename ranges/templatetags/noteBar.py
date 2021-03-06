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

# %%


def noteToNumber(note_id):
    keys = {'C': 3, 'CS': 4, 'D': 5, 'DS': 6,
            'E': 7, 'F': 8, 'FS': 9, 'G': 10,
            'GS': 11, 'A': 0, 'AS': 1, 'B': 2}
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
    return numberToNote(noteToNumber(note_id)-7)


def numberToNote(number):
    keys = {0: 'A', 1: 'AS', 2: 'B', 3: 'C',
            4: 'CS', 5: 'D', 6: 'DS', 7: 'E',
            8: 'F', 9: 'FS', 10: 'G', 11: 'GS', }
    prefs = {1: 'H', 0: 'M', -1: 'L'}
    pref = int(number / 12)
    key = number % 12
    if number < 0:
        p = prefs[-1]
        pref = int((number+1) / 12)
        n = -1 * pref + 1
    elif pref < 2:
        p = prefs[0]
        n = pref + 1
    else:
        p = prefs[1]
        n = pref - 1
    return p + str(n) + keys[key]


def maleKey(l, h):
    print(l, '->', getMaleKey(l))
    print(h, '->', getMaleKey(h))


def addKey(l, h, add):
    print(l, '->', numberToNote(noteToNumber(l)+add))
    print(h, '->', numberToNote(noteToNumber(h)+add))
# %%


def main():
    l = 'M1FS'
    h = 'H1FS'
    addKey(l, h, -4)


if __name__ == '__main__':
    main()

# %%
