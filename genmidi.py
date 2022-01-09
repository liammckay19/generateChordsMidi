from midiutil.MidiFile import MIDIFile


class ChordProgressionGenerator:
    def __init__(self, scale_root, LOWEST_OCTAVE):
        OCTAVES = {1: 60 - 36, 2: 60 - 24, 3: 60 - 12, 4: 60, 5: 60 + 12}

        self.scale_root = scale_root
        self.LOWEST_OCTAVE = LOWEST_OCTAVE

        self.rootlookup = {
            "A": -3,
            "A#": -2,
            "B": -1,
            "C": 0,
            "C#": 1,
            "D": 2,
            "D#": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "G#": 7,
        }
        i = self.rootlookup[self.scale_root]

        c_dim = {
            "C": OCTAVES[self.LOWEST_OCTAVE] - 1 + i,
            "D": OCTAVES[self.LOWEST_OCTAVE] + 1 + i,
            "E": OCTAVES[self.LOWEST_OCTAVE] + 2 + i,
            "F": OCTAVES[self.LOWEST_OCTAVE] + 4 + i,
            "G": OCTAVES[self.LOWEST_OCTAVE] + 6 + i,
            "A": OCTAVES[self.LOWEST_OCTAVE] + 7 + i,
            "B": OCTAVES[self.LOWEST_OCTAVE] + 9 + i,
        }
        c_aug = {
            "C": OCTAVES[self.LOWEST_OCTAVE] + 1 + i,
            "D": OCTAVES[self.LOWEST_OCTAVE] + 3 + i,
            "E": OCTAVES[self.LOWEST_OCTAVE] + 5 + i,
            "F": OCTAVES[self.LOWEST_OCTAVE] + 6 + i,
            "G": OCTAVES[self.LOWEST_OCTAVE] + 7 + i,
            "A": OCTAVES[self.LOWEST_OCTAVE] + 10 + i,
            "B": OCTAVES[self.LOWEST_OCTAVE] + 12 + i,
        }
        self.c_min = {
            "C": OCTAVES[self.LOWEST_OCTAVE] + i,
            "D": OCTAVES[self.LOWEST_OCTAVE] + 2 + i,
            "E": OCTAVES[self.LOWEST_OCTAVE] + 3 + i,
            "F": OCTAVES[self.LOWEST_OCTAVE] + 5 + i,
            "G": OCTAVES[self.LOWEST_OCTAVE] + 7 + i,
            "A": OCTAVES[self.LOWEST_OCTAVE] + 8 + i,
            "B": OCTAVES[self.LOWEST_OCTAVE] + 10 + i,
        }
        self.c_maj = {
            "C": OCTAVES[self.LOWEST_OCTAVE] + i,
            "D": OCTAVES[self.LOWEST_OCTAVE] + 2 + i,
            "E": OCTAVES[self.LOWEST_OCTAVE] + 4 + i,
            "F": OCTAVES[self.LOWEST_OCTAVE] + 5 + i,
            "G": OCTAVES[self.LOWEST_OCTAVE] + 7 + i,
            "A": OCTAVES[self.LOWEST_OCTAVE] + 9 + i,
            "B": OCTAVES[self.LOWEST_OCTAVE] + 11 + i,
        }
        self.R_c_maj = {midi: note for note, midi in self.c_maj.items()}
        self.c_maj_list = {1: "C", 2: "D", 3: "E", 4: "F", 5: "G", 6: "A", 7: "B"}
        self.R_c_maj_list = {note: deg for deg, note in self.c_maj_list.items()}
        # self.c_maj_low = {note: midi - 12 for note, midi in self.c_maj.items()}

    # self.c_maj_hi = {note: midi + 12 for note, midi in self.c_maj.items()}
    # c_maj_midi = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    # R_c_maj_midi = {midi: note for note, midi in c_maj_midi.items()}

    def get_add_maj_min_sus_interval(self, midi, interval, majmin="maj"):
        if interval == 2:
            return midi + 2
        elif interval == 4:
            return midi + 4
        elif interval == 7:
            if majmin == "maj":
                return midi + 11
            if majmin == "min":
                return midi + 10
        elif interval == 9:
            if majmin == "maj":
                return midi + 14
            if majmin == "min":
                return midi + 13
        else:
            return midi

    def get_maj_scale_chords(
        self, scale_root, inversion="closed", add=[], dom=[], majmin="maj"
    ):
        simple_maj_chords = {
            "i": [self.c_min["C"], self.c_min["E"], self.c_min["G"]],
            "I": [self.c_maj["C"], self.c_maj["E"], self.c_maj["G"]],
            "ii": [self.c_maj["D"], self.c_maj["F"], self.c_maj["A"]],
            "II": [self.c_maj["D"], self.c_maj["F"] + 1, self.c_maj["A"]],
            "iii": [self.c_maj["E"], self.c_maj["G"], self.c_maj["B"]],
            "III": [self.c_maj["E"], self.c_maj["G"] + 1, self.c_maj["B"]],
            "iv": [self.c_maj["F"], self.c_maj["A"] - 1, self.c_maj["C"]],
            "IV": [self.c_maj["F"], self.c_maj["A"], self.c_maj["C"]],
            "v": [self.c_maj["G"], self.c_maj["B"] - 1, self.c_maj["D"]],
            "V": [self.c_maj["G"], self.c_maj["B"], self.c_maj["D"]],
            "vi": [self.c_maj["A"], self.c_maj["C"], self.c_maj["E"]],
            "VI": [self.c_maj["A"], self.c_maj["C"] + 1, self.c_maj["E"]],
            "viio": [self.c_maj["B"], self.c_maj["D"], self.c_maj["F"]],
            "VIIaug": [self.c_maj["B"], self.c_maj["D"] + 1, self.c_maj["F"] + 1],
        }
        extended_maj_chords = {numeral: [] for numeral in simple_maj_chords.keys()}
        for numeral, notes in simple_maj_chords.items():
            extendednotes = [n for n in notes]
            for note in add:
                extendednotes.append(
                    self.get_add_maj_min_sus_interval(
                        extendednotes[0], note, majmin=majmin
                    )
                )
            for note in dom:
                extendednotes.append(extendednotes[0] + 10)  # only works for dominant7
            extended_maj_chords.update({numeral: extendednotes})
        inversions = {
            "I": [0, 0, 0],
            "i": [0, 0, 0],
            "ii": [0, 0, 0],
            "II": [0, 0, 0],
            "iii": [0, 0, 0],
            "III": [0, 0, 0],
            "IV": [0, 0, 0],
            "iv": [0, 0, 0],
            "V": [0, 0, 0],
            "v": [0, 0, 0],
            "vi": [0, 0, 0],
            "VI": [0, 0, 0],
            "viio": [0, 0, 0],
            "VIIaug": [0, 0, 0],
        }
        if inversion == "open":
            inversions = {
                "I": [-12, 12, 0],
                "i": [-12, 12, 0],
                "ii": [-12, 12, 0],
                "II": [-12, 12, 0],
                "iii": [-12, 0, 0],
                "III": [-12, 0, 0],
                "IV": [-12, 0, 0],
                "iv": [-12, 0, 0],
                "V": [-12, 0, -12],
                "v": [-12, 0, -12],
                "vi": [-12, 12, -12],
                "VI": [-12, 12, -12],
                "viio": [-12, 0, 12],
                "VIIaug": [-12, 0, 12],
            }
        elif inversion == "first":
            inversions = {
                "I": [12, 0, 0],
                "i": [12, 0, 0],
                "ii": [12, 0, 0],
                "II": [12, 0, 0],
                "iii": [12, 0, 0],
                "III": [12, 0, 0],
                "IV": [12, 0, 0],
                "iv": [12, 0, 0],
                "V": [12, 0, 0],
                "v": [12, 0, 0],
                "vi": [12, 0, 0],
                "VI": [12, 0, 0],
                "viio": [12, 0, 0],
                "VIIaug": [12, 0, 0],
            }
        elif inversion == "second":
            inversions = {
                "I": [12, 12, 0],
                "i": [12, 12, 0],
                "ii": [12, 12, 0],
                "II": [12, 12, 0],
                "iii": [12, 12, 0],
                "III": [12, 12, 0],
                "IV": [12, 12, 0],
                "iv": [12, 12, 0],
                "V": [12, 12, 0],
                "v": [12, 12, 0],
                "vi": [12, 12, 0],
                "VI": [12, 12, 0],
                "viio": [12, 12, 0],
                "VIIaug": [12, 12, 0],
            }
        if dom or add:
            extended_inv = {numeral: [] for numeral in inversions.keys()}
            for numeral, change in inversions.items():
                extended_chages = [c for c in change]
                for d in dom:
                    if inversion == "first" or inversion == "second":
                        extended_chages.append(12)
                    elif inversion == "cluster":
                        extended_chages.append(-12)
                    else:
                        extended_chages.append(0)

                for a in add:
                    if inversion == "first" or inversion == "second":
                        extended_chages.append(12)
                    elif inversion == "cluster":
                        extended_chages.append(-12)
                    else:
                        extended_chages.append(0)

                extended_inv.update({numeral: extended_chages})
            if inversion == "cluster":
                cluster_voicings = {}
                for numeral, chords in extended_maj_chords.items():
                    chord = []
                    for note, inv in zip(chords, extended_inv[numeral]):
                        chord.append(note + inv)
                    cluster_voicings.update(
                        {numeral: [chord[0] - 12, chord[1], chord[-1]]}
                    )
                return cluster_voicings
            else:
                return {
                    numeral: [
                        note + inv for note, inv in zip(chords, extended_inv[numeral])
                    ]
                    for numeral, chords in extended_maj_chords.items()
                }
        return {
            numeral: [note + inv for note, inv in zip(chords, inversions[numeral])]
            for numeral, chords in simple_maj_chords.items()
        }

    # c_maj_chords = {
    #     'I':[c_maj["C"],c_maj['E'],c_maj['G']],
    #     "ii":[c_maj["C"]+2,c_maj['E']+2,c_maj['G']+2],
    #     'iii':[c_maj["C"]+4,c_maj['E']+4,c_maj['G']+4],
    #     'IV':[c_maj["C"]+5,c_maj['E']+5,c_maj['G']+5],
    #     'V':[c_maj["C"]+7,c_maj['E']+7,c_maj['G']+7],
    #     'vi':[c_maj["C"]+9,c_maj['E']+9,c_maj['G']+9],
    #     'viio':[c_maj["C"]+11,c_maj['E']+11,c_maj['G']+11],
    # }

    def create_major_progression(
        self, interval_list, key, inversion="closed", filename=""
    ):
        # create your MIDI object
        mf = MIDIFile(1)  # only 1 track
        track = 0  # the only track

        time = 0  # start at the beginning
        mf.addTrackName(track, time, "Sample Track")
        mf.addTempo(track, time, 120)

        # add some notes
        channel = 0
        volume = 100
        duration = 4  # whole measure chords
        maj_chords = self.get_maj_scale_chords(key, inversion)
        interval_list = interval_list.split("-")
        for i in interval_list:
            print(i)
            if "maj" in i and not "min" in i:
                numeral, ext = i.split("maj")
                chord = self.get_maj_scale_chords(
                    key, inversion, add=[int(ext)], majmin="maj"
                )[numeral]
            elif "min" in i and not "maj" in i:
                numeral, ext = i.split("min")
                chord = self.get_maj_scale_chords(
                    key, inversion, add=[int(ext)], majmin="min"
                )[numeral]
            elif "maj" in i and "min" in i:
                chord = maj_chords[i]  # minmaj majmin not supported.
            elif "dom" in i:
                numeral, ext = i.split("dom")
                chord = self.get_maj_scale_chords(key, inversion, dom=[int(ext)])[
                    numeral
                ]
            else:
                chord = maj_chords[i]

            print(chord)
            for note in chord:
                mf.addNote(track, channel, note, time, duration, volume)
            time += 4
        if not filename:
            filename = "-".join(interval_list) + "output.mid"
        with open(filename, "wb") as outf:
            mf.writeFile(outf)
        print(f"wrote to {filename}")


