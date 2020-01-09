from shapely.geometry import LineString, Point


def map(x: int, a: int, b: int, c: int, d: int) -> float:
    """
    Maps a number (x) that is between a and b to a equivalent number between c and d

    :param x: Number to map
    :type x: int

    :param a: Lower limit of original bound
    :type a: int

    :param b: Upper limit of original bound
    :type b: int

    :param c: Lower limit of new bound
    :type c: int

    :param d: Upper limit of new bound
    :type d: int

    :return: New number
    :rtype: float
    """
    return (x - a) / (b - a) * (d - c) + c


def get_int(text: str) -> int:
    """
    Gets a number from input, else complains about the input not being a number

    :param text: Display text for input prompt
    :type text: str

    :return: Number from input
    :rtype: int
    """
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Not a number!")


def intersect(a1, a2, b1, b2) -> list:
    """
    Checks if a line that starts at a1 and goes infinitely toward of a2 intersects with a line segment (b1, b2)
    If they intersect, it returns the point where they intersect as a list

    :param a1: Starting point of line A
    :type a1: Vector

    :param a2: Direction of line A to extend
    :type a2: Vector

    :param b1: Starting point of line B
    :type b1: Vector

    :param b2: End point of line B
    :type b2: Vector

    :return: A point where the lines intersect, or an empty list if they don't
    :rtype: List[float, float]
    """
    den = ((a2.x - a1.x) * (b2.y - b1.y)) - ((a2.y - a1.y) * (b2.x - b1.x))

    num1 = ((a1.y - b1.y) * (b2.x - b1.x)) - ((a1.x - b1.x) * (b2.y - b1.y))
    num2 = ((a1.y - b1.y) * (a2.x - a1.x)) - ((a1.x - b1.x) * (a2.y - a1.y))
    if not den:
        return []

    r = num1 / den
    s = num2 / den

    if 0 < r < 1 and s > 0:
        x = a1.x + r * (a2.x - a1.x)
        y = a1.y + r * (a2.y - a1.y)
        return [round(x, 2), round(y, 2)]
    else:
        return []


def segintersect(a1, a2, b1, b2):
    """
    Checks if a line segment (a1, a2) intersects with another line segment (b1, b2)
    If they intersect, it returns the point where they intersect as a list

    :param a1: Starting point of line A
    :type a1: Vector

    :param a2: End point of line A
    :type a2: Vector

    :param b1: Starting point of line B
    :type b1: Vector

    :param b2: End point of line B
    :type b2: Vector

    :return: A point where the lines intersect, or an empty list if they don't
    :rtype: List[float, float]
    """
    line1 = LineString([(a1.x, a1.y), (a2.x, a2.y)])
    line2 = LineString([(b1.x, b1.y), (b2.x, b2.y)])

    int_pt = line1.intersection(line2)
    return [int_pt.x, int_pt.y] if (type(int_pt) == Point) else []
