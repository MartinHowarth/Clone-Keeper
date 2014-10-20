import pygame
import sys
from pygame.locals import *
import keyboard
import globals
import time


def quit():
    pygame.event.post(pygame.event.Event(QUIT))

pygame.init()

window = pygame.display.set_mode((640, 480))

glob = globals.Globals()


function_map = {'left': ((glob.left, None), {'repeat': True}),
                'right': ((glob.right, None), {'repeat': True}),
                'up': ((glob.up, None), {'repeat': True}),
                'down': ((glob.down, None), {'repeat': True}),
                'escape': ((quit, None), None),
                }

keyb = keyboard.KeyMap(function_map)

while 1:
    for event in pygame.event.get():
        # print event
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            pass
        elif event.type == KEYDOWN or event.type == KEYUP:
            keyb.receive_event(event)
            print event, str(event.key)

    keyb.receive_tick()

    window.fill((255, 255, 255))
    pygame.draw.circle(window, (0, 0, 255), (glob.x, glob.y), 20)


    pygame.display.update()
    time.sleep(1/30.0)