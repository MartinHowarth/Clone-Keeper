import pygame
import sys
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((640, 480))


x, y = 10, 10
pos = x, y

while 1:
    for event in pygame.event.get():
        # print event
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            pass
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                x -= 10
            elif event.key == K_RIGHT:
                x += 10
            elif event.key == K_DOWN:
                y += 10
            elif event.key == K_UP:
                y -= 10

            elif event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

        window.fill((255, 255, 255))
        pygame.draw.circle(window, (0, 0, 255), (x, y), 20)


        pygame.display.update()