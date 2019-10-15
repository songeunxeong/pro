import numpy as np
import random



class MatrixBuilder:

    def __init__(self, value_list):
        self.values_added = 0
        self.init_num = value_list
        self.num = {}


        for i in range(0, len(value_list)):
            self.num[value_list[i]] = i

        self.matrix=[[0 for x in range(len(value_list))] for i in range(len(value_list))]

    def add(self, from_value, to_value):

        value = self.num
        self.matrix[value[from_value]][value[to_value]] += 1
        self.values_added = self.values_added + 1

    def next_value(self, from_value):
        value = self.num[from_value]
        value_counts = self.matrix[value]
        value_index = self.choose(value_counts)
        if(value_index < 0):
            raise RuntimeError("Non-existent value selected.")
        else:
            return self.init_num[value_index]

    def choose(self, value_counts):

        counted_sum = 0
        count_sum = sum(value_counts)

        if count_sum == 0:
            return random.randint(0, len(value_counts)-1)
        else:
            selected_count = random.randrange(1, count_sum + 1)
            for index in range(0, len(value_counts)):
                counted_sum += value_counts[index]
                if(counted_sum >= selected_count):
                    return index
        raise RuntimeError("Impossible value selection made. BAD!")
