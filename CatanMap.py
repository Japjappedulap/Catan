import numpy

from Statistics import Statistics


class CatanMap:
    # GLOBAL variables
    pair_coefficient = [4, 7]
    trip_coefficient = [8, 10]
    pair_peak = pair_coefficient[0] + pair_coefficient[1] / 2
    trip_peak = trip_coefficient[0] + trip_coefficient[1] / 2
    initial_coefficient = 100

    def __init__(self):
        # print("creating new map")
        self.tile = []
        self.tile_dice = []
        self.neighbor_recurrence = {}
        self.resource_distribution = None
        self.tile_pairs = []
        self.tile_to_name = {0: "none", 1: "LUMB", 2: "WOOL", 3: "GRAI", 4: "OREE", 5: "CLAY", 6: "DESE"}
        self.name_to_tile = {"LUMB": 1, "WOOL": 2, "GRAI": 3, "OREE": 4, "CLAY": 5, "DESE": 6}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
        # self.statistics = Statistics()

    # def __del__(self):
        # self.statistics.close_statistics()
        # self.statistics.generate_graph()

    def fix_tile(self, index, resource, dice):
        self.tile[index] = resource
        self.tile_dice[index] = dice
        self.resource_distribution.remove_resource(resource, dice)

    def get_resource_distribution(self):
        return self.resource_distribution

    def completed(self):
        if not self.no_identic_neighbours():
            return False
        for i in self.tile:
            if i == 0:
                return False
        return True

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

            indexes = []
            total = sum(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
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
                        coefficient = self.initial_coefficient
                        candidates.append((i, j))

                        # coefficient grows if there are more resources available in the pool
                        coefficient += len(self.resource_distribution.configuration[i])

                        # coefficient grows if bigger dice
                        coefficient += self.dice_probability[j]

                        # coefficient grows when getting closer to peak
                        coefficient = coefficient - 2 * abs(self.pair_peak - (self.dice_probability[tile_dice] +
                                                                              self.dice_probability[j])) ** 2

                        # coefficient shrinks if resources are identical
                        if i == tile_resource:
                            coefficient /= 4
                        else:
                            coefficient *= 4

                        prob.append(coefficient)
                        # records coefficient for statistics
                        # self.statistics.log_coefficient(coefficient)

            indexes = []
            total = sum(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
            return candidates[numpy.asscalar(result[0])]
        except Exception as e:
            print(e)
            # if no tile and dice available, throw exception in order to stop
            raise Exception

    def generate_next_tile_possibilities_closed_triple(self, index1, index2):
        try:
            tile1_resource = self.tile[index1]  # already set
            tile1_dice = self.tile_dice[index1]  # already set
            tile2_resource = self.tile[index2]  # already set
            tile2_dice = self.tile_dice[index2]  # already set

            candidates = []
            prob = []
            for i in self.resource_distribution.configuration:
                for j in self.resource_distribution.configuration[i]:
                    if self.trip_coefficient[0] <= self.dice_probability[tile1_dice] + self.dice_probability[j] + \
                            self.dice_probability[tile2_dice] <= self.trip_coefficient[1]:
                        coefficient = self.initial_coefficient
                        candidates.append((i, j))

                        # coefficient grows if there are more resources available in the pool
                        coefficient += len(self.resource_distribution.configuration[i])

                        # coefficient grows if bigger dice
                        coefficient += self.dice_probability[j]

                        # coefficient grows when getting closer to peak
                        coefficient -= 2 * abs(self.trip_peak - (self.dice_probability[tile1_dice] +
                                                                 self.dice_probability[tile2_dice] +
                                                                 self.dice_probability[j])) ** 2

                        # coefficient shrinks if resources are identical
                        if i == tile1_resource:
                            coefficient /= 4
                        elif i != tile1_resource:
                            coefficient *= 4
                        if i == tile2_resource:
                            coefficient /= 4
                        elif i != tile2_resource:
                            coefficient *= 4

                        prob.append(coefficient)
                        # records coefficient for statistics
                        # self.statistics.log_coefficient(coefficient)

            indexes = []
            total = sum(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
            return candidates[numpy.asscalar(result[0])]
        except Exception:
            raise Exception

    def generate_next_tile_possibilities_scattered_triple(self, index1, index2):
        try:
            tile1_resource = self.tile[index1]  # already set
            tile1_dice = self.tile_dice[index1]  # already set
            tile2_resource = self.tile[index2]  # already set
            tile2_dice = self.tile_dice[index2]  # already set

            candidates = []
            prob = []
            for i in self.resource_distribution.configuration:
                for j in self.resource_distribution.configuration[i]:
                    if self.pair_coefficient[0] <= self.dice_probability[tile1_dice] + self.dice_probability[j] <= \
                            self.pair_coefficient[1] and \
                            self.pair_coefficient[0] <= self.dice_probability[tile2_dice] + self.dice_probability[j] \
                            <= self.pair_coefficient[1]:
                        coefficient = self.initial_coefficient
                        candidates.append((i, j))

                        # coefficient grows if there are more resources available in the pool
                        coefficient += len(self.resource_distribution.configuration[i])

                        # coefficient grows if bigger dice
                        coefficient += self.dice_probability[j]

                        # coefficient grows when getting closer to peak
                        coefficient -= 2 * (abs(self.pair_peak - (self.dice_probability[tile1_dice] +
                                                                  self.dice_probability[j])) ** 2 +
                                            abs(self.pair_peak - (self.dice_probability[tile2_dice] +
                                                                  self.dice_probability[j])) ** 2)

                        # coefficient shrinks if resources are identical
                        if i == tile1_resource:
                            coefficient /= 4
                        elif i != tile1_resource:
                            coefficient *= 4
                        if i == tile2_resource:
                            coefficient /= 4
                        elif i != tile2_resource:
                            coefficient *= 4

                        prob.append(coefficient)
                        # records coefficient for statistics
                        # self.statistics.log_coefficient(coefficient)

            indexes = []
            total = sum(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
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

            candidates = []
            prob = []
            for i in self.resource_distribution.configuration:
                for j in self.resource_distribution.configuration[i]:
                    if self.trip_coefficient[0] <= self.dice_probability[tile1_dice] + \
                            self.dice_probability[tile2_dice] + \
                            self.dice_probability[j] <= self.trip_coefficient[1] \
                            and self.trip_coefficient[0] <= \
                            self.dice_probability[tile1_dice] + \
                            self.dice_probability[tile3_dice] + \
                            self.dice_probability[j] <= self.trip_coefficient[1]:
                        coefficient = self.initial_coefficient
                        candidates.append((i, j))

                        # coefficient grows if there are more resources available in the pool
                        coefficient += len(self.resource_distribution.configuration[i])

                        # coefficient grows if bigger dice
                        coefficient += self.dice_probability[j]

                        # coefficient grows when getting closer to peak
                        coefficient -= 2 * (abs(self.trip_peak - (self.dice_probability[tile1_dice] +
                                                                  self.dice_probability[tile2_dice] +
                                                                  self.dice_probability[j])) ** 2 +
                                            abs(self.trip_peak - (self.dice_probability[tile1_dice] +
                                                                  self.dice_probability[tile3_dice] +
                                                                  self.dice_probability[j])) ** 2)

                        # coefficient shrinks if resources are identical
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
                        # records coefficient for statistics
                        # self.statistics.log_coefficient(coefficient)

            indexes = []
            total = sum(prob)
            for i in range(len(prob)):
                prob[i] = prob[i] / total
                indexes.append(i)
            result = numpy.random.choice(indexes, 1, p=prob)
            return candidates[numpy.asscalar(result[0])]
        except Exception:
            raise Exception
