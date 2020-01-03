import pygame as pg
import classes as cl
from random import randint

colors = [
	(0,  0,  0  ),
	(255,255,255),
	(255,0,  0  ),
	(0,  255,0  ),
	(0,  0,  255),
]

is_running = True
width = 1000
height = 1000
window = pg.display.set_mode((width,height))
pg.display.set_caption("Display Window")
clock = pg.time.Clock()

while is_running:
	is_active = True
	walls = []
	for w in range(0,5):
		x1 = randint(5,width-5)
		y1 = randint(5,height-5)
		x2 = randint(5,width-5)
		y2 = randint(5,height-5)
		walls.append(cl.Boundary(cl.Vector(x1,y1), cl.Vector(x2,y2)))
	walls.append(cl.Boundary(cl.Vector(0, 0), cl.Vector(0,height)))
	walls.append(cl.Boundary(cl.Vector(0, height), cl.Vector(width,height)))
	walls.append(cl.Boundary(cl.Vector(width, height), cl.Vector(width,0)))
	walls.append(cl.Boundary(cl.Vector(width, 0), cl.Vector(0,0)))

	cam = cl.Particle(rays=360)

	while is_active:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				is_active = False
				is_running = False
				print("Goodbye!")
			elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
				is_active = False

		window.fill(colors[0])

		for wall in walls:
			wall.draw(window)

		mouse_x, mouse_y = pg.mouse.get_pos()
		cam.update(mouse_x,mouse_y)
		cam.draw(window)
		cam.look(window, walls)

		pg.display.flip()

		clock.tick(60)

pg.quit()