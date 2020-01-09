def map(x: int, a: int, b: int, c: int, d: int):
    return (x - a) / (b - a) * (d - c) + c


def get_int(text: str):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Not a number!")