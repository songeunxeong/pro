# music sheet 추가

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
        self.musicsheet_song = None

    def convert(self):

        multiple_notes = [] # 한 block에서 두 개 이상 추출되는거 제거하기 전 ntoes
        for i in range(0, self.block_length):
            part = self.data[self.block_size * i: self.block_size * (i+1)]
            pitchs = self.__fourier_transform(part)
            note = []
            if pitchs:
                for pitch in pitchs:
                    note.append(self.__decide_basic_note(pitch))
            else:
                note.append('r')
            multiple_notes.append(note)

        # 한 block 에서 두 개 이상 주파수 추출될 때 하나로
        notes = self.to_notes(multiple_notes)
        notes = sum(notes, [])
        # 3개 연속 음정 추출 되는 것 중 옥타브 2 이상 차이 제거
        octav_removed_notes = self.remove_octav_note(notes)
        # 음정 길이 추가
        song = []
        sheet = []
        score = 1/8
        tempo = 1/32
        for i in range(0, len(octav_removed_notes)-1):
            if(octav_removed_notes[i] == octav_removed_notes[i+1]):
                tempo += 1/32
                score += 1/8
                if (i == len(octav_removed_notes)-2):
                    song.append([octav_removed_notes[i], tempo])
                    sheet.append([octav_removed_notes[i], score])
            else:
                song.append([octav_removed_notes[i], tempo])
                sheet.append([octav_removed_notes[i], score])
                tempo = 1/32
                score = 1/8
                if (i == len(octav_removed_notes)-2):
                    song.append([octav_removed_notes[i+1], tempo])
                    sheet.append([octav_removed_notes[i+1], score])

        #이상음 변환
        noise_removed_song = self.remov_noise_song(song)
        sheet_song = self.remov_noise_song(sheet)
        # 추가
        self.musicsheet_song = sheet_song

        # midimakefile 음정길이 역수로
        for i in range(len(noise_removed_song)):
            noise_removed_song[i][1] = 1/noise_removed_song[i][1]

        return noise_removed_song

    def __fourier_transform(self, wave_sample):
        size = len(wave_sample)
        k = np.arange(size)

        f0=k*self.rate/size    # double sides frequency range
        f0=f0[range(int(size/2))]

        Y=np.fft.fft(wave_sample)/size        # fft computing and normaliation
        Y=Y[range(int(size/2))]          # single sied frequency range

        amplitude_Hz = 2*abs(Y)
        # 진폭 기준 조정**
        banks = np.where((amplitude_Hz >= (amplitude_Hz.max() * 0.90)) & (amplitude_Hz > 5000))
        pitchs = []
        for bank in banks[0]:
            pitchs.append(f0[bank])
        return pitchs

    def __decide_basic_note(self, pitch):
        # 샵, 플랫은 잡음인 경우 많아서 제거함
        # 가청주파수 범위 벗어나는거 제거함
        if pitch > 33 and pitch <= 35:
            return 'c1'
        elif pitch > 35 and pitch <= 39:
            return 'd1'
        elif pitch > 39 and pitch <= 42.5:
            return 'e1'
        elif pitch > 42.5 and pitch <= 46.5:
            return 'f1'
        elif pitch > 46.5 and pitch <= 52:
            return 'g1'
        elif pitch > 52 and pitch <= 58:
            return 'a1'
        elif pitch > 58 and pitch <= 63:
            return 'b1'
        elif pitch > 63 and pitch <= 69:
            return 'c2'
        elif pitch > 69 and pitch <= 78:
            return 'd2'
        elif pitch > 78 and pitch <= 85:
            return 'e2'
        elif pitch > 85 and pitch <= 93:
            return 'f2'
        elif pitch > 93 and pitch <= 104:
            return 'g2'
        elif pitch > 104 and pitch <= 117:
            return 'a2'
        elif pitch > 117 and pitch <= 127:
            return 'b2'
        elif pitch > 127 and pitch <= 139:
            return 'c3'
        elif pitch > 139 and pitch <= 156:
            return 'd3'
        elif pitch > 156 and pitch <= 170:
            return 'e3'
        elif pitch > 170 and pitch <= 186:
            return 'f3'
        elif pitch > 186 and pitch <= 208:
            return 'g3'
        elif pitch > 208 and pitch <= 234:
            return 'a3'
        elif pitch > 234 and pitch <= 255:
            return 'b3'
        elif pitch > 255 and pitch <= 278:
            return 'c4'
        elif pitch > 278 and pitch <= 312:
            return 'd4'
        elif pitch > 312 and pitch <= 340:
            return 'e4'
        elif pitch > 340 and pitch <= 371:
            return 'f4'
        elif pitch > 371 and pitch <= 416:
            return 'g4'
        elif pitch > 427 and pitch <= 467:
            return 'a4'
        elif pitch > 480 and pitch <= 508:
            return 'b4'
        elif pitch > 508 and pitch <= 555:
            return 'c5'
        elif pitch > 555 and pitch <= 623:
            return 'd5'
        elif pitch > 623 and pitch <= 679:
            return 'e5'
        elif pitch > 679 and pitch <= 741:
            return 'f5'
        elif pitch > 741 and pitch <= 832:
            return 'g5'
        elif pitch > 832 and pitch <= 934:
            return 'a5'
        elif pitch > 934 and pitch <= 1018:
            return 'b5'
        elif pitch > 1018 and pitch <= 1111:
            return 'c6'
        elif pitch > 1111 and pitch <= 1246:
            return 'd6'
        elif pitch > 1246 and pitch <= 1357:
            return 'e6'
        elif pitch > 1357 and pitch <= 1482:
            return 'f6'
        elif pitch > 1482 and pitch <= 1664:
            return 'g6'
        elif pitch > 1664 and pitch <= 1868:
            return 'a6'
        elif pitch > 1868 and pitch <= 2034:
            return 'b6'
        elif pitch > 2034 and pitch <= 2221:
            return 'c7'
        elif pitch > 2221 and pitch <= 2493 :
            return 'd7'
        elif pitch > 2493 and pitch <= 2715:
            return 'e7'
        elif pitch > 2715 and pitch <= 2965:
            return 'f7'
        elif pitch > 2965 and pitch <= 3328:
            return 'g7'
        elif pitch > 3328 and pitch <= 3735:
            return 'a7'
        elif pitch > 3735 and pitch <= 4068:
            return 'b7'
        elif pitch > 4068 and pitch <= 4442:
            return 'c8'
        elif pitch > 4442 and pitch <= 4986:
            return 'd8'
        elif pitch > 4986 and pitch <= 5431:
            return 'e8'
        elif pitch > 5431 and pitch <= 5930:
            return 'f8'
        elif pitch > 5930 and pitch <= 6656:
            return 'g8'
        elif pitch > 6656 and pitch <= 7471:
            return 'a8'
        elif pitch > 7471 and pitch <= 8137:
            return 'b8'
        elif pitch > 8137 and pitch <= 8884:
            return 'c9'
        elif pitch > 8884 and pitch <= 9972:
            return 'd9'
        elif pitch > 9972 and pitch <= 10862:
            return 'e9'
        elif pitch > 10862 and pitch <= 11859:
            return 'f9'
        elif pitch > 11859 and pitch <= 13312:
            return 'g9'
        elif pitch > 13312 and pitch <= 14942:
            return 'a9'
        elif pitch > 14942 and pitch <= 16744:
            return 'b9'
        else:
            return 'r'

    def to_notes(self, multiple_notes):

        notes = []
        flow0 = multiple_notes[0]
        notes.append(flow0)
        for i in range(1, len(multiple_notes)-1):
            flow = ''
            flow1 = multiple_notes[i]
            flow2 = multiple_notes[i+1]

            # 두 개 이상 주파수 추출되었는지 확인
            if(len(flow1)>=2) :
                for j in range(len(flow1)):
                    # 앞 음정과 같으면 선택
                    if [flow1[j]] == flow0:
                        flow = flow1[j]
                        break
                    # 뒤 음정과 같으면 선택
                    # 뒤 음정이 두개 이상일 수 있음
                    if len(flow2)>=2:
                        for k in range(len(flow2)):
                            if [flow1[j]] == [flow2[k]]:
                                flow = flow1[j]
                                break
                        # 뒤 음정 중 같은게 있어서 flow에 할당되면 반복문 탈출
                        if flow==flow1[j]:
                            break
                    if len(flow2)==1:
                        if [flow1[j]] == flow2:
                            flow = flow1[j]
                            break
                    # 앞 뒤 음정과 다 다르면 일단 빈음처리
                    if j == (len(flow1)-1):
                        flow = 'r'
                notes.append([flow])
                # 앞 음정flow0 notes에 추가된 flow로
                flow0 = flow
            else:
                flow = flow1
                notes.append(flow)
                # 앞 음정flow0 notes에 추가된 flow로
                flow0 = flow

        return notes

    def remove_octav_note(self, notes):
        note_names = 'c c# d d# e f f# g g# a a# b'.split()
        octavs = []
        remov = []
        octav = 0

        # 옥타브 차이 계산 하기 위해 notes의 옥타브만 octavs에 저장
        for note in notes:
            if note=='r':
                octavs.append('r')
            else:
                octav = int(note[-1:])
                octavs.append(octav)

        # r은 계산할 필요 없으므로 int형만 꺼내와서
        # 앞뒤 음정과 옥타브 2이상 차이나면 잡음일 확률 큼, 제거할 index remov에 저장
        for x in range(len(octavs)-2):
            if ((type(octavs[x]) == int)
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

    def remov_noise_song(self, song):

        remov=[]
        for i in range(len(song)-2):
            flow0 = song[i][0]
            flow1 = song[i+1][0]
            flow2 = song[i+2][0]

            if flow0==flow2 and flow1!=flow0 :
                if song[i+1][1] <= 3/32:
                    song[i+1][0] = flow0
            return song

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
                    # 행렬요소 값의 행과 열이 같은 인덱스인지 확인
                    for i in range(len(self.uniq_pitch)):
                        if (self.Pitch[test_index][i]==1) and (test_index==i):
                            test_index = random.randrange(0, len(self.uniq_pitch))
                            break
                        else:
                            return test_index
                else:
                    return test_index
        else:
              while True:
                for i in range(len(self.uniq_durations)):
                    if self.Durations[test_index][i]==0:
                        check += 1
            # check가 전체길이-1과 같으면 행렬요소값이 하나만 존재하고 나머지는 0
                if check == (len(self.uniq_durations)-1):
                    # 행렬요소 값의 행과 열이 같은 인덱스인지 확인
                    for i in range(len(self.uniq_durations)):
                        if (self.Durations[test_index][i]==1) and (test_index==i):
                            test_index = random.randrange(0, len(self.uniq_durations))
                            break
                        else:
                            return test_index
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
