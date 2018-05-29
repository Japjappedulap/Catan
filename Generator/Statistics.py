import pickle
import matplotlib.pyplot as plt


class Statistics:
    # TODO Implement statistics
    def __init__(self):
        self.coefficients = {}
        self.init_statistics()

    def init_statistics(self):
        coefficient_file = open("coefficients.pickle", "rb")
        self.coefficients = pickle.load(coefficient_file)

    @staticmethod
    def reset_statistics_file():
        with open("coefficients.pickle", "wb") as file:
            pickle.dump({}, file)

    def close_statistics(self):
        with open("coefficients.pickle", "wb") as file:
            pickle.dump(self.coefficients, file)

    def log_coefficient(self, coefficient):
        coefficient = int(coefficient)
        if coefficient in self.coefficients:
            self.coefficients[coefficient] += 1
        else:
            self.coefficients[coefficient] = 1

    def generate_graph(self):
        key_list = list(self.coefficients.keys())
        key_list.sort()
        value_list = []
        for i in key_list:
            value_list.append(self.coefficients[i])
        plt.scatter(key_list, value_list)
        plt.show()
