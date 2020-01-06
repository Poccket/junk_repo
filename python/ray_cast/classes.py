from typing import List
from math import sqrt, radians, cos, sin, ceil
import pygame as pg
from copy import deepcopy
from sys import float_info

def colltest(a,b,c):
	crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
	# compare versus epsilon for floating point values, or != 0 if using integers
	if abs(crossproduct) > float_info.epsilon:
		return False
	dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
	if dotproduct < 0:
		return False
	squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
	if dotproduct > squaredlengthba:
		return False
	return True

class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def normalize(self, scale=1):
		norm = sqrt(self.x * self.x + self.y * self.y)
		if norm != 0:
			self.x = scale * self.x / norm
			self.y = scale * self.y / norm

	def setMag(self, n):
		self.normalize()
		self.mult(n)

	def mult(self, n):
		self.x *= n
		self.y *= n

	def dist(self, v2):
		return sqrt((v2.x - self.x)**2 + (v2.y - self.y)**2)

	def add(self, vec):
		self.x += vec.x
		self.y += vec.y

#	def setMag(self, mag):
#		self.x = x * 


class Boundary:
	def __init__(self, posA: Vector, posB: Vector, col=(255,255,255)):
		self.a = posA
		self.b = posB
		self.col = col

	def draw(self, win, stroke:int=1):
		pg.draw.line(win, self.col, [self.a.x, self.a.y], [self.b.x, self.b.y], stroke)

class Ray:
	def __init__(self, pos: Vector, dir: float):
		self.pos = pos
		self.dir = Vector(cos(dir), sin(dir))

	def setAngle(self, a):
		self.dir = Vector(cos(a), sin(a))

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
	def __init__(self, pos: Vector=Vector(250,250), fov: int=90, res: int=1):
		self.pos = pos
		self.rays = []
		self.fov = fov
		self.heading = 0
		self.res = res
		for x in range(0-(int(fov/2))*res, int(fov/2)*res):
			self.rays.append(Ray(self.pos, radians(x/res)))
		self.rotate(0)

	def move(self, amt, walls):
		vel = Vector(cos(self.heading), sin(self.heading))
		vel.setMag(amt)
		self.pos.add(vel)


	def update(self,x,y):
		self.pos = Vector(x,y)
		for ray in self.rays:
			ray.pos = self.pos

	def rotate(self,angle):
		self.heading += angle
		index = 0
		for i in range(0-(int(len(self.rays)/2)), int(len(self.rays)/2)):
			self.rays[index].setAngle(radians(i/self.res) + self.heading)
			index += 1

	def look(self, win, walls, do_draw):
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
				pg.draw.line(win, (255,255,255), [self.pos.x, self.pos.y], closest, 1)
			scene.append(record)
		return scene

	def draw(self, win, color=(255,255,255), stroke:int=0):
		pg.draw.ellipse(win, color, [self.pos.x-8,self.pos.y-8,16,16], stroke)
		for ray in self.rays:
			ray.draw(win)