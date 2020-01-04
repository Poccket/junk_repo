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
width = 400
width2 = 400
height = 400
window = pg.display.set_mode((width+width2,height))
pg.display.set_caption("Display Window")
clock = pg.time.Clock()

scene = []

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
	walls.append(cl.Boundary(cl.Vector(0, height), cl.Vector(width,height)))
	walls.append(cl.Boundary(cl.Vector(width, height), cl.Vector(width,0)))
	walls.append(cl.Boundary(cl.Vector(width, 0), cl.Vector(0,0)))

	# Cube In Upper Left Corner
	walls.append(cl.Boundary(cl.Vector(25,25), cl.Vector(25,75)))
	walls.append(cl.Boundary(cl.Vector(25,75), cl.Vector(75,75)))
	walls.append(cl.Boundary(cl.Vector(75,75), cl.Vector(75,25)))
	walls.append(cl.Boundary(cl.Vector(75,25), cl.Vector(25,25)))

	# Cube In Lower Right Corner
	walls.append(cl.Boundary(cl.Vector(325,325), cl.Vector(325,375)))
	walls.append(cl.Boundary(cl.Vector(325,375), cl.Vector(375,375)))
	walls.append(cl.Boundary(cl.Vector(375,375), cl.Vector(375,325)))
	walls.append(cl.Boundary(cl.Vector(375,325), cl.Vector(325,325)))

	# Hexagon In Center
	walls.append(cl.Boundary(cl.Vector(200,175), cl.Vector(175, 200)))
	walls.append(cl.Boundary(cl.Vector(200,175), cl.Vector(225, 200)))
	walls.append(cl.Boundary(cl.Vector(175,200), cl.Vector(185,225)))
	walls.append(cl.Boundary(cl.Vector(225,200), cl.Vector(215,225)))
	walls.append(cl.Boundary(cl.Vector(215,225), cl.Vector(185,225)))

	p_fov = 60
	cam = cl.Particle(fov=p_fov)

	while is_active:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				is_active = False
				is_running = False
				print("Goodbye!")
			elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
				is_active = False
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			cam.rotate(-0.05)
		if keys[pg.K_RIGHT]:
			cam.rotate(0.05)
		if keys[pg.K_UP]:
			cam.move(2)
		if keys[pg.K_DOWN]:
			cam.move(-2)
		
		window.fill(colors[0])

		for wall in walls:
			wall.draw(window)

		pg.draw.rect(window, (50,50,50), (width, height/2, width*2, height))

		mouse_x, mouse_y = pg.mouse.get_pos()
		if mouse_x > width:
			mouse_x = width
		#cam.update(mouse_x,mouse_y)
		cam.draw(window)
		scene = cam.look(window, walls)

		w = width2 / p_fov
		for i in range(0, len(scene)):
			if scene[i] > height:
				scene[i] = height
			sq = scene[i]**2
			wsq = width**2
			b = map(sq, 0, wsq, height, 0)
			#h = map(scene[i], 0, width2, height, 0)
			h = height * p_fov / scene[i]
			col = b*0.63
			if col > 255:
				col = 255
			to_draw = pg.Rect(0, 0, w+1, h)
			#to_draw = pg.Rect(i*w+w/2, height/2, w+1, 10*200/scene[i])
			#to_draw = pg.Rect(0, 0, w+1, 10*200/scene[i])
			to_draw.center = ((i*w)+width, height/2)
			pg.draw.rect(window, (col,col,col), to_draw)

		pg.display.flip()

		clock.tick(60)

pg.quit()