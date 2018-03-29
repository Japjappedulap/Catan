import datetime
from classicMap import SimpleTable
from extendedMap import ExtendedTable


def classic():
    no_player = 5  # desert on corner
    # no_player = 6  # desert in center
    # no_player = 7  # desert in edge
    # no_player = 8  # desert in inner circle

    start_time = datetime.datetime.now()
    x = SimpleTable()
    x.generate_map(no_player)
    k = 0
    while not x.completed():
        x = SimpleTable()
        x.generate_map(no_player)
        k += 1
    print("completed in:", datetime.datetime.now() - start_time, "seconds, with", k, "attempts")
    x.dbg()


def extended():
    start_time = datetime.datetime.now()
    no_player = 6
    x = ExtendedTable()
    x.generate_map(no_player)
    k = 0
    while not x.completed():
        # x.dbg()
        # sleep(1)
        x = ExtendedTable()
        x.generate_map(no_player)
        k += 1
    print("completed in:", datetime.datetime.now() - start_time, "seconds, with", k, "attempts")
    x.dbg()


if __name__ == '__main__':
    # test()
    # classic()
    extended()
