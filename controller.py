from pyknon.genmidi import Midi
from pyknon.music import NoteSeq, Note, Rest
import numpy as np
import random

class NoteTempoConvertor(object):

    def __init__(self, data, bpm, sr):
        self.data = data.T[0]
        self.bpm = bpm
        self.rate = sr
        self.block_size = int(self.rate*60*(1/self.bpm)*(1/8))
        self.block_length = int(len(self.data)/self.block_size)

    def convert(self):
        notes = [] # 한 block에서 두 개 이상 추출되는거 제거 후 
        multiple_notes = [] # 한 block에서 두 개 이상 추출되는거 제거하기 전 ntoes
        for i in range(0, self.block_length):
            part = self.data[self.block_size * i: self.block_size * (i+1)]
            pitchs = self.__fourier_transform(part)
            note = []
            if pitchs:
                for pitch in pitchs:
                    note.append(self.__decide_note(pitch))
            else:
                note.append('r')
            multiple_notes.append(note)
            
            # 한 block 에서 두 개 이상 주파수 추출될 때 하나로
            for i in range(len(multiple_notes)-2):
                flow0 = multiple_notes[i]
                flow1 = multiple_notes[i+1]
                flow2 = multiple_notes[i+2]
                
                # 두 개 이상 주파수 추출되었는지 확인
                if(len(flow1)>=2) :
                    for j in range(len(flow1)):
                        # 앞 음정과 같으면 선택
                        if [flow1[j]] == flow0:
                            flow = flow1[j]
                            break
                        # 뒤 음정과 같으면 선택
                        if [flow1[j]] == flow2:
                            flow = flow1[j]
                            break
                        # 앞 뒤 음정과 다 다르면 일단 빈음처리 
                        if j == (len(flow1)-1):
                            flow = 'r'
                    notes.append([flow])
                else:
                    flow = flow1
                    notes.append(flow)
            
        notes = sum(notes, [])
        # 3개 연속 음정 추출 되는 것 중 옥타브 2 이상 차이 제거
        notes = self.remove_note(notes)
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
        # 가청주파수 범위 벗어나는거 제거함
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
        elif pitch > 4000 and pitch <= 4310:
            return 'c8'
        elif pitch > 4310 and pitch <= 4567:
            return 'c#8'
        elif pitch > 4567 and pitch <= 4838:
            return 'd8'
        elif pitch > 4838 and pitch <= 5126:
            return 'd#8'
        elif pitch > 5126 and pitch <= 5431:
            return 'e8'
        elif pitch > 5431 and pitch <= 5754:
            return 'f8'
        elif pitch > 5754 and pitch <= 6096:
            return 'f#8'
        elif pitch > 6096 and pitch <= 6458:
            return 'g8'
        elif pitch > 6458 and pitch <= 6842:
            return 'g#8'
        elif pitch > 6842 and pitch <= 7249:
            return 'a8'
        elif pitch > 7249 and pitch <= 7680:
            return 'a#8'
        elif pitch > 7680 and pitch <= 8137:
            return 'b8'
        elif pitch > 8137 and pitch <= 8621:
            return 'c9'
        elif pitch > 8621 and pitch <= 9134:
            return 'c#9'
        elif pitch > 9134 and pitch <= 9677:
            return 'd9'
        elif pitch > 9677 and pitch <= 10252:
            return 'd#9'
        elif pitch > 10252 and pitch <= 10862:
            return 'e9'
        elif pitch > 10862 and pitch <= 11507:
            return 'f9'
        elif pitch > 11507 and pitch <= 12192:
            return 'f#9'
        elif pitch > 12192 and pitch <= 12917:
            return 'g9'
        elif pitch > 12917 and pitch <= 13685:
            return 'g#9'
        elif pitch > 13685 and pitch <= 14499:
            return 'a9'
        elif pitch > 14499 and pitch <= 15361:
            return 'a#9'
        elif pitch > 15361 and pitch <= 16744:
            return 'b9'
        else:
            return 'r'
        
    def remove_note(self, notes):
        note_names = 'c c# d d# e f f# g g# a a# b'.split()
#        octav10 = {'c10', 'c#10', 'd10', 'd#10', 'e10', 'f10', 'f#10', 'g10', 'g#10', 'a10', 'a#10' ,'b10'}
        octavs = []
        remov = []
        octav = 0
        
        # 옥타브 차이 계산 하기 위해 notes의 옥타브만 octavs에 저장
        for note in notes:
            if note=='r':
                octavs.append('r')
#            elif {note}.issubset(octav10):
#                octav = int(note[-2:])
#                octavs.append(octav)
            else:
                octav = int(note[-1:])
                octavs.append(octav)
        
        # r은 계산할 필요 없으므로 int형만 꺼내와서
        # 앞뒤 음정과 옥타브 2이상 차이나면 잡음일 확률 큼, 제거할 index remov에 저장 
        for x in range(len(octavs)-2):
            if((type(octavs[x]) == int)
              and (type(octavs[x+1]) == int)
              and (type(octavs[x+2]) == int)):
                if((abs(octavs[x]-octavs[x+1]) >= 2)
                  and (abs(octavs[x+1]-octavs[x+2]) >= 2)):
                    remov.append(x+1)
                    
        # 제거 과정
        if remov:
            for x in range(len(remov)):
                # 제거되는 수만큼 index에서 빼줌
                remov[x] -= x
                del notes[remov[x]]
            return notes
        else:
            return notes

