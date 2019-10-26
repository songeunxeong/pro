class NoteConvertor(object):

    def __init__(self, data, bpm):
        self.data = data.T
        self.bpm = bpm
        self.rate = 44000
        self.block_size = int(rate*60*(1/bpm)*(1/8))
        self.block_length = int(len(data) /block_size)

    def convert(self):
        notes = []
        for i in range(0, self.block_length):
            part = self.data[self.block_size * i: self.block_size * (i+1)]
            pitchs = self.__fourier_transform(part)
            note = []
            for pitch in pitchs:
                note.append(self.__decide_note(pitch))
            notes.append(note)
        
        notes = sum(notes, [])
        song = []
        tempo = 1/32
        

        for i in range(0, len(notes)-1):
            if(notes[i] == notes[i+1]):
                tempo += 1/32
                if (i == len(notes)-2):
                    song.append([notes[i], tempo])
            else:
                song.append([notes[i], tempo])
                tempo = 1/32
                if (i == len(notes)-2):
                    song.append([notes[i+1], tempo])            
        
        for i in range(len(song)):
            song[i][1] = 1/song[i][1]
            
        return song
        

    def __fourier_transform(self, wave_sample):
        size = len(wave_sample)
        k = np.arange(size)

        f0=k*self.rate/size    # double sides frequency range
        f0=f0[range(int(size/2))]

        Y=np.fft.fft(wave_sample)/size        # fft computing and normaliation
        Y=Y[range(int(size/2))]          # single sied frequency range

        amplitude_Hz = 2*abs(Y)
        banks = np.where((amplitude_Hz >= (amplitude_Hz.max() * 0.90)) & (amplitude_Hz > 500))
        pitchs = []
        for bank in banks[0]:
            pitchs.append(f0[bank])
        return pitchs

    def __decide_note(self, pitch):
        if pitch > 33 and pitch <= 34:
            return 'c1'
        elif pitch > 34 and pitch <= 36:
            return 'c#1'
        elif pitch > 36 and pitch <= 38:
            return 'd1'
        elif pitch > 38 and pitch <= 40:
            return 'd#1'
        elif pitch > 40 and pitch <= 42:
            return 'e1'
        elif pitch > 42 and pitch <= 45:
            return 'f1'
        elif pitch > 45 and pitch <= 48:
            return 'f#1'
        elif pitch > 48 and pitch <= 51:
            return 'g1'
        elif pitch > 51 and pitch <= 54:
            return 'g#1'
        elif pitch > 54 and pitch <= 57:
            return 'a1'
        elif pitch > 57 and pitch <= 61:
            return 'a#1'
        elif pitch > 61 and pitch <= 64:
            return 'c2'
        elif pitch > 64 and pitch <= 67:
            return 'c#2'
        elif pitch > 67 and pitch <= 71:
            return 'd2'
        elif pitch > 71 and pitch <= 76:
            return 'd#2'
        elif pitch > 76 and pitch <= 80:
            return 'e2'
        elif pitch > 80 and pitch <= 84:
            return 'f2'
        elif pitch > 84 and pitch <= 90:
            return 'f#2'
        elif pitch > 90 and pitch <= 95:
            return 'g2'
        elif pitch > 95 and pitch <= 101:
            return 'g#2'
        elif pitch > 101 and pitch <= 107:
            return 'a2'
        elif pitch > 107 and pitch <= 114:
            return 'a#2'
        elif pitch > 114 and pitch <= 120:
            return 'b2'
        elif pitch > 127 and pitch <= 135:
            return 'c3'
        elif pitch > 135 and pitch <= 143:
            return 'c#3'
        elif pitch > 143 and pitch <= 152:
            return 'd3'
        elif pitch > 152 and pitch <= 160:
            return 'd#3'
        elif pitch > 160 and pitch <= 170:
            return 'e3'
        elif pitch > 170 and pitch <= 180:
            return 'f3'
        elif pitch > 180 and pitch <= 190:
            return 'g3'
        elif pitch > 190 and pitch <= 214:
            return 'g#3'
        elif pitch > 214 and pitch <= 226:
            return 'a3'
        elif pitch > 226 and pitch <= 240:
            return 'a#3'
        elif pitch > 240 and pitch <= 254:
            return 'b3'
        elif pitch > 254 and pitch <= 270:
            return 'c4'      
        elif pitch > 270 and pitch <= 285:
            return 'c#4'
        elif pitch > 285 and pitch <= 302:
            return 'd4'
        elif pitch > 302 and pitch <= 320:
            return 'd#4'
        elif pitch > 320 and pitch <= 339:
            return 'e4'
        elif pitch > 339 and pitch <= 359:
            return 'f4'
        elif pitch > 359 and pitch <= 381:
            return 'f#4'
        elif pitch > 381 and pitch <= 403:
            return 'g4'
        elif pitch > 403 and pitch <= 427:
            return 'g#4'
        elif pitch > 427 and pitch <= 453:
            return 'a4'
        elif pitch > 453 and pitch <= 480:
            return 'a#4'
        elif pitch > 480 and pitch <= 508:
            return 'b4'
        elif pitch > 508 and pitch <= 538:
            return 'c5'
        elif pitch > 538 and pitch <= 570:
            return 'c#5'
        elif pitch > 570 and pitch <= 604:
            return 'd5'
        elif pitch > 604 and pitch <= 640:
            return 'd#5'
        elif pitch > 640 and pitch <= 678:
            return 'e5'
        elif pitch > 678 and pitch <= 719:
            return 'f5'
        elif pitch > 719 and pitch <= 762:
            return 'f#5'
        elif pitch > 762 and pitch <= 807:
            return 'g5'
        elif pitch > 807 and pitch <= 855:
            return 'g#5'
        elif pitch > 855 and pitch <= 906:
            return 'a5' 
        elif pitch > 906 and pitch <= 960:
            return 'a#5'
        elif pitch > 960 and pitch <= 1482:
            return 'b5'
        elif pitch > 1482 and pitch <= 1077:
            return 'c6'
        elif pitch > 1077 and pitch <= 1142:
            return 'c#6'
        elif pitch > 1142 and pitch <= 1209:
            return 'd6'
        elif pitch > 1209 and pitch <= 1281:
            return 'd#6'
        elif pitch > 1281 and pitch <= 1357:
            return 'e6'
        elif pitch > 1357 and pitch <= 1438:
            return 'f6'
        elif pitch > 1438 and pitch <= 1524:
            return 'f#6'
        elif pitch > 1524 and pitch <= 1614:
            return 'g6'
        elif pitch > 1614 and pitch <= 1710:
            return 'g#6'
        elif pitch > 1710 and pitch <= 1812:
            return 'a6'
        elif pitch > 1812 and pitch <= 1920:
            return 'a#6'
        elif pitch > 1920 and pitch <= 2034:
            return 'b6'
        elif pitch > 2034 and pitch <= 2155:
            return 'c7'
        elif pitch > 2155 and pitch <= 2283:
            return 'c#7'
        elif pitch > 2283 and pitch <= 2419 :
            return 'd7'
        elif pitch > 2419 and pitch <= 2563:
            return 'd#7'
        elif pitch > 2563 and pitch <= 2715:
            return 'e7'
        elif pitch > 2715 and pitch <= 2876:
            return 'f7'
        elif pitch > 2876 and pitch <= 3048:
            return 'f#7'      
        elif pitch > 3048 and pitch <= 3229:
            return 'g7'
        elif pitch > 3229 and pitch <= 3421:
            return 'g#7'
        elif pitch > 3421 and pitch <= 3624:
            return 'a7'
        elif pitch > 3624 and pitch <= 3840:
            return 'a#7'
        elif pitch > 3840 and pitch <= 4000:
            return 'b7'
        else:
            return 'x'
