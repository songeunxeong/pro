import numpy as np


class MarcovMatrix:

    def __init__(self, song=None):
        self.previous_note = None

        if song is not None:
            pitch = np.array(song, dtype=str)[:, 0]
            durations = np.array(song, dtype=str)[:, 1]

            for i, d in enumerate(durations):
                durations[i] = self.float2str(durations[i])

            self.Pitch = MatrixBuilder(np.unique(pitch).tolist())
            self.Dura = MatrixBuilder(np.unique(durations).tolist())


            for note in song:
                self.add(note)

        else:
            self.Pitch = MatrixBuilder(["a", "a#", "b", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#"])
            self.Dura = MatrixBuilder([1, 2, 4, 8, 16])

    def float2str(self, d):
        if float(d) >= 1:
            return '%d' % int(float(d))
        else:
            return '%.2f' % float(d)


    def add(self, to_note):

        to_note = list(to_note)
        to_note[1] = self.float2str(to_note[1])

        if(self.previous_note is None):
            self.previous_note = to_note
            return
        from_note = self.previous_note
        self.Pitch.add(from_note[0], to_note[0])
        self.Dura.add(from_note[1], to_note[1])
        self.previous_note = to_note

    def next_note(self, from_note):
        from_note = list(from_note)
        from_note[1] = self.float2str(from_note[1])

        return [self.Pitch.next_value(from_note[0]), float(self.Dura.next_value(from_note[1]))]
