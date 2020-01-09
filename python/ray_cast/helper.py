from shapely.geometry import LineString, Point


def map(x: int, a: int, b: int, c: int, d: int):
    return (x - a) / (b - a) * (d - c) + c


def get_int(text: str):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Not a number!")


def intersect(a, b, c, d) -> list:
    """
    Used for raycasting, assumes lines go infinitely
    :param a:
    :param b:
    :param c:
    :param d:
    :return:
    """
    den = ((b.x - a.x) * (d.y - c.y)) - ((b.y - a.y) * (d.x - c.x))

    num1 = ((a.y - c.y) * (d.x - c.x)) - ((a.x - c.x) * (d.y - c.y))
    num2 = ((a.y - c.y) * (b.x - a.x)) - ((a.x - c.x) * (b.y - a.y))
    if not den:
        return []

    r = num1 / den
    s = num2 / den

    if 0 < r < 1 and s > 0:
        x = a.x + r * (b.x - a.x)
        y = a.y + r * (b.y - a.y)
        return [round(x, 2), round(y, 2)]
    else:
        return []


def segintersect(a1, a2, b1, b2):
    line1 = LineString([(a1.x, a1.y), (a2.x, a2.y)])
    line2 = LineString([(b1.x, b1.y), (b2.x, b2.y)])

    int_pt = line1.intersection(line2)
    return [int_pt.x, int_pt.y] if (type(int_pt) == Point) else []
