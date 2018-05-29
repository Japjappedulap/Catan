import datetime

from Generator.ClassicMap import ClassicMap
from Generator.ExtendedMap import ExtendedMap


def classic():
    no_player = 5  # desert on corner
    # no_player = 6  # desert in center
    # no_player = 7  # desert in edge
    # no_player = 8  # desert in inner circle

    start_time = datetime.datetime.now()
    catan_map = ClassicMap()
    catan_map.generate_map(no_player)
    k = 0
    while not catan_map.completed():
        catan_map.clear()
        catan_map.generate_map(no_player)
        k += 1
    print("completed in:", datetime.datetime.now() - start_time, "seconds, with", k, "attempts")
    catan_map.dbg()
    dic = catan_map.export()
    return dic


def extended():
    start_time = datetime.datetime.now()
    no_player = 6
    catan_map = ExtendedMap()
    catan_map.generate_map(no_player)
    k = 0
    while not catan_map.completed():
        # x.dbg()
        # sleep(1)
        catan_map = ExtendedMap()
        catan_map.generate_map(no_player)
        k += 1
    print("completed in:", datetime.datetime.now() - start_time, "seconds, with", k, "attempts")
    catan_map.dbg()
    dic = catan_map.export()
    return dic


if __name__ == '__main__':

    # global_coefficient_records = []
    # test()
    v = classic()
    print(v)
    v = extended()
    print(v)

    # from Statistics import Statistics
    # x = Statistics()
    # x.coefficients[6] = 10
    # x.generate_graph()
