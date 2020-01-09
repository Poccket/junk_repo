from typing import List
from math import sqrt, radians, cos, sin, ceil
import pygame as pg
import helper as hl


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def normalize(self, scale: float = 1):
        norm = sqrt(self.x * self.x + self.y * self.y)
        if norm != 0:
            self.x = scale * self.x / norm
            self.y = scale * self.y / norm

    def setmag(self, n: float):
        self.normalize()
        self.mult(n)

    def mult(self, n: float):
        self.x *= n
        self.y *= n

    def dist(self, v2: "Vector"):
        return sqrt((v2.x - self.x)**2 + (v2.y - self.y)**2)

    def add(self, vec: "Vector"):
        self.x += vec.x
        self.y += vec.y


class Boundary:
    def __init__(self, posa: Vector, posb: Vector, col: tuple = (255, 255, 255)):
        self.a = posa
        self.b = posb
        self.col = col

    def draw(self, win: pg.Surface, stroke: float = 1, offset: float = 0):
        pg.draw.line(win, self.col, [self.a.x+offset, self.a.y], [self.b.x+offset, self.b.y], stroke)


class Ray:
    def __init__(self, pos: Vector, ang: float):
        self.pos = pos
        self.ang = Vector(cos(ang), sin(ang))

    def setangle(self, a: float):
        self.ang = Vector(cos(a), sin(a))

    def look(self, x: float, y: float):
        self.ang.x = x - self.pos.x
        self.ang.y = y - self.pos.y
        self.ang.normalize()

    def draw(self, win: pg.Surface, color: tuple = (255, 255, 255), stroke: float = 1):
        draw_dir = [self.pos.x + (self.ang.x * 10), self.pos.y + (self.ang.y * 10), ]
        pg.draw.line(win, color, [self.pos.x, self.pos.y], draw_dir, stroke)

    def cast(self, wall: Boundary):
        return hl.intersect(wall.a, wall.b, self.pos, Vector(self.pos.x + self.ang.x, self.pos.y + self.ang.y))


class Particle:
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
        vel = Vector(cos(self.heading), sin(self.heading))
        vel.setmag(amt)
        self.pos.add(vel)

    def update(self, x: float, y: float):
        self.pos = Vector(x, y)
        for ray in self.rays:
            ray.pos = self.pos

    def rotate(self, angle: float):
        self.heading += angle
        index = 0
        for i in range(0-(int(len(self.rays)/2)), int(len(self.rays)/2)):
            self.rays[index].setangle(radians(i / self.res) + self.heading)
            index += 1

    def look(self, win: pg.Surface, walls: List[Boundary], do_draw: bool, offset: float = 0):
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
        pg.draw.ellipse(win, color, [self.pos.x-8+offset, self.pos.y-8, 16, 16], stroke)
        pg.draw.rect(win, color, (self.pos.x-4+offset, self.pos.y-4, 8, 8), 1)
