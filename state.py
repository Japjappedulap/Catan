import random

INF = 999999


class ClassicState:
    def __init__(self):
        self.configuration = {1: [0, 0, 0, 0], 2: [0, 0, 0, 0], 3: [0, 0, 0, 0], 4: [0, 0, 0], 5: [0, 0, 0]}
        self.resource_pool = {1: 4, 2: 4, 3: 4, 4: 3, 5: 3, 6: 1}
        self.dices_available = {2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 1}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}

    def next_dice(self):
        best_prob = 0
        for i in self.dices_available:
            if self.dices_available[i] > 0:
                best_prob = max(self.dice_probability[i], best_prob)
        possible_choice = []
        for i in self.dices_available:
            if self.dices_available[i] > 0 and self.dice_probability[i] == best_prob:
                possible_choice.append(i)
        random.shuffle(possible_choice)
        return possible_choice[0]

    def next_resource(self):
        # returns list of resource codes available for next addition
        to_sort = []
        for resource_code in self.configuration:
            coefficient = sum(self.configuration[resource_code]) + len(self.configuration[resource_code])
            completed_resource = True
            for i in self.configuration[resource_code]:
                if i == 0:
                    completed_resource = False
                    break
            if completed_resource:
                coefficient = INF
            to_sort.append((coefficient, resource_code))
        to_sort.sort()
        result = []
        best_value = to_sort[0][0]
        for pair in to_sort:
            if pair[0] == best_value:
                result.append(pair[1])
        random.shuffle(result)
        return result[0]

    def add_to_state(self, where, what):
        for i in range(0, len(self.configuration[where])):
            if self.configuration[where][i] == 0:
                self.configuration[where][i] = what
                self.dices_available[what] -= 1
                return

    def completed(self):
        for i in self.dices_available:
            if self.dices_available[i] != 0:
                return False
        return True

    def all_coefficient(self):
        result = {}
        for i in self.configuration:
            coefficient = 0
            for j in self.configuration[i]:
                coefficient += self.dice_probability[j]
            result[i] = coefficient
        return result

    def max_coefficient(self):
        coefficients = self.all_coefficient()
        result = 0
        for i in coefficients:
            result = max(result, coefficients[i])
        return result

    def min_coefficient(self):
        coefficients = self.all_coefficient()
        result = INF
        for i in coefficients:
            result = min(result, coefficients[i])
        return result

    def generate(self):
        while not self.completed():
            next_dice = self.next_dice()
            next_resource = self.next_resource()
            self.add_to_state(next_resource, next_dice)

    def remove_resource(self, resource, dice):
        self.configuration[resource].remove(dice)

    def generate_balanced(self):
        self.generate()

        while not ((self.max_coefficient() <= 12 and self.all_coefficient()[5] == 12 and self.all_coefficient()[
            4] == 12 and
                    self.all_coefficient()[2] == 10) or
                   (self.max_coefficient() <= 12 and self.all_coefficient()[3] == 11 and self.all_coefficient()[
                       2] == 11)):
            self.clear()
            self.generate()
        return self

    def clear(self):
        self.configuration = {1: [0, 0, 0, 0], 2: [0, 0, 0, 0], 3: [0, 0, 0, 0], 4: [0, 0, 0], 5: [0, 0, 0]}
        self.resource_pool = {1: 4, 2: 4, 3: 4, 4: 3, 5: 3, 6: 1}
        self.dices_available = {2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 1}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}


class ExtendedState:
    def __init__(self):
        self.configuration = {1: [0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0], 4: [0, 0, 0, 0, 0],
                              5: [0, 0, 0, 0, 0]}
        self.resource_pool = {1: 6, 2: 6, 3: 6, 4: 5, 5: 5, 6: 2}
        self.dices_available = {2: 2, 3: 3, 4: 3, 5: 3, 6: 3, 8: 3, 9: 3, 10: 3, 11: 3, 12: 2}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}

    def next_dice(self):
        best_prob = 0
        for i in self.dices_available:
            if self.dices_available[i] > 0:
                best_prob = max(self.dice_probability[i], best_prob)
        possible_choice = []
        for i in self.dices_available:
            if self.dices_available[i] > 0 and self.dice_probability[i] == best_prob:
                possible_choice.append(i)
        random.shuffle(possible_choice)
        return possible_choice[0]

    def next_resource(self):
        # returns list of resource codes available for next addition
        to_sort = []
        for resource_code in self.configuration:
            coefficient = sum(self.configuration[resource_code]) + len(self.configuration[resource_code])
            completed_resource = True
            for i in self.configuration[resource_code]:
                if i == 0:
                    completed_resource = False
                    break
            if completed_resource:
                coefficient = INF
            to_sort.append((coefficient, resource_code))
        to_sort.sort()
        result = []
        best_value = to_sort[0][0]
        for pair in to_sort:
            if pair[0] == best_value:
                result.append(pair[1])
        random.shuffle(result)
        return result[0]

    def add_to_state(self, where, what):
        for i in range(0, len(self.configuration[where])):
            if self.configuration[where][i] == 0:
                self.configuration[where][i] = what
                self.dices_available[what] -= 1
                return

    def completed(self):
        for i in self.dices_available:
            if self.dices_available[i] != 0:
                return False
        return True

    def all_coefficient(self):
        result = {}
        for i in self.configuration:
            coefficient = 0
            for j in self.configuration[i]:
                coefficient += self.dice_probability[j]
            result[i] = coefficient
        return result

    def max_coefficient(self):
        coefficients = self.all_coefficient()
        result = 0
        for i in coefficients:
            result = max(result, coefficients[i])
        return result

    def min_coefficient(self):
        coefficients = self.all_coefficient()
        result = INF
        for i in coefficients:
            result = min(result, coefficients[i])
        return result

    def generate(self):
        while not self.completed():
            next_dice = self.next_dice()
            next_resource = self.next_resource()
            self.add_to_state(next_resource, next_dice)

    def remove_resource(self, resource, dice):
        self.configuration[resource].remove(dice)

    def generate_balanced(self):
        self.generate()
        while not (
                (self.max_coefficient() <= 20 and self.all_coefficient()[5] >= 18 and self.all_coefficient()[
                    4] >= 18
                 and self.all_coefficient()[2] <= 17)
                or
                (self.max_coefficient() <= 18 and self.all_coefficient()[3] == 17 and self.all_coefficient()[
                    2] == 17) and self.min_coefficient() >= 17):
            self.clear()
            # print("failed at dice generator")
            self.generate()
        return self

    def clear(self):
        self.configuration = {1: [0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0], 4: [0, 0, 0, 0, 0],
                              5: [0, 0, 0, 0, 0]}
        self.resource_pool = {1: 6, 2: 6, 3: 6, 4: 5, 5: 5, 6: 2}
        self.dices_available = {2: 2, 3: 3, 4: 3, 5: 3, 6: 3, 8: 3, 9: 3, 10: 3, 11: 3, 12: 2}
        self.dice_probability = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
