import classes as cl

width = 800
height = 800

spawn = cl.Vector(250, 250)

walls = [
    # Map boundaries
    cl.Boundary(cl.Vector(1, 1), cl.Vector(1, height)),
    cl.Boundary(cl.Vector(1, height), cl.Vector(width, height), (200, 200, 200)),
    cl.Boundary(cl.Vector(width, height), cl.Vector(width, 1)),
    cl.Boundary(cl.Vector(width, 1), cl.Vector(1, 1), (200, 200, 200)),

    # Square in upper left
    cl.Boundary(cl.Vector(25, 25), cl.Vector(25, 75), (255, 0, 0)),
    cl.Boundary(cl.Vector(25, 75), cl.Vector(75, 75), (0, 255, 0)),
    cl.Boundary(cl.Vector(75, 75), cl.Vector(75, 25), (0, 0, 255)),
    cl.Boundary(cl.Vector(75, 25), cl.Vector(25, 25)),

    # Square in lower right
    cl.Boundary(cl.Vector(725, 725), cl.Vector(725, 775)),
    cl.Boundary(cl.Vector(725, 775), cl.Vector(775, 775)),
    cl.Boundary(cl.Vector(775, 775), cl.Vector(775, 725)),
    cl.Boundary(cl.Vector(775, 725), cl.Vector(725, 725)),

    # Rainbow Hexagon
    cl.Boundary(cl.Vector(400, 290), cl.Vector(447, 317), (255, 0, 0)),     # Wall 1
    cl.Boundary(cl.Vector(447, 317), cl.Vector(495, 345), (255, 255, 0)),
    cl.Boundary(cl.Vector(495, 345), cl.Vector(495, 400), (0, 255, 0)),     # Wall 2
    cl.Boundary(cl.Vector(495, 400), cl.Vector(495, 455), (0, 255, 255)),
    cl.Boundary(cl.Vector(495, 455), cl.Vector(447, 482), (0, 0, 255)),     # Wall 3
    cl.Boundary(cl.Vector(447, 482), cl.Vector(400, 510), (255, 0, 255)),
    cl.Boundary(cl.Vector(400, 510), cl.Vector(353, 482), (255, 0, 0)),     # Wall 4
    cl.Boundary(cl.Vector(353, 482), cl.Vector(305, 455), (255, 255, 0)),
    cl.Boundary(cl.Vector(305, 455), cl.Vector(305, 400), (0, 255, 0)),     # Wall 5
    cl.Boundary(cl.Vector(305, 400), cl.Vector(305, 345), (0, 255, 255)),
    cl.Boundary(cl.Vector(305, 345), cl.Vector(353, 317), (0, 0, 255)),     # Wall 6
    cl.Boundary(cl.Vector(353, 317), cl.Vector(400, 290), (255, 0, 255)),

    # """Brick""" wall
    cl.Boundary(cl.Vector(600, 75), cl.Vector(700, 175), (188, 60, 33)),
    cl.Boundary(cl.Vector(600, 75), cl.Vector(610, 65), (188, 60, 33)),
    cl.Boundary(cl.Vector(700, 175), cl.Vector(710, 165), (188, 60, 33)),
    cl.Boundary(cl.Vector(710, 165), cl.Vector(610, 65), (188, 60, 33))
]
