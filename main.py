import datetime

from ClassicMap import ClassicMap
from ExtendedMap import ExtendedMap


def classic():
    no_player = 5  # desert on corner
    # no_player = 6  # desert in center
    # no_player = 7  # desert in edge
    # no_player = 8  # desert in inner circle

    start_time = datetime.datetime.now()
    x = ClassicMap()
    x.generate_map(no_player)
    k = 0
    while not x.completed():
        # x = ClassicMap()
        # x.generate_map(no_player)
        x.clear()
        x.generate_map(no_player)
        # x.dbg()
        k += 1
    print("completed in:", datetime.datetime.now() - start_time, "seconds, with", k, "attempts")
    x.dbg()


def extended():
    start_time = datetime.datetime.now()
    no_player = 6
    x = ExtendedMap()
    x.generate_map(no_player)
    k = 0
    while not x.completed():
        # x.dbg()
        # sleep(1)
        x = ExtendedMap()
        x.generate_map(no_player)
        k += 1
    print("completed in:", datetime.datetime.now() - start_time, "seconds, with", k, "attempts")
    x.dbg()


if __name__ == '__main__':

    # global_coefficient_records = []
    # test()
    classic()
    # extended()

    # from Statistics import Statistics
    # x = Statistics()
    # x.coefficients[6] = 10
    # x.generate_graph()
