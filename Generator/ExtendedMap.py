import json

import Generator.DiceState
from Generator.CatanMap import CatanMap


class ExtendedMap(CatanMap):
    def __init__(self):
        super().__init__()
        self.tile = []
        self.tile_dice = []
        self.neighbor_recurrence = {}
        for i in range(30):
            self.tile.append(0)
            self.tile_dice.append(-1)
        self.neighbor_recurrence[0] = []
        self.neighbor_recurrence[1] = [0]
        self.neighbor_recurrence[2] = [1]
        self.neighbor_recurrence[3] = [2]

        self.neighbor_recurrence[4] = [0]
        self.neighbor_recurrence[5] = [4, 0, 1]
        self.neighbor_recurrence[6] = [5, 1, 2]
        self.neighbor_recurrence[7] = [6, 2, 3]
        self.neighbor_recurrence[8] = [7, 3]

        self.neighbor_recurrence[9] = [4]
        self.neighbor_recurrence[10] = [9, 4, 5]
        self.neighbor_recurrence[11] = [10, 5, 6]
        self.neighbor_recurrence[12] = [11, 6, 7]
        self.neighbor_recurrence[13] = [12, 7, 8]
        self.neighbor_recurrence[14] = [13, 8]

        self.neighbor_recurrence[15] = [9]
        self.neighbor_recurrence[16] = [15, 9, 10]
        self.neighbor_recurrence[17] = [16, 10, 11]
        self.neighbor_recurrence[18] = [17, 11, 12]
        self.neighbor_recurrence[19] = [18, 12, 13]
        self.neighbor_recurrence[20] = [19, 13, 14]

        self.neighbor_recurrence[21] = [15, 16]
        self.neighbor_recurrence[22] = [21, 16, 17]
        self.neighbor_recurrence[23] = [22, 17, 18]
        self.neighbor_recurrence[24] = [23, 18, 19]
        self.neighbor_recurrence[25] = [24, 19, 20]

        self.neighbor_recurrence[26] = [21, 22]
        self.neighbor_recurrence[27] = [26, 22, 23]
        self.neighbor_recurrence[28] = [27, 23, 24]
        self.neighbor_recurrence[29] = [28, 24, 25]

        self.resource_pool = {1: 6, 2: 6, 3: 6, 4: 5, 5: 5, 6: 2}
        self.tile_to_name = {0: "none", 1: "LUMB", 2: "WOOL", 3: "GRAI", 4: "OREE", 5: "CLAY", 6: "DESE"}
        self.name_to_tile = {"LUMB": 1, "WOOL": 2, "GRAI": 3, "OREE": 4, "CLAY": 5, "DESE": 6}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
        self.resource_distribution = Generator.DiceState.ExtendedDiceState()
        self.tile_pairs = []
        for i in range(30):
            self.tile_pairs.append([])

    def export(self):
        # returns JSON object representing the map
        export_dictionary = {'type': 'extended', 'tile': []}
        for i in range(30):
            export_dictionary['tile'].append({'index': i, 'resource_type': self.tile_to_name[self.tile[i]],
                                              'dice': self.tile_dice[i]})
        return json.dumps(export_dictionary)
        pass

    def fix_desert(self, number_of_players):
        if number_of_players == 6:
            self.tile[0] = 6
            self.tile_dice[0] = 0
            self.tile[29] = 6
            self.tile_dice[29] = 0

    def build_slots(self):
        # must have only desert placed
        for index in range(1, 30):
            if self.tile[index] == 6:
                continue
            for i in self.neighbor_recurrence[index]:
                if self.tile[i] == 6:
                    continue
                self.tile_pairs[index].append(i)
        for index in range(1, 30):
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

    def generate_map(self, number_of_players):
        try:
            if not self.resource_distribution.completed():
                self.resource_distribution.generate_balanced()
            self.fix_desert(number_of_players)
            self.build_slots()
            for index in range(30):
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
            if e is not None:
                return False
            return True

    def dbg(self):
        print("\t\t\t\t  %4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d" % (
            self.tile_to_name[self.tile[0]], self.tile_dice[0],
            self.tile_to_name[self.tile[1]], self.tile_dice[1],
            self.tile_to_name[self.tile[2]], self.tile_dice[2],
            self.tile_to_name[self.tile[3]], self.tile_dice[3]))

        print("\t\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d" % (
            self.tile_to_name[self.tile[4]], self.tile_dice[4],
            self.tile_to_name[self.tile[5]], self.tile_dice[5],
            self.tile_to_name[self.tile[6]], self.tile_dice[6],
            self.tile_to_name[self.tile[7]], self.tile_dice[7],
            self.tile_to_name[self.tile[8]], self.tile_dice[8]))

        print("\t  %4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d" % (
            self.tile_to_name[self.tile[9]], self.tile_dice[9],
            self.tile_to_name[self.tile[10]], self.tile_dice[10],
            self.tile_to_name[self.tile[11]], self.tile_dice[11],
            self.tile_to_name[self.tile[12]], self.tile_dice[12],
            self.tile_to_name[self.tile[13]], self.tile_dice[13],
            self.tile_to_name[self.tile[14]], self.tile_dice[14]))

        print("%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d" % (
            self.tile_to_name[self.tile[15]], self.tile_dice[15],
            self.tile_to_name[self.tile[16]], self.tile_dice[16],
            self.tile_to_name[self.tile[17]], self.tile_dice[17],
            self.tile_to_name[self.tile[18]], self.tile_dice[18],
            self.tile_to_name[self.tile[19]], self.tile_dice[19],
            self.tile_to_name[self.tile[20]], self.tile_dice[20]))

        print("\t  %4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d" % (
            self.tile_to_name[self.tile[21]], self.tile_dice[21],
            self.tile_to_name[self.tile[22]], self.tile_dice[22],
            self.tile_to_name[self.tile[23]], self.tile_dice[23],
            self.tile_to_name[self.tile[24]], self.tile_dice[24],
            self.tile_to_name[self.tile[25]], self.tile_dice[25]))

        print("\t\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d\t\t%4s%2d" % (
            self.tile_to_name[self.tile[26]], self.tile_dice[26],
            self.tile_to_name[self.tile[27]], self.tile_dice[27],
            self.tile_to_name[self.tile[28]], self.tile_dice[28],
            self.tile_to_name[self.tile[29]], self.tile_dice[29]))
        print()
        print()

    def clear(self):
        self.tile = []
        self.tile_dice = []
        self.neighbor_recurrence = {}
        for i in range(30):
            self.tile.append(0)
            self.tile_dice.append(-1)
        self.neighbor_recurrence[0] = []
        self.neighbor_recurrence[1] = [0]
        self.neighbor_recurrence[2] = [1]
        self.neighbor_recurrence[3] = [2]

        self.neighbor_recurrence[4] = [0]
        self.neighbor_recurrence[5] = [4, 0, 1]
        self.neighbor_recurrence[6] = [5, 1, 2]
        self.neighbor_recurrence[7] = [6, 2, 3]
        self.neighbor_recurrence[8] = [7, 3]

        self.neighbor_recurrence[9] = [4]
        self.neighbor_recurrence[10] = [9, 4, 5]
        self.neighbor_recurrence[11] = [10, 5, 6]
        self.neighbor_recurrence[12] = [11, 6, 7]
        self.neighbor_recurrence[13] = [12, 7, 8]
        self.neighbor_recurrence[14] = [13, 8]

        self.neighbor_recurrence[15] = [9]
        self.neighbor_recurrence[16] = [15, 9, 10]
        self.neighbor_recurrence[17] = [16, 10, 11]
        self.neighbor_recurrence[18] = [17, 11, 12]
        self.neighbor_recurrence[19] = [18, 12, 13]
        self.neighbor_recurrence[20] = [19, 13, 14]

        self.neighbor_recurrence[21] = [15, 16]
        self.neighbor_recurrence[22] = [21, 16, 17]
        self.neighbor_recurrence[23] = [22, 17, 18]
        self.neighbor_recurrence[24] = [23, 18, 19]
        self.neighbor_recurrence[25] = [24, 19, 20]

        self.neighbor_recurrence[26] = [21, 22]
        self.neighbor_recurrence[27] = [26, 22, 23]
        self.neighbor_recurrence[28] = [27, 23, 24]
        self.neighbor_recurrence[29] = [28, 24, 25]

        self.resource_pool = {1: 6, 2: 6, 3: 6, 4: 5, 5: 5, 6: 2}
        self.tile_to_name = {0: "none", 1: "LUMB", 2: "WOOL", 3: "GRAI", 4: "OREE", 5: "CLAY", 6: "DESE"}
        self.name_to_tile = {"LUMB": 1, "WOOL": 2, "GRAI": 3, "OREE": 4, "CLAY": 5, "DESE": 6}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
        self.resource_distribution = Generator.DiceState.ExtendedDiceState()
        self.tile_pairs = []
        for i in range(30):
            self.tile_pairs.append([])
