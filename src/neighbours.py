WIDTH = 9
HEIGHT = 26
x = 0
y = 0


def set_x_y(_x, _y):
    global x, y
    x = _x
    y = _y


def neighbour_up_position():
    if x - 2 < 0:
        return None
    return x - 2, y


def neighbour_down_position():
    if x + 2 > HEIGHT:
        return None
    return x + 2, y


def neighbour_upper_left_position():
    y1 = y
    if x % 2 == 0:
        y1 -= 1
    if x - 1 < 0 or y1 < 0:
        return None
    else:
        return x - 1, y1


def neighbour_upper_right_position():
    y1 = y
    if x % 2 == 1:
        y1 += 1
    if x - 1 < 0 or y1 > WIDTH:
        return None
    return x - 1, y1


def neighbour_down_left_position():
    y1 = y
    if x % 2 == 0:
        y1 -= 1
    if x + 1 > HEIGHT or y1 < 0:
        return None
    return x + 1, y1


def neighbour_down_right_position():
    y1 = y
    if x % 2 == 1:
        y1 += 1
    if x + 1 > HEIGHT or y1 > WIDTH:
        return None
    else:
        return x + 1, y1
