WIDTH = 8
HEIGHT = 26
x = 0
y = 0


def y_out_of_bonds(y1, x1):
    if y1 == WIDTH and x1 % 2 == 1:
        return True
    return False


def set_x_y(_x, _y):
    global x, y
    x = _x
    y = _y


def neighbor_up_position():
    if x - 2 < 0:
        return None
    return x - 2, y


def neighbor_down_position():
    if x + 2 > HEIGHT:
        return None
    return x + 2, y


def neighbor_upper_left_position():
    y1 = y
    if x % 2 == 0:
        y1 -= 1
    if x - 1 < 0 or y1 < 0:
        return None
    else:
        return x - 1, y1


def neighbor_upper_right_position():
    # < y1 = 25   7
    # > 24 8
    y1 = y
    if x % 2 == 1:
        y1 += 1
    if x - 1 < 0 or y1 > WIDTH or y_out_of_bonds(y1, x - 1):
        return None
    return x - 1, y1


def neighbor_down_left_position():
    y1 = y
    if x % 2 == 0:
        y1 -= 1
    if x + 1 > HEIGHT or y1 < 0:
        return None
    return x + 1, y1


def neighbor_down_right_position():
    y1 = y
    if x % 2 == 1:
        y1 += 1
    if x + 1 > HEIGHT or y1 > WIDTH or y_out_of_bonds(y1, x + 1):
        return None
    else:
        return x + 1, y1
