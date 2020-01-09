import classes as cl

width = 500
height = 500

sky = (0, 0, 0)
floor = (128, 128, 128)

r_distance = 640000
r_color = sky

spawn = cl.Vector(250, 250)

walls = [
    # Map boundaries
    cl.Boundary(cl.Vector(1, 1), cl.Vector(1, height)),
    cl.Boundary(cl.Vector(1, height), cl.Vector(width, height), (200, 200, 200)),
    cl.Boundary(cl.Vector(width, height), cl.Vector(width, 1)),
    cl.Boundary(cl.Vector(width, 1), cl.Vector(1, 1), (200, 200, 200)),
]