commonprogressions = [
    "I-IV-V-I",
    "I-I-I-I-IVdom7-IVdom7-I-I-Vdom7-IVdom7-I-Vdom7",
    "I-V-vi-IV",
    "iimin7-Vdom7-Imaj7-Imaj7",
    "I-V-vi-iii-IV-I-IV-V",
    "I-vi-IV-V",
    "I-IV-V-IV",
    "vi-IV-I-V",
    "I-IV-ii-V",
    "I-IV-I-V",
    "I-ii-iii-IV-V",
    "I-III-IV-iv",
    "vi-V-IV-III",
    "iimin7-Vdom7-imin7-imin7",
    "Imaj7-vimin7-iimin7-Vdom7",
    "Imaj9-vimin9-iimin9-Vdom7",
    "Imaj7-VImaj7-iimin7-Vdom7",
    "imin7-vimin7-iimin7-Vdom7",
    "iiimin7-VImaj7-iimin7-Vdom7",
    "Imaj7-IVdom7-iiimin7-VIdom7",
]

for p in commonprogressions:
    key = "E"
    cpg = ChordProgressionGenerator(scale_root=key, LOWEST_OCTAVE=3)
    cpg.create_major_progression(
        p,
        key,
        inversion="closed",
        filename=f"closed {p}.mid",
    )
