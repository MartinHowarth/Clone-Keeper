import pygame
import sys

pygame.init()

window = pygame.display.set_mode((640, 480))

pygame.draw.circle(window, (0, 0, 255), (10, 10), 20)

pygame.display.update()

while 1:
    for event in pygame.event.get():
        print event
        if event.type == 12:  # quit
            pygame.quit()
            sys.exit()
        elif event.type == 1:
            pass
