import argparse
import logging
import sys
import pygame
import importlib

import classes as cl
import helper as hl

parser = argparse.ArgumentParser(description="Raycasting program.")
parser.add_argument('--height', help='Height of first person viewport',
                    type=int, default=800)
parser.add_argument('--width', help='Width of first person viewport',
                    type=int, default=800)
parser.add_argument('-f', '--fov', help='Angle of field of view and initial raycount',
                    type=int, default=60)
parser.add_argument('-r', '--res', help='Amount to multiply raycount by',
                    type=int, default=1)
parser.add_argument('-m', '--map', help='Map file to import',
                    type=str, default="maps.map_test01")
parser.add_argument('-n', '--noclip', help='Noclip',
                    action='store_true')
parser.add_argument('-v', '--verbose', help='Prints verbose messages',
                    action='store_true')
parser.add_argument('-d', '--debug', help='Prints debug messages',
                    action='store_true')
args = parser.parse_args()

logging.basicConfig(stream=sys.stderr, level=(10 if args.debug else (20 if args.verbose else 30)))

noclip = args.noclip
scr_height = args.height
scr_width = args.width
logging.info('Got viewport dimensions from parse_args, %dx%d.' % (scr_width, scr_height))

map = importlib.import_module(args.map)

mapview_width = 0

window = pygame.display.set_mode((mapview_width + scr_width, scr_height + 20))
pygame.display.set_caption("Display Window")
logging.debug('Initiated pygame window. Dimensions: %dx%d.' % pygame.display.get_surface().get_size())
clock = pygame.time.Clock()
pygame.font.init()
textspace = pygame.font.SysFont("Fira Code", 14)


scene = []
show_map = False
is_active = True

cam = cl.Particle(pos=map.spawn, fov=args.fov, res=args.res)
logging.debug('Initiated player camera.')

w = scr_width / (cam.fov * cam.res)
tbuih = scr_height * cam.fov
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
                        mapview_width += map.width * -1
                    else:
                        mapview_width -= map.width * -1
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
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            cam.rotate(-0.05)
            if bounce == b_limit or bounce == b_limit * -1:
                b_change *= -1
            bounce += b_change
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            cam.rotate(0.05)
            if bounce == b_limit or bounce == b_limit * -1:
                b_change *= -1
            bounce += b_change
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            cam.move(movement_speed)
            can_move = True
            if not noclip:
                for wall in map.walls:
                    for hitline in [[cl.Vector(round(cam.pos.x)-2, round(cam.pos.y)-2),
                                     cl.Vector(round(cam.pos.x)-2, round(cam.pos.y)+2)],
                                    [cl.Vector(round(cam.pos.x)-2, round(cam.pos.y)+2),
                                     cl.Vector(round(cam.pos.x)+2, round(cam.pos.y)+2)],
                                    [cl.Vector(round(cam.pos.x)+2, round(cam.pos.y)+2),
                                     cl.Vector(round(cam.pos.x)+2, round(cam.pos.y)-2)],
                                    [cl.Vector(round(cam.pos.x)+2, round(cam.pos.y)-2),
                                     cl.Vector(round(cam.pos.x)-2, round(cam.pos.y)-2)]]:
                        if not wall.clip:
                            continue
                        h = hl.segintersect(hitline[0], hitline[1], wall.a, wall.b)
                        if h:
                            logging.debug("intersection:", h,
                                          "\na1:", hitline[0].x, "x /", hitline[0].y,
                                          "y, a2:", hitline[1].x, "x /", hitline[1].y,
                                          "y\nb1:", wall.a.x, "x /", wall.a.y,
                                          "y, b2:", wall.b.x, "x /", wall.b.y, "y")
                            can_move = False
                            break
                    if not can_move:
                        cam.move(-movement_speed)
                        break
            if bounce == b_limit or bounce == b_limit * -1:
                b_change *= -1
            bounce += b_change
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            cam.move(-movement_speed * moveb_mult)
            can_move = True
            if not noclip:
                for wall in map.walls:
                    for hitline in [[cl.Vector(round(cam.pos.x) - 2, round(cam.pos.y) - 2),
                                     cl.Vector(round(cam.pos.x) - 2, round(cam.pos.y) + 2)],
                                    [cl.Vector(round(cam.pos.x) - 2, round(cam.pos.y) + 2),
                                     cl.Vector(round(cam.pos.x) + 2, round(cam.pos.y) + 2)],
                                    [cl.Vector(round(cam.pos.x) + 2, round(cam.pos.y) + 2),
                                     cl.Vector(round(cam.pos.x) + 2, round(cam.pos.y) - 2)],
                                    [cl.Vector(round(cam.pos.x) + 2, round(cam.pos.y) - 2),
                                     cl.Vector(round(cam.pos.x) - 2, round(cam.pos.y) - 2)]]:
                        if not wall.clip:
                            continue
                        h = hl.segintersect(hitline[0], hitline[1], wall.a, wall.b)
                        if h:
                            logging.debug("intersection:", h,
                                          "\na1:", hitline[0].x, "x /", hitline[0].y,
                                          "y, a2:", hitline[1].x, "x /", hitline[1].y,
                                          "y\nb1:", wall.a.x, "x /", wall.a.y,
                                          "y, b2:", wall.b.x, "x /", wall.b.y, "y")
                            can_move = False
                            break
                    if not can_move:
                        cam.move(movement_speed * moveb_mult)
                        break
            if bounce == b_limit or bounce == b_limit * -1:
                b_change *= -1
            bounce += b_change

    # Move back into boundaries if left them
    cam.pos.x = max(movement_speed, min(cam.pos.x, map.width - movement_speed))
    cam.pos.y = max(movement_speed, min(cam.pos.y, map.height - movement_speed))

    # Reset window
    window.fill(map.sky)
    pygame.draw.rect(window, map.floor, (0, (scr_height / 2) - bounce, scr_width, scr_height))
    scene = cam.look(window, map.walls, show_map, offset=scr_width)

    # First Person View
    for i, item in enumerate(scene):
        if item[0] > scr_height:
            item[0] = scr_height
        sq = item[0]**2
        col_r = hl.map(sq, 0, map.r_distance, item[1][0], map.r_color[0])
        col_g = hl.map(sq, 0, map.r_distance, item[1][1], map.r_color[1])
        col_b = hl.map(sq, 0, map.r_distance, item[1][2], map.r_color[2])
        h = tbuih / item[0]
        to_draw = pygame.Rect(0, 0, w + 1, h)
        to_draw.center = ((i * w), half - bounce)

        col_r = col_r if col_r > 0 else 0
        col_g = col_g if col_g > 0 else 0
        col_b = col_b if col_b > 0 else 0

        pygame.draw.rect(window, (col_r, col_g, col_b), to_draw)

    if show_map:
        pygame.draw.rect(window, (0, 0, 0), (scr_width, 0, scr_height, mapview_width))
        cam.draw(window, offset=scr_width)
        for wall in map.walls:
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
