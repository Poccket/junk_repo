from typing import List
from math import sqrt, radians, cos, sin, ceil
import pygame as pg
import helper as hl


class Vector:
    """
    A simple vector object with a position and various functions

    :param x: Position along the horizontal
    :type x: float
    :param y: Position along the vertical
    :type y: float
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def normalize(self, scale: float = 1):
        """
        Normalizes the vector with a scale
        I gotta be honest I don't know exactly what this does

        :param scale: Scale
        :type scale: float
        :return: None
        """
        norm = sqrt(self.x * self.x + self.y * self.y)
        if norm != 0:
            self.x = scale * self.x / norm
            self.y = scale * self.y / norm
        return

    def setmag(self, n: float):
        """
        Sets the magnitude of the vector

        :param n: Scale of the magnitude
        :type n: float
        :return: None
        """
        self.normalize()
        self.mult(n)
        return

    def mult(self, n: float):
        """
        Multiplies the vector by n

        :param n: Factor to multiply by
        :type n: float
        :return: None
        """
        self.x *= n
        self.y *= n
        return

    def dist(self, v2: "Vector"):
        """
        Determines distance between two vectors

        :param v2: Second vector
        :type v2: Vector
        :return: Distance
        :rtype: float
        """
        return sqrt((v2.x - self.x)**2 + (v2.y - self.y)**2)

    def add(self, vec: "Vector"):
        """
        Adds two vectors together

        :param vec: Second vector
        :type vec: Vector
        :return: None
        """
        self.x += vec.x
        self.y += vec.y
        return


class Boundary:
    """
    A boundary made from two vectors

    :param posa: The first position of the boundary
    :type posa: Vector

    :param posb: The second position of the boundary
    :type posb: Vector

    :param col: Three colors delineating an RGB color
    :type col: tuple

    :param clip: Whether or not the wall can be clipped through
    :type clip: bool
    """
    def __init__(self, posa: Vector, posb: Vector, col: tuple = (255, 255, 255), clip: bool = False):
        self.a = posa
        self.b = posb
        self.col = col
        self.clip = clip

    def draw(self, win: pg.Surface, stroke: float = 1, offset: float = 0):
        """
        Draws the boundary on the screen (2D)

        :param win: The window to draw to
        :type win: pygame.Surface
        :param stroke: The width of the line
        :type stroke: float
        :param offset: Horizontal offset to draw too
        :type offset: float
        :return:
        """
        pg.draw.line(win, self.col, [self.a.x+offset, self.a.y], [self.b.x+offset, self.b.y], stroke)


class Ray:
    """
    A ray drawn from a point that goes infinitely offward

    :param pos: The position that the ray starts
    :type pos: Vector
    :param angle: The angle the ray is facing
    :type angle: float
    """
    def __init__(self, pos: Vector, angle: float):
        self.pos = pos
        self.ang = Vector(cos(angle), sin(angle))

    def setangle(self, a: float):
        """
        Set the angle to a

        :param a: Angle to set
        :type a: float
        :return: None
        """
        self.ang = Vector(cos(a), sin(a))
        return

    def look(self, x: float, y: float):
        """
        Look towards a point

        :param x: Horizontal position
        :type x: float
        :param y: Vertical position
        :type y: float
        :return: None
        """
        self.ang.x = x - self.pos.x
        self.ang.y = y - self.pos.y
        self.ang.normalize()
        return

    def draw(self, win: pg.Surface, color: tuple = (255, 255, 255), stroke: float = 1):
        """
        Draw the ray on the screen (2D)

        :param win: The window to draw to
        :type win: pygame.Surface
        :param color: Color of the ray
        :type color: tuple
        :param stroke: The width of the line
        :type stroke: float
        :return: None
        """
        draw_dir = [self.pos.x + (self.ang.x * 10), self.pos.y + (self.ang.y * 10), ]
        pg.draw.line(win, color, [self.pos.x, self.pos.y], draw_dir, stroke)
        return

    def cast(self, wall: Boundary):
        """
        Checks if the ray intersects with a wall, and returns the results

        :param wall: A boundary to check the intersection with
        :type wall: Boundary
        :return: The point where the ray hits the wall, or an empty list if it doesn't
        :rtype: List[float]
        """
        return hl.intersect(wall.a, wall.b, self.pos, Vector(self.pos.x + self.ang.x, self.pos.y + self.ang.y))


class Particle:
    """
    A particle that draws rays for drawing

    :param pos: The initial position of the particle
    :type pos: Vector
    :param fov: The field of view, and the initital raycount
    :type fov: int
    :param res: The amount to multiply the raycount by
    :type res: int
    """
    def __init__(self, pos: Vector = Vector(250, 250), fov: int = 90, res: int = 1):
        self.pos = pos
        self.rays = []
        self.fov = fov
        self.heading = 0
        self.res = res
        for x in range(0-(int(fov/2))*res, int(fov/2)*res):
            self.rays.append(Ray(self.pos, radians(x/res)))
        self.rotate(0)

    def move(self, amt: float):
        """
        Move in the direction of the heading

        :param amt: Amount to move
        :type amt: float
        :return: None
        """
        vel = Vector(cos(self.heading), sin(self.heading))
        vel.setmag(amt)
        self.pos.add(vel)
        return

    def update(self, x: float, y: float):
        """
        Move to new position

        :param x: Horizontal position
        :type x: float
        :param y: Vertical position
        :type y: float
        :return: None
        """
        self.pos = Vector(x, y)
        for ray in self.rays:
            ray.pos = self.pos
        return

    def rotate(self, angle: float):
        """
        Rotate clockwise by angle

        :param angle: Angle to turn
        :type angle: float
        :return: None
        """
        self.heading += angle
        index = 0
        for i in range(0-(int(len(self.rays)/2)), int(len(self.rays)/2)):
            self.rays[index].setangle(radians(i / self.res) + self.heading)
            index += 1
        return

    def look(self, win: pg.Surface, walls: List[Boundary], do_draw: bool, offset: float = 0):
        """
        Checks all ray intersections and returns a list of all of them

        :param win: Screen to draw to if enabled
        :type win: pygame.Surface
        :param walls: List of walls to check intersections with
        :type walls: List[Boundary]
        :param do_draw: Whether or not to draw the rays
        :type do_draw: bool
        :param offset: Horizontal offset to draw too
        :type offset: float
        :return: A list of all points of intersections with walls and rays
        :rtype: List[List[float]]
        """
        scene = []
        for ray in self.rays:
            closest = None
            record = [float("inf")]
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    d = self.pos.dist(Vector(pt[0], pt[1]))
                    if d < record[0]:
                        record = [ceil(d), wall.col]
                        closest = pt
            if closest and do_draw:
                pg.draw.line(win, (255, 255, 255), [self.pos.x+offset, self.pos.y], [closest[0]+offset, closest[1]], 1)
            if record[0] < float("inf"):
                scene.append(record)
            else:
                scene.append([float("inf"), (0, 0, 0)])
        return scene

    def draw(self, win, color=(255, 255, 255), stroke: float = 0, offset: float = 0):
        """
        Draws the particle to the screen

        :param win: The window to draw to
        :type win: pygame.Surface
        :param color: Color of the ray
        :type color: tuple
        :param stroke: The width of the line
        :type stroke: float
        :param offset: Horizontal offset to draw too
        :type offset: float
        :return: None
        """
        pg.draw.ellipse(win, color, [self.pos.x-8+offset, self.pos.y-8, 16, 16], stroke)
        return
