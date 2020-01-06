import pygame as pg
import classes as cl
from random import randint
from math import floor
from numpy import inf

colors = [
	(0,  0,  0  ),
	(255,255,255),
	(255,0,  0  ),
	(0,  255,0  ),
	(0,  0,  255),
]

def map(x,a,b,c,d):
	return (x-a)/(b-a)*(d-c)+c

is_running = True
width = 0
mapw = 800
width2 = 1000
height = 800
window = pg.display.set_mode((width+width2,height))
pg.display.set_caption("Display Window")
clock = pg.time.Clock()
pg.font.init()
textspace = pg.font.SysFont("Fira Code", 14)

scene = []

show_map = False

while is_running:
	is_active = True
	walls = []
#	for w in range(0,5):
#		x1 = randint(5,width-5)
#		y1 = randint(5,height-5)
#		x2 = randint(5,width-5)
#		y2 = randint(5,height-5)
#		walls.append(cl.Boundary(cl.Vector(x1,y1), cl.Vector(x2,y2)))

	# Outer Walls
	walls.append(cl.Boundary(cl.Vector(0, 0), cl.Vector(0,height)))
	walls.append(cl.Boundary(cl.Vector(0, height), cl.Vector(mapw,height), (200,200,200)))
	walls.append(cl.Boundary(cl.Vector(mapw, height), cl.Vector(mapw,0)))
	walls.append(cl.Boundary(cl.Vector(mapw, 0), cl.Vector(0,0), (200,200,200)))

	# Cube In Upper Left Corner
	walls.append(cl.Boundary(cl.Vector(25,25), cl.Vector(25,75), (255,0,0)))
	walls.append(cl.Boundary(cl.Vector(25,75), cl.Vector(75,75), (0,255,0)))
	walls.append(cl.Boundary(cl.Vector(75,75), cl.Vector(75,25), (0,0,255)))
	walls.append(cl.Boundary(cl.Vector(75,25), cl.Vector(25,25)))

	# Cube In Lower Right Corner
	walls.append(cl.Boundary(cl.Vector(725,725), cl.Vector(725,775)))
	walls.append(cl.Boundary(cl.Vector(725,775), cl.Vector(775,775)))
	walls.append(cl.Boundary(cl.Vector(775,775), cl.Vector(775,725)))
	walls.append(cl.Boundary(cl.Vector(775,725), cl.Vector(725,725)))

	# Hexagon In Center
	walls.append(cl.Boundary(cl.Vector(400,290), cl.Vector(447,317), (255,0,0)))
	walls.append(cl.Boundary(cl.Vector(447,317), cl.Vector(495,345), (255,255,0)))

	walls.append(cl.Boundary(cl.Vector(495,345), cl.Vector(495,400), (0,255,0)))
	walls.append(cl.Boundary(cl.Vector(495,400), cl.Vector(495,455), (0,255,255)))

	walls.append(cl.Boundary(cl.Vector(495,455), cl.Vector(447,482), (0,0,255)))
	walls.append(cl.Boundary(cl.Vector(447,482), cl.Vector(400,510), (255,0,255)))

	walls.append(cl.Boundary(cl.Vector(400,510), cl.Vector(353,482), (255,0,0)))
	walls.append(cl.Boundary(cl.Vector(353,482), cl.Vector(305,455), (255,255,0)))

	walls.append(cl.Boundary(cl.Vector(305,455), cl.Vector(305,400), (0,255,0)))
	walls.append(cl.Boundary(cl.Vector(305,400), cl.Vector(305,345), (0,255,255)))

	walls.append(cl.Boundary(cl.Vector(305,345), cl.Vector(353,317), (0,0,255)))
	walls.append(cl.Boundary(cl.Vector(353,317), cl.Vector(400,290), (255,0,255)))

	# ??? somethin

	walls.append(cl.Boundary(cl.Vector(600, 75), cl.Vector(700, 175), (188,60,33)))
	walls.append(cl.Boundary(cl.Vector(600, 75), cl.Vector(610, 65), (188,60,33)))
	walls.append(cl.Boundary(cl.Vector(700, 175), cl.Vector(710, 165), (188,60,33)))
	walls.append(cl.Boundary(cl.Vector(710, 165), cl.Vector(610, 65), (188,60,33)))

	cam = cl.Particle(fov=70, res=4)

	w = width2 / (cam.fov*cam.res)
	tbuih = height*cam.fov
	wsq = mapw**2
	half = height/2
	bounce = 0
	b_change = 2
	b_limit = 10
	movement_speed = 3
	moveb_mult = 0.66

	paused = False

	while is_active:
		# Pause Controls
		if paused:
			for event in pg.event.get():
				if event.type == pg.QUIT:
						is_active = False
						is_running = False
						print("Goodbye!")
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_y:
						is_active = False
						is_running = False
						print("Goodbye!")
					if event.key == pg.K_n:
						paused = False
		# Normal Controls
		else:
			for event in pg.event.get():
				if event.type == pg.QUIT:
						is_active = False
						is_running = False
						print("Goodbye!")
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_RETURN:
						is_active = False
					elif event.key == pg.K_ESCAPE:
						paused = True
					elif event.key == pg.K_m:
						if show_map:
							width += mapw*-1
						else:
							width -= mapw*-1
						show_map = not show_map
						window = pg.display.set_mode((width+width2,height))
				elif event.type == pg.KEYUP and event.key in [pg.K_UP, pg.K_RIGHT, pg.K_LEFT, pg.K_DOWN]:
					bounce = 0
			# Movement
			keys = pg.key.get_pressed()
			if keys[pg.K_LEFT]:
				cam.rotate(-0.05)
				if bounce == b_limit or bounce == b_limit*-1:
					b_change *= -1
				bounce += b_change
			if keys[pg.K_RIGHT]:
				cam.rotate(0.05)
				if bounce == b_limit or bounce == b_limit*-1:
					b_change *= -1
				bounce += b_change
			if keys[pg.K_UP]:
				cam.move(movement_speed, walls)
				if bounce == b_limit or bounce == b_limit*-1:
					b_change *= -1
				bounce += b_change
			if keys[pg.K_DOWN]:
				cam.move(-movement_speed*moveb_mult, walls)
				if bounce == b_limit or bounce == b_limit*-1:
					b_change *= -1
				bounce += b_change
		
		# Move back into boundaries if left them

		if cam.pos.x >= mapw:
			cam.pos.x = mapw-movement_speed
		if cam.pos.x <= 0:
			cam.pos.x = movement_speed

		if cam.pos.y >= height:
			cam.pos.y = height-movement_speed
		if cam.pos.y <= 0:
			cam.pos.y = movement_speed


		window.fill(colors[0])

		if show_map:
			for wall in walls:
				wall.draw(window)

		pg.draw.rect(window, (50,50,50), (width, (height/2)-bounce, width2, height))

		if show_map:
			cam.draw(window)
		scene = cam.look(window, walls, show_map)

		# First Person View
		for i in range(0, len(scene)):
			if scene[i][0] > height:
				scene[i][0] = height
			sq = scene[i][0]**2
			col_r = map(sq, 0, wsq, scene[i][1][0], 0)
			col_g = map(sq, 0, wsq, scene[i][1][1], 0)
			col_b = map(sq, 0, wsq, scene[i][1][2], 0)
			h = tbuih / scene[i][0]
			to_draw = pg.Rect(0, 0, w+1, h)
			to_draw.center = ((i*w)+width, half-bounce)
			pg.draw.rect(window, (col_r,col_g,col_b), to_draw)

		# Pause Menu
		if paused:
			pg.draw.rect(window, (0,0,0), ((width+width2)*0.4,height*0.4,350,115))
			pg.draw.rect(window, (255,255,255), ((width+width2)*0.4,height*0.4,350,115), 1)
			textsurface = textspace.render('Press Y to quit, or N to cancel.', False, (255,255,255))
			window.blit(textsurface, (((width+width2)/2)*.86, (height/2)-30))

		pg.display.flip()

		clock.tick(60)

pg.quit()