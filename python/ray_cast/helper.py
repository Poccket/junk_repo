def map(x: int, a: int, b: int, c: int, d: int):
    return (x - a) / (b - a) * (d - c) + c


def get_int(text: str):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Not a number!")


def intersect(a, b, c, d):
    x1, y1 = a.x, a.y
    x2, y2 = b.x, b.y
    x3, y3 = c.x, c.y
    x4, y4 = d.x, d.y

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if not den:
        return

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

    if 0 < t < 1 and u > 0:
        pt = [0, 0]
        pt[0] = x1 + t * (x2 - x1)
        pt[1] = y1 + t * (y2 - y1)
        return pt
    else:
        return
