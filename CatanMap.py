import numpy


class CatanMap:
    triple_coefficient = [9, 10]
    pair_coefficient = [4, 8]
    pair_peak = pair_coefficient[0] + pair_coefficient[1] / 2
    triple_peak = triple_coefficient[0] + triple_coefficient[1] / 2

    def __init__(self):
        self.tile = []
        self.tile_dice = []
        self.neighbor_recurrence = {}
        self.resource_distribution = None
        self.tile_pairs = []
        self.tile_to_name = {0: "none", 1: "LUMB", 2: "WOOL", 3: "GRAI", 4: "OREE", 5: "CLAY", 6: "DESE"}
        self.name_to_tile = {"LUMB": 1, "WOOL": 2, "GRAI": 3, "OREE": 4, "CLAY": 5, "DESE": 6}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}

    def fix_tile(self, index, resource, dice):
        # print("fixing tile:", index, resource, dice)
        self.tile[index] = resource
        self.tile_dice[index] = dice
        self.resource_distribution.remove_resource(resource, dice)

    def get_resource_distribution(self):
        return self.resource_distribution

    def no_identic_neighbours(self):
        for i in self.neighbor_recurrence:
            for j in self.neighbor_recurrence[i]:
                if self.tile[j] == self.tile[i]:
                    return False
        return True

    def are_neighbor(self, tile1, tile2):
        for i in self.neighbor_recurrence[tile1]:
            if i == tile2:
                return True
        for i in self.neighbor_recurrence[tile2]:
            if i == tile1:
                return True
        return False

    def generate_dices(self):
        self.resource_distribution.generate_balanced()

    def generate_next_tile_possibilities_single(self):
        try:
            candidates = []
            prob = []
            for i in self.resource_distribution.configuration:
                for j in self.resource_distribution.configuration[i]:
                    candidates.append((i, j))
                    coefficient = len(self.resource_distribution.configuration[i])
                    coefficient += self.dice_probability[j]
                    prob.append(coefficient)

            # print("pool of choice", len(candidates))
            indexes = []
            total = sum(prob)
            # print("total sum of coefficients:", total)
            # print(candidates)
            # print(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
            # print(candidates[numpy.asscalar(result[0])])
            return candidates[numpy.asscalar(result[0])]
        except Exception:
            raise Exception

    def generate_next_tile_possibilities_pair(self, index):
        try:
            tile_resource = self.tile[index]  # already set
            tile_dice = self.tile_dice[index]  # already set

            candidates = []
            prob = []
            for i in self.resource_distribution.configuration:
                for j in self.resource_distribution.configuration[i]:
                    if self.pair_coefficient[0] <= self.dice_probability[tile_dice] + self.dice_probability[j] <= \
                            self.pair_coefficient[1]:
                        coefficient = 8
                        candidates.append((i, j))
                        coefficient += len(self.resource_distribution.configuration[i])
                        coefficient += self.dice_probability[j]
                        coefficient = coefficient - 2 * abs(self.pair_peak - (self.dice_probability[tile_dice] +
                                                                              self.dice_probability[j])) ** 2
                        if i == tile_resource:
                            coefficient /= 4
                        else:
                            coefficient *= 4
                        prob.append(coefficient)

            # print("pool of choice", len(candidates))
            indexes = []
            total = sum(prob)
            # print("total sum of coefficients:", total)
            # print(candidates)
            # print(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
            # print(candidates[numpy.asscalar(result[0])])
            return candidates[numpy.asscalar(result[0])]
        except Exception:
            raise Exception

    def generate_next_tile_possibilities_simple_triple(self, index1, index2):
        try:
            tile1_resource = self.tile[index1]  # already set
            tile1_dice = self.tile_dice[index1]  # already set
            tile2_resource = self.tile[index2]  # already set
            tile2_dice = self.tile_dice[index2]  # already set
            # print("closed triples")
            candidates = []
            prob = []
            for i in self.resource_distribution.configuration:
                for j in self.resource_distribution.configuration[i]:
                    if self.triple_coefficient[0] <= self.dice_probability[tile1_dice] + self.dice_probability[j] + \
                            self.dice_probability[tile2_dice] <= self.triple_coefficient[1] and \
                            self.pair_coefficient[0] <= \
                            self.dice_probability[j] + self.dice_probability[tile1_dice] <= \
                            self.pair_coefficient[1] and \
                            self.pair_coefficient[0] <= \
                            self.dice_probability[j] + self.dice_probability[tile2_dice] <= \
                            self.pair_coefficient[1]:
                        coefficient = 8
                        candidates.append((i, j))
                        coefficient += len(self.resource_distribution.configuration[i])
                        coefficient += self.dice_probability[j]
                        coefficient -= 2 * (abs(self.triple_peak - (self.dice_probability[tile1_dice] +
                                                                    self.dice_probability[tile2_dice] +
                                                                    self.dice_probability[j])) ** 2 +
                                            abs(self.pair_peak - (self.dice_probability[tile1_dice] +
                                                                  self.dice_probability[j])) ** 2 +
                                            abs(self.pair_peak - (self.dice_probability[tile2_dice] +
                                                                  self.dice_probability[j])) ** 2)
                        if i == tile1_resource:
                            coefficient /= 4
                        elif i != tile1_resource:
                            coefficient *= 4
                        if i == tile2_resource:
                            coefficient /= 4
                        elif i != tile2_resource:
                            coefficient *= 4
                        prob.append(coefficient)

            # print("pool of choice", len(candidates))
            indexes = []
            total = sum(prob)
            # print("total sum of coefficients:", total)
            # print(candidates)
            # print(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
            # print(candidates[numpy.asscalar(result[0])])
            return candidates[numpy.asscalar(result[0])]
        except Exception:
            raise Exception

    def generate_next_tile_possibilities_scattered_triple(self, index1, index2):
        try:
            tile1_resource = self.tile[index1]  # already set
            tile1_dice = self.tile_dice[index1]  # already set
            tile2_resource = self.tile[index2]  # already set
            tile2_dice = self.tile_dice[index2]  # already set
            # print("scattered triples")
            candidates = []
            prob = []
            for i in self.resource_distribution.configuration:
                for j in self.resource_distribution.configuration[i]:
                    if self.pair_coefficient[0] <= \
                            self.dice_probability[tile1_dice] + self.dice_probability[j] <= \
                            self.pair_coefficient[1] \
                            and \
                            self.pair_coefficient[0] <= \
                            self.dice_probability[tile2_dice] + self.dice_probability[j] <= \
                            self.pair_coefficient[1]:
                        coefficient = 20
                        candidates.append((i, j))
                        coefficient += len(self.resource_distribution.configuration[i])
                        coefficient += self.dice_probability[j]
                        coefficient -= 2 * (abs(self.pair_peak - (self.dice_probability[tile1_dice] +
                                                                  self.dice_probability[j])) ** 2 +
                                            abs(self.pair_peak - (self.dice_probability[tile2_dice] +
                                                                  self.dice_probability[j])) ** 2)
                        if i == tile1_resource:
                            coefficient /= 4
                        elif i != tile1_resource:
                            coefficient *= 4
                        if i == tile2_resource:
                            coefficient /= 4
                        elif i != tile2_resource:
                            coefficient *= 4
                        prob.append(coefficient)

            # print("pool of choice", len(candidates))
            indexes = []
            total = sum(prob)
            # print("total sum of coefficients:", total)
            # print(candidates)
            # print(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
            # print(candidates[numpy.asscalar(result[0])])
            return candidates[numpy.asscalar(result[0])]
        except Exception:
            raise Exception

    def generate_next_tile_possibilities_quad(self, index1, index2, index3):
        # index1 must be common for both triples (smallest of the indexes)
        try:
            tile1_resource = self.tile[index1]  # already set
            tile1_dice = self.tile_dice[index1]  # already set
            tile2_resource = self.tile[index2]  # already set
            tile2_dice = self.tile_dice[index2]  # already se
            tile3_resource = self.tile[index3]  # already set
            tile3_dice = self.tile_dice[index3]  # already set
            # print("scattered triples")
            candidates = []
            prob = []
            for i in self.resource_distribution.configuration:
                for j in self.resource_distribution.configuration[i]:
                    if self.triple_coefficient[0] <= self.dice_probability[tile1_dice] + \
                            self.dice_probability[tile2_dice] + \
                            self.dice_probability[j] <= self.triple_coefficient[1] and \
                            self.triple_coefficient[0] <= \
                            self.dice_probability[tile1_dice] + self.dice_probability[tile3_dice] + \
                            self.dice_probability[j] <= self.triple_coefficient[1] and \
                            self.pair_coefficient[0] <= self.dice_probability[tile2_dice] + self.dice_probability[j] <=\
                            self.pair_coefficient[1] and \
                            self.pair_coefficient[0] <= self.dice_probability[tile3_dice] + self.dice_probability[j] <=\
                            self.pair_coefficient[1]:
                        coefficient = 18
                        candidates.append((i, j))
                        coefficient += len(self.resource_distribution.configuration[i])
                        coefficient += self.dice_probability[j]
                        if i == tile1_resource or i == tile2_resource or i == tile3_resource:
                            coefficient -= 1
                        else:
                            coefficient += 1
                        coefficient -= 2 * (abs(self.triple_peak - (self.dice_probability[tile1_dice] +
                                                                    self.dice_probability[tile2_dice] +
                                                                    self.dice_probability[j])) ** 2 +
                                            abs(self.triple_peak - (self.dice_probability[tile1_dice] +
                                                                    self.dice_probability[tile3_dice] +
                                                                    self.dice_probability[j])) ** 2 +
                                            abs(self.pair_peak - (self.dice_probability[j] +
                                                                  self.dice_probability[tile2_dice])) ** 2 +
                                            abs(self.pair_peak - (self.dice_probability[j] +
                                                                  self.dice_probability[tile3_dice])) ** 2)
                        if i == tile1_resource:
                            coefficient /= 4
                        elif i != tile1_resource:
                            coefficient *= 4
                        if i == tile2_resource:
                            coefficient /= 4
                        elif i != tile2_resource:
                            coefficient *= 4
                        if i == tile3_resource:
                            coefficient /= 4
                        elif i != tile3_resource:
                            coefficient *= 4
                        prob.append(coefficient)

            # print("pool of choice", len(candidates))
            # if len(candidates) == 0:
            #     self.dbg()
            indexes = []
            total = sum(prob)
            # print("total sum of coefficients:", total)
            # print(candidates)
            # print(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
            # print(candidates[numpy.asscalar(result[0])])
            return candidates[numpy.asscalar(result[0])]
        except Exception:
            raise Exception
