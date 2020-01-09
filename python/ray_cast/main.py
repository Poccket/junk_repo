import argparse
import logging
import sys
import pygame

import classes as cl
import helper as hl

parser = argparse.ArgumentParser(description="Raycasting program.")
parser.add_argument('-v', '--verbose', help='Prints verbose messages',
                    action='store_true')
parser.add_argument('-d', '--debug', help='Prints debug messages',
                    action='store_true')
parser.add_argument('--height', help='Height of first person viewport',
                    type=int, default=800)
parser.add_argument('--width', help='Width of first person viewport',
                    type=int, default=800)
parser.add_argument('--fov', help='Angle of field of view and initial raycount',
                    type=int, default=60)
parser.add_argument('--res', help='Amount to multiply raycount by',
                    type=int, default=1)
args = parser.parse_args()

logging.basicConfig(stream=sys.stderr, level=(10 if args.debug else (20 if args.verbose else 30)))

scr_height = args.height
scr_width = args.width
logging.info('Got viewport dimensions from parse_args, %dx%d.' % (scr_width, scr_height))

mapview_width = 0
mapw = 800
maph = 800

window = pygame.display.set_mode((mapview_width + scr_width, scr_height + 20))
pygame.display.set_caption("Display Window")
logging.debug('Initiated pygame window. Dimensions: %dx%d.' % pygame.display.get_surface().get_size())
clock = pygame.time.Clock()
pygame.font.init()
textspace = pygame.font.SysFont("Fira Code", 14)


scene = []

show_map = False

is_active = True
walls = [
    # Map boundaries
    cl.Boundary(cl.Vector(0, 0), cl.Vector(0, maph)),
    cl.Boundary(cl.Vector(0, maph), cl.Vector(mapw, maph), (200, 200, 200)),
    cl.Boundary(cl.Vector(mapw, maph), cl.Vector(mapw, 0)),
    cl.Boundary(cl.Vector(mapw, 0), cl.Vector(0, 0), (200, 200, 200)),

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
logging.debug('Wall setup complete, wall count: %d.' % len(walls))

cam = cl.Particle(pos=cl.Vector(250, 250), fov=args.fov, res=args.res)
logging.debug('Initiated player camera.')

w = scr_width / (cam.fov * cam.res)
tbuih = scr_height * cam.fov
wsq = mapw**2
half = scr_height / 2
bounce = 0
b_change = 2
b_limit = 10
movement_speed = 3
moveb_mult = 0.66

paused = False
while is_active:
    # Pause Controls
    if paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Window closed, quitting.")
                print("Goodbye!")
                is_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    logging.info("Closed from pause menu.")
                    print("Goodbye!")
                    is_active = False
                if event.key == pygame.K_n:
                    logging.info("Unpaused.")
                    paused = False
        continue
    # Normal Controls
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Window closed, quitting.")
                print("Goodbye!")
                is_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    logging.info("Paused.")
                    paused = True
                    continue
                elif event.key == pygame.K_m:
                    logging.info("Map closed." if show_map else "Map opened.")
                    if show_map:
                        mapview_width += mapw * -1
                    else:
                        mapview_width -= mapw * -1
                    show_map = not show_map
                    window = pygame.display.set_mode((mapview_width + scr_width, scr_height + 20))
                    logging.debug('New screen dimensions: %dx%d.' % pygame.display.get_surface().get_size())
            elif event.type == pygame.KEYUP and event.key in [
                pygame.K_UP, pygame.K_RIGHT,
                pygame.K_LEFT, pygame.K_DOWN
            ]:
                bounce = 0

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cam.rotate(-0.05)
            if bounce == b_limit or bounce == b_limit * -1:
                b_change *= -1
            bounce += b_change
        if keys[pygame.K_RIGHT]:
            cam.rotate(0.05)
            if bounce == b_limit or bounce == b_limit * -1:
                b_change *= -1
            bounce += b_change
        if keys[pygame.K_UP]:
            cam.move(movement_speed)
            if bounce == b_limit or bounce == b_limit * -1:
                b_change *= -1
            bounce += b_change
        if keys[pygame.K_DOWN]:
            cam.move(-movement_speed * moveb_mult)
            if bounce == b_limit or bounce == b_limit * -1:
                b_change *= -1
            bounce += b_change

    # Move back into boundaries if left them
    cam.pos.x = max(movement_speed, min(cam.pos.x, mapw - movement_speed))
    cam.pos.y = max(movement_speed, min(cam.pos.y, maph - movement_speed))

    # Reset window
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (50, 50, 50), (0, (scr_height / 2) - bounce, scr_width, scr_height))
    scene = cam.look(window, walls, show_map, offset=scr_width)

    # First Person View
    for i, item in enumerate(scene):
        if item[0] > scr_height:
            item[0] = scr_height
        sq = item[0]**2
        col_r = hl.map(sq, 0, wsq, item[1][0], 0)
        col_g = hl.map(sq, 0, wsq, item[1][1], 0)
        col_b = hl.map(sq, 0, wsq, item[1][2], 0)
        h = tbuih / item[0]
        to_draw = pygame.Rect(0, 0, w + 1, h)
        to_draw.center = ((i * w), half - bounce)

        col_r = col_r if col_r > 0 else 0
        col_g = col_g if col_g > 0 else 0
        col_b = col_b if col_b > 0 else 0

        pygame.draw.rect(window, (col_r, col_g, col_b), to_draw)

    if show_map:
        cam.draw(window, offset=scr_width)
        for wall in walls:
            wall.draw(window, offset=scr_width)

    # Pause Menu
    if paused:
        pygame.draw.rect(window, (0, 0, 0), ((mapview_width + scr_width) * 0.4, scr_height * 0.4, 350, 115))
        pygame.draw.rect(window, (255, 255, 255), ((mapview_width + scr_width) * 0.4, scr_height * 0.4, 350, 115), 1)
        text_quit = textspace.render('Press Y to quit, or N to cancel.', False, (255, 255, 255))
        window.blit(text_quit, (((mapview_width + scr_width) / 2) * .86, (scr_height / 2) - 30))

    pygame.draw.rect(window, (0, 0, 0), (0, scr_height, mapview_width + scr_width, 20))
    pygame.draw.line(window, (255, 255, 255), [0, scr_height], [mapview_width + scr_width, scr_height], 1)

    textcont = textspace.render('Press M to open map. Press ESC to leave.', False, (255, 255, 255))
    window.blit(textcont, (0, scr_height + 2))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