class MarcovMatrix:

    def __init__(self, song=None):
        self.previous_note = None
        self.uniq_song = []
        self.uniq_pitch = []
        self.uniq_durations = []
        self.pitch_index = {}
        self.dura_index = {}
        self.Pitch = []
        self.Durations = []

        # song = [('c4', 32), ('c4', 16), ..]
        pitch = np.array(song, dtype=str)[:, 0] # ['c4', 'c4', ...]
        durations = np.array(song, dtype=str)[:, 1] # ['32', '16', ...]
        for i, d in enumerate(durations):
            durations[i] = self.float2str(durations[i])


        # uniq_song은 start_note 추출
        self.uniq_song = np.unique(song, axis=0).tolist() # [('c4', 16)]
        self.uniq_pitch = np.unique(pitch).tolist() # ['c4', 'd4']
        self.uniq_durations = np.unique(durations).tolist()

        self.Pitch, self.pitch_index = self.matrixbuilder(self.uniq_pitch)
        self.Durations, self.dura_index = self.matrixbuilder(self.uniq_durations)

        for note in song:  # note ('c4', 32)
            self.add(note, self.pitch_index, self.dura_index)


    def float2str(self, d):
        if float(d) >= 1:
            return '%d' % int(float(d))
        else:
            return '%.2f' % float(d)

    def matrixbuilder(self, uniq_list):
        matrix = []
        index = {}

        for i in range(0, len(uniq_list)):
            index[uniq_list[i]] = i   # index = {'c4' : 0, 'd4' : 1, ...}

        matrix = [[0 for x in range(len(uniq_list))] for i in range(len(uniq_list))]

        return matrix, index

    def add(self, to_note, pitch_index, dura_index):  # to_note = ('c4', 16)

        to_note = list(to_note)
        to_note[1] = self.float2str(to_note[1])

        if(self.previous_note is None):
            self.previous_note = to_note
            return

        from_note = self.previous_note
         # pitch_index = {'c4' : 0, 'd4' : 1, ...}
        self.Pitch[self.pitch_index[from_note[0]]][self.pitch_index[to_note[0]]] += 1
        self.Durations[self.dura_index[from_note[1]]][self.dura_index[to_note[1]]] += 1
        self.previous_note = to_note

    def next_note(self, from_note):  # frome_note = ['c3', 16]
        from_note = list(from_note)
        from_note[1] = self.float2str(from_note[1])

        pitch_rowindex = self.pitch_index[from_note[0]]  # 해당하는 행의 index번호
        dura_rowindex = self.dura_index[from_note[1]]

        pitch_rowindex = self.same_note_check(pitch_rowindex, pitch=True)  # 한 음정 반복되는 오류 검사
        dura_rowindex = self.same_note_check(dura_rowindex, pitch=False)

        pitch_row = self.Pitch[pitch_rowindex]
        dura_row = self.Durations[dura_rowindex]

        pitch_new_ = self.select(pitch_row)
        duration_new_ = self.select(dura_row)

        if(pitch_new_ < 0 or duration_new_ < 0):
            raise RuntimeError("impossible selection")
        else:
            return [self.uniq_pitch[pitch_new_], float(self.uniq_durations[duration_new_])]

    def select(self, row):

        cur_sum = 0
        all_sum = sum(row)

        if all_sum == 0:
            return random.randrange(0, len(row))
        else:
            randomly_number = random.randrange(1, all_sum+1)
            for i in range(0, len(row)):
                cur_sum += row[i]
                if(cur_sum >= randomly_number):
                    return i
        raise RuntimeError("impossoble selection")


    def same_note_check(self, rowindex, pitch=True):
        check = 0
        test_index = rowindex

        if pitch==True:

            while True:
                for i in range(len(self.uniq_pitch)):
                    if self.Pitch[test_index][i]==0:
                        check += 1
            # check가 전체길이-1과 같으면 행렬요소값이 하나만 존재하고 나머지는 0
                if check == (len(self.uniq_pitch)-1):
                    test_index = random.randrange(0, len(self.uniq_pitch))
                    continue
                else:
                    return test_index
        else:
              while True:
                for i in range(len(self.uniq_durations)):
                    if self.Durations[test_index][i]==0:
                        check += 1
            # check가 전체길이-1과 같으면 행렬요소값이 하나만 존재하고 나머지는 0
                if check == (len(self.uniq_durations)-1):
                    test_index = random.randrange(0, len(self.uniq_durations))
                    continue
                else:
                    return test_index

class MakeMidi:

    def __init__(self, song, bpm, path):
        self.song = song
        self.bpm = bpm
        self.path = path

    def makemidi(self):
        note_names = 'c c# d d# e f f# g g# a a# b'.split()
        octav10 = {'c10', 'c#10', 'd10', 'd#10', 'e10', 'f10', 'f#10', 'g10', 'g#10', 'a10', 'a#10' ,'b10'}

        result = NoteSeq()
        for s in self.song:
            duration = 1. / s[1]

            if s[0] == 'r':
                result.append(Rest(dur=duration))
            elif {s[0]}.issubset(octav10):
                md = s[0][:-2]
                octave = int(s[0][-2:]) + 1
                note_number = note_names.index(md)
                result.append(Note(note_number, octave=octave, dur=duration))
            else:
                md = s[0][:-1]
                octave = int(s[0][-1]) + 1
                note_number = note_names.index(md)
                result.append(Note(note_number, octave=octave, dur=duration))

        midi = Midi(number_tracks=1, tempo=self.bpm)
        midi.seq_notes(result, track=0)
        midi.write(self.path)
