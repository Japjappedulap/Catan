import datetime

from Generator.ClassicMap import ClassicMap
from Generator.ExtendedMap import ExtendedMap


def dummy():
    import json
    return json.dumps({"tile": [
        {"index": 0, "dice": 0, "resource_type": "DESE"},
        {"index": 1, "dice": 5, "resource_type": "OREE"},
        {"index": 2, "dice": 2, "resource_type": "WOOL"},
        {"index": 3, "dice": 6, "resource_type": "CLAY"},
        {"index": 4, "dice": 11, "resource_type": "GRAI"},
        {"index": 5, "dice": 10, "resource_type": "LUMB"},
        {"index": 6, "dice": 6, "resource_type": "OREE"},
        {"index": 7, "dice": 3, "resource_type": "LUMB"},
        {"index": 8, "dice": 4, "resource_type": "OREE"},
        {"index": 9, "dice": 8, "resource_type": "WOOL"},
        {"index": 10, "dice": 12, "resource_type": "GRAI"},
        {"index": 11, "dice": 9, "resource_type": "CLAY"},
        {"index": 12, "dice": 9, "resource_type": "GRAI"},
        {"index": 13, "dice": 3, "resource_type": "LUMB"},
        {"index": 14, "dice": 4, "resource_type": "CLAY"},
        {"index": 15, "dice": 8, "resource_type": "LUMB"},
        {"index": 16, "dice": 10, "resource_type": "WOOL"},
        {"index": 17, "dice": 5, "resource_type": "GRAI"},
        {"index": 18, "dice": 11, "resource_type": "WOOL"}],
        "type": "classic"})


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
