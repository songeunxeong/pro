from pyknon.genmidi import Midi
from pyknon.music import NoteSeq, Note, Rest

class MakeMidi:
    
    def __init__(self, song, bpm, path):
        self.song = song
        self.bpm = bpm
        self.path = path
                
    def makemidi(self):
        note_names = 'c c# d d# e f f# g g# a a# b'.split()

        result = NoteSeq()
        for s in self.song:
            duration = 1. / s[1]

            if s[0].lower() == 'r':
                result.append(Rest(dur=duration))
            else:
                pitch = s[0][:-1]
                octave = int(s[0][-1]) + 1
                pitch_number = note_names.index(pitch.lower())
                result.append(Note(pitch_number, octave=octave, dur=duration))
            
        midi = Midi(number_tracks=1, tempo=self.bpm)
        midi.seq_notes(result, track=0)
        midi.write(self.path)      
