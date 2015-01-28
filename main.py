import pygame
import sys
from pygame.locals import *
import keyboard
import share
import time
import os
import pickle

import grid_2d
import tile


def save(to_save, save_file=None):
    if save_file is None:  # if save_file name not specified, find next available default name
        current_saves = os.listdir(os.getcwd() + "/saves")
        min_default = 0
        for sav in current_saves:
            if 'default' in sav:
                num = int(sav[sav.index('t') + 1:][:-4])  # get number from default<num>.sav
                if num >= min_default:
                    min_default = num + 1
        save_file = 'default' + str(min_default) + '.sav'

    with open(os.getcwd() + '/saves/' + save_file, 'wb') as f:
        pickle.dump(to_save, f, protocol=2)


def load(save_file='default1.sav'):
    with open(os.getcwd() + '/saves/' + save_file, 'rb') as f:
        loaded = pickle.load(f)
    return loaded


def _quit():
    pygame.event.post(pygame.event.Event(QUIT))


def draw_grid(_grid, tile_size=(20, 20)):
    dx = tile_size[0] * _grid.x
    dy = tile_size[1] * _grid.y
    surf = pygame.Surface((dx, dy))
    for ind, elem in grid_2d.enumerate_grid(_grid):
        x = ind[0] * tile_size[0]
        y = ind[1] * tile_size[1]
        rec = pygame.Rect((x, y), tile_size)
        if elem is not None:
            pygame.draw.rect(surf, elem.colour, rec)
    return surf


def add_grass(_grid, location):
    x = location[0] / 20
    y = location[1] / 20
    _grid[x, y] = tile.Grass()

pygame.init()

window = pygame.display.set_mode((640, 480))

glob = share.Globals()

to_save = []


keybind_function_map = {'left': ((glob.left, None), {'repeat': True}),
                        'right': ((glob.right, None), {'repeat': True}),
                        'up': ((glob.up, None), {'repeat': True}),
                        'down': ((glob.down, None), {'repeat': True}),
                        'escape': ((_quit, None), None),
                        }

keyb = keyboard.KeyMap(keybind_function_map)

grid = grid_2d.Grid2d()
grid.populate(tile.Grass, {}, (1, 5), (1, 4))
print grid

to_save.append(grid)

while 1:
    for event in pygame.event.get():
        # print event
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            pass
        elif event.type == MOUSEBUTTONDOWN:
            add_grass(grid, event.coord)

        elif event.type == KEYDOWN or event.type == KEYUP:
            keyb.receive_event(event)
            print event, str(event.key)
            if event.key == pygame.K_s and event.type == KEYDOWN:
                print 'Saving...'
                save([grid], 'default1.sav')
            if event.key == pygame.K_l:
                print 'Loading...'
                grid, = load()

    keyb.receive_tick()

    window.fill((255, 255, 255))

    window.blit(draw_grid(grid), (0, 0))
    pygame.draw.circle(window, (0, 0, 255), (glob.x, glob.y), 10)


    pygame.display.update()
    time.sleep(1/30.0)