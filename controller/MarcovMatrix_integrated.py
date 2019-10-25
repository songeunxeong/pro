


class MarcovMatrix:

    def __init__(self, song=None):
        self.previous_note = None
        self.uniq_pitch = []
        self.uniq_durations = []
        self.pitch_index = {}
        self.dura_index = {}
        self.Pitch = [][]
        self.Durations = [][]

        # song = [('c4', 32), ('c4', 16), ..]
        pitch = np.array(song, dtype=str)[:, 0] # ['c4', 'c4', ...]
        durations = np.array(song, dtype=str)[:, 1] # ['32', '16', ...]
        for i, d in enumerate(durations):
            durations[i] = self.float2str(durations[i])
          
        uniq_pitch = np.unique(pitch).tolist() #['c4', 'd4']
        uniq_durations = np.unique(durations).tolist() 
        
        Pitch, pitch_index = self.matrixbuilder(uniq_pitch)
        Durations, dura_index = self.matrixbuilder(uniq_durations)

        for note in song:  # note ('c4', 32)
            self.add(note, pitch_index, dura_index)


    def float2str(self, d):
        if float(d) >= 1:
            return '%d' % int(float(d))
        else:
            return '%.2f' % float(d)

    def matrixbuilder(self, uniq_list):    
        matrix = [][]
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
        Pitch[pitch_index[frome_note[0]]][pitch_index[to_note[0]]] += 1
        Durations[dura_index[from_note[1]]][dura_index[to_note[1]]] += 1
        self.previous_note = to_note

    def next_note(self, from_note):  # frome_note = ['c3', 16]
        from_note = list(from_note)
        from_note[1] = self.float2str(from_note[1])
        
        pitch_indexnum = self.pitch_index[from_note[0]]  # 해당하는 행의 index번호
        dura_indexnum = self.dura_index[from_note[1]]
        
        pitch_row = Pitch[pitch_indexnum]
        dura_row = Durations[dura_indexnum]
        
        pitch_new_index = self.select(pitch_row)
        duration_new_index = self.select(dura_row)
        
        if(pitch_new_index < 0 or duration_new_index < 0):
            raise RuntimeError("impossible selection")
        else 
            return [uniq_pitch[pitch_new_index], float(uniq_durations[duration_new_index])]
        
    def select(self, row):
        
        cur_sum = 0
        all_sum = sum(row)
        
        if all_sum == 0:
            return random.randint(0, len(row)-1)
        else:
            randomly_number = random.randrange(1, all_sum+1)
            for i in range(0, len(row)):
                cur_sum += row[i]
                if(cur_sum >= randomly_number):
                    return i
        raise RuntimeError("impossoble selection")                

        