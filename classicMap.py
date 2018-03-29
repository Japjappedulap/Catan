import numpy

import state
from CatanMap import CatanMap


class SimpleTable(CatanMap):
    def __init__(self):
        super().__init__()
        self.tile = []
        self.tile_dice = []
        self.neighbor_recurrence = {}
        for i in range(19):
            self.tile.append(0)
            self.tile_dice.append(-1)
        self.neighbor_recurrence[0] = []
        self.neighbor_recurrence[1] = [0]
        self.neighbor_recurrence[2] = [1]
        self.neighbor_recurrence[3] = [0]
        self.neighbor_recurrence[4] = [3, 0, 1]
        self.neighbor_recurrence[5] = [4, 1, 2]
        self.neighbor_recurrence[6] = [5, 2]
        self.neighbor_recurrence[7] = [3]
        self.neighbor_recurrence[8] = [7, 3, 4]
        self.neighbor_recurrence[9] = [8, 4, 5]
        self.neighbor_recurrence[10] = [9, 5, 6]
        self.neighbor_recurrence[11] = [10, 6]
        self.neighbor_recurrence[12] = [7, 8]
        self.neighbor_recurrence[13] = [12, 8, 9]
        self.neighbor_recurrence[14] = [13, 9, 10]
        self.neighbor_recurrence[15] = [14, 10, 11]
        self.neighbor_recurrence[16] = [12, 13]
        self.neighbor_recurrence[17] = [16, 13, 14]
        self.neighbor_recurrence[18] = [17, 14, 15]
        self.resource_pool = {1: 4, 2: 4, 3: 4, 4: 3, 5: 3, 6: 1}
        self.tile_to_name = {0: "none", 1: "LUMB", 2: "WOOL", 3: "GRAI", 4: "OREE", 5: "CLAY", 6: "DESE"}
        self.name_to_tile = {"LUMB": 1, "WOOL": 2, "GRAI": 3, "OREE": 4, "CLAY": 5, "DESE": 6}
        self.dices_available = {2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 1}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
        self.resource_distribution = state.ClassicState()
        self.tile_pairs = []
        for i in range(19):
            self.tile_pairs.append([])

    def fix_desert(self, number_of_players):
        if number_of_players == 4:
            self.tile[2] = 6
            self.tile_dice[2] = 0
        elif number_of_players == 3:
            prob_for_edge = 1 / 10
            prob_for_corner = 6 / 10
            prob_for_center = 1
            result = numpy.random.uniform(low=0, high=1)
            if 0 <= result <= prob_for_edge:
                self.tile[6] = 6
                self.tile_dice[6] = 0
            elif prob_for_edge <= result <= prob_for_corner:
                self.tile[2] = 6
                self.tile_dice[2] = 0
            elif prob_for_corner <= result <= prob_for_center:
                self.tile[9] = 6
                self.tile_dice[9] = 0
        elif number_of_players == 2:
            prob_for_edge = 2 / 10
            prob_for_corner = 5 / 10
            prob_for_center = 8 / 10
            prob_for_inner = 1
            result = numpy.random.uniform(low=0, high=1)
            if 0 <= result <= prob_for_edge:
                self.tile[1] = 6
                self.tile_dice[1] = 0
            elif prob_for_edge <= result <= prob_for_corner:
                self.tile[0] = 6
                self.tile_dice[0] = 0
            elif prob_for_corner <= result <= prob_for_center:
                self.tile[9] = 6
                self.tile_dice[9] = 0
            elif prob_for_center <= result <= prob_for_inner:
                self.tile[4] = 6
                self.tile_dice[4] = 0
        #  for dev
        elif number_of_players == 5:
            self.tile[0] = 6
            self.tile_dice[0] = 0
        elif number_of_players == 6:
            self.tile[9] = 6
            self.tile_dice[9] = 0
        elif number_of_players == 7:
            self.tile[1] = 6
            self.tile_dice[1] = 0
        elif number_of_players == 8:
            self.tile[4] = 6
            self.tile_dice[4] = 0

    def build_slots(self):
        # must have only desert placed
        for index in range(1, 19):
            if self.tile[index] == 6:
                continue
            for i in self.neighbor_recurrence[index]:
                if self.tile[i] == 6:
                    continue
                self.tile_pairs[index].append(i)
        for index in range(1, 19):
            if self.tile[index] == 6:
                continue
            for i in self.neighbor_recurrence[index]:
                if self.tile[i] == 6:
                    continue
                for j in self.neighbor_recurrence[index]:
                    if self.tile[j] == 6 or j <= i:
                        continue
                    if self.are_neighbor(i, j):
                        self.tile_pairs[index].append((i, j))
                        if i in self.tile_pairs[index]:
                            self.tile_pairs[index].remove(i)
                        if j in self.tile_pairs[index]:
                            self.tile_pairs[index].remove(j)

        # for i in range(19):
        #     print(i, self.__tile_pairs[i])
        pass

    def generate_map(self, number_of_players):
        try:
            if not self.resource_distribution.completed():
                self.resource_distribution.generate_balanced()
            self.fix_desert(number_of_players)

            self.build_slots()
            for index in range(19):
                # print("   @@@@ configuration:", self.__resource_distribution.configuration)
                if self.tile[index] == 6:
                    continue
                # print("len:", len(self.__tile_pairs[index]), self.__tile_pairs[index])

                if len(self.tile_pairs[index]) == 0:
                    next_tile_resource_and_dice = self.generate_next_tile_possibilities_single()
                    # print("single:", next_tile_resource_and_dice)
                    self.fix_tile(index, next_tile_resource_and_dice[0], next_tile_resource_and_dice[1])

                elif len(self.tile_pairs[index]) == 1 \
                        and isinstance(self.tile_pairs[index][0], int) \
                        and self.tile[self.tile_pairs[index][0]] != 0:
                    next_tile_resource_and_dice = self.generate_next_tile_possibilities_pair(
                        self.tile_pairs[index][0])
                    # print("pair:", next_tile_resource_and_dice)
                    self.fix_tile(index, next_tile_resource_and_dice[0], next_tile_resource_and_dice[1])

                elif len(self.tile_pairs[index]) == 1 \
                        and isinstance(self.tile_pairs[index][0], tuple) \
                        and self.tile[self.tile_pairs[index][0][0]] != 0 \
                        and self.tile[self.tile_pairs[index][0][1]] != 0:
                    next_tile_resource_and_dice = self.generate_next_tile_possibilities_closed_triple(
                        self.tile_pairs[index][0][0],
                        self.tile_pairs[index][0][1])
                    # print("closed triple:", next_tile_resource_and_dice)
                    self.fix_tile(index, next_tile_resource_and_dice[0], next_tile_resource_and_dice[1])

                elif len(self.tile_pairs[index]) == 2 \
                        and isinstance(self.tile_pairs[index][0], int) \
                        and isinstance(self.tile_pairs[index][1], int) \
                        and self.tile[self.tile_pairs[index][0]] != 0 \
                        and self.tile[self.tile_pairs[index][1]] != 0:
                    next_tile_resource_and_dice = self.generate_next_tile_possibilities_scattered_triple(
                        self.tile_pairs[index][0],
                        self.tile_pairs[index][1])
                    # print("scattered triple:", next_tile_resource_and_dice)
                    self.fix_tile(index, next_tile_resource_and_dice[0], next_tile_resource_and_dice[1])

                elif len(self.tile_pairs[index]) == 2 \
                        and isinstance(self.tile_pairs[index][0], tuple) \
                        and isinstance(self.tile_pairs[index][1], tuple):
                    unique = []
                    for i in self.tile_pairs[index]:
                        for j in i:
                            unique.append(j)
                    unique = tuple(sorted(set(unique)))
                    next_tile_resource_and_dice = self.generate_next_tile_possibilities_quad(
                        unique[0],
                        unique[1],
                        unique[2])
                    # print("quad:", next_tile_resource_and_dice)
                    self.fix_tile(index, next_tile_resource_and_dice[0], next_tile_resource_and_dice[1])
                # print()
                # print()
                # print()
            return True
        except Exception as e:
            # print("failed:", e)
            return False

    def rotate(self):
        save0 = self.tile[0]
        save1 = self.tile[1]
        save2 = self.tile[4]
        self.tile[0] = self.tile[7]
        self.tile[1] = self.tile[3]
        self.tile[4] = self.tile[8]
        self.tile[7] = self.tile[16]
        self.tile[3] = self.tile[12]
        self.tile[8] = self.tile[13]
        self.tile[16] = self.tile[18]
        self.tile[12] = self.tile[17]
        self.tile[13] = self.tile[14]
        self.tile[18] = self.tile[11]
        self.tile[17] = self.tile[15]
        self.tile[14] = self.tile[10]
        self.tile[11] = self.tile[2]
        self.tile[15] = self.tile[6]
        self.tile[10] = self.tile[5]
        self.tile[2] = save0
        self.tile[6] = save1
        self.tile[5] = save2
        save_dice0 = self.tile_dice[0]
        save_dice1 = self.tile_dice[1]
        save_dice2 = self.tile_dice[4]
        self.tile_dice[0] = self.tile_dice[7]
        self.tile_dice[1] = self.tile_dice[3]
        self.tile_dice[4] = self.tile_dice[8]
        self.tile_dice[7] = self.tile_dice[16]
        self.tile_dice[3] = self.tile_dice[12]
        self.tile_dice[8] = self.tile_dice[13]
        self.tile_dice[16] = self.tile_dice[18]
        self.tile_dice[12] = self.tile_dice[17]
        self.tile_dice[13] = self.tile_dice[14]
        self.tile_dice[18] = self.tile_dice[11]
        self.tile_dice[17] = self.tile_dice[15]
        self.tile_dice[14] = self.tile_dice[10]
        self.tile_dice[11] = self.tile_dice[2]
        self.tile_dice[15] = self.tile_dice[6]
        self.tile_dice[10] = self.tile_dice[5]
        self.tile_dice[2] = save_dice0
        self.tile_dice[6] = save_dice1
        self.tile_dice[5] = save_dice2

    def dbg(self):
        print("\t\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t" % (
            self.tile_to_name[self.tile[0]], self.tile_dice[0],
            self.tile_to_name[self.tile[1]], self.tile_dice[1],
            self.tile_to_name[self.tile[2]], self.tile_dice[2]))

        print("\t  %4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t" % (
            self.tile_to_name[self.tile[3]], self.tile_dice[3],
            self.tile_to_name[self.tile[4]], self.tile_dice[4],
            self.tile_to_name[self.tile[5]], self.tile_dice[5],
            self.tile_to_name[self.tile[6]], self.tile_dice[6]))

        print("%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t" % (
            self.tile_to_name[self.tile[7]], self.tile_dice[7],
            self.tile_to_name[self.tile[8]], self.tile_dice[8],
            self.tile_to_name[self.tile[9]], self.tile_dice[9],
            self.tile_to_name[self.tile[10]], self.tile_dice[10],
            self.tile_to_name[self.tile[11]], self.tile_dice[11]))

        print("\t  %4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t" % (
            self.tile_to_name[self.tile[12]], self.tile_dice[12],
            self.tile_to_name[self.tile[13]], self.tile_dice[13],
            self.tile_to_name[self.tile[14]], self.tile_dice[14],
            self.tile_to_name[self.tile[15]], self.tile_dice[15]))

        print("\t\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t" % (
            self.tile_to_name[self.tile[16]], self.tile_dice[16],
            self.tile_to_name[self.tile[17]], self.tile_dice[17],
            self.tile_to_name[self.tile[18]], self.tile_dice[18]))
        print()
        print()
