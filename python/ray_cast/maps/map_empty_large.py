import classes as cl

width = 2000
height = 2000

spawn = cl.Vector(1000, 1000)

walls = [
    # Map boundaries
    cl.Boundary(cl.Vector(1, 1), cl.Vector(1, height)),
    cl.Boundary(cl.Vector(1, height), cl.Vector(width, height), (200, 200, 200)),
    cl.Boundary(cl.Vector(width, height), cl.Vector(width, 1)),
    cl.Boundary(cl.Vector(width, 1), cl.Vector(1, 1), (200, 200, 200)),
]
