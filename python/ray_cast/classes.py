from typing import List
from math import sqrt, radians, cos, sin
import pygame as pg

class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def normalize(self, scale=1):
		norm = sqrt(self.x * self.x + self.y * self.y)
		if norm != 0:
			self.x = scale * self.x / norm
			self.y = scale * self.y / norm

	def dist(self, v2):
		return sqrt((v2.x - self.x)**2 + (v2.y - self.y)**2)


class Boundary:
	def __init__(self, posA: Vector, posB: Vector):
		self.a = posA
		self.b = posB

	def draw(self, win, color=(255,255,255), stroke:int=1):
		pg.draw.line(win, color, [self.a.x, self.a.y], [self.b.x, self.b.y], stroke)

class Ray:
	def __init__(self, pos: Vector, dir: float):
		self.pos = pos
		self.dir = Vector(cos(dir), sin(dir))

	def look(self, x, y):
		self.dir.x = x - self.pos.x
		self.dir.y = y - self.pos.y
		self.dir.normalize()

	def draw(self, win, color=(255,255,255), stroke:int=1):
		draw_dir = [self.pos.x+(self.dir.x*10), self.pos.y+(self.dir.y*10),]
		pg.draw.line(win, color, [self.pos.x, self.pos.y], draw_dir, stroke)

	def cast(self, wall):
		x1 = wall.a.x
		y1 = wall.a.y
		x2 = wall.b.x
		y2 = wall.b.y

		x3 = self.pos.x
		y3 = self.pos.y
		x4 = self.pos.x + self.dir.x
		y4 = self.pos.y + self.dir.y

		den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
		if not den:
			return

		t =  ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
		u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

		if t > 0 and t < 1 and u > 0:
			pt = [0,0]
			pt[0] = x1 + t * (x2 - x1)
			pt[1] = y1 + t * (y2 - y1)
			return pt
		else:
			return

class Particle:
	def __init__(self, pos: Vector=Vector(250,250), rays: int=36):
		self.pos = pos
		self.rays = []
		for x in range(0, rays):
			self.rays.append(Ray(self.pos, radians(x*360/rays)))

	def update(self,x,y):
		self.pos = Vector(x,y)
		for ray in self.rays:
			ray.pos = self.pos

	def look(self, win, walls):
		for ray in self.rays:
			closest = None
			record = float("inf")
			for wall in walls:
				pt = ray.cast(wall)
				if pt:
					d = self.pos.dist(Vector(pt[0], pt[1]))
					if d < record:
						record = d
						closest = pt
			if closest:
				pg.draw.line(win, (255,255,255), [self.pos.x, self.pos.y], closest, 1)

	def draw(self, win, color=(255,255,255), stroke:int=0):
		pg.draw.ellipse(win, color, [self.pos.x-8,self.pos.y-8,16,16], stroke)
		for ray in self.rays:
			ray.draw(win)