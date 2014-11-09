import pygame


class Tile(object):
    def __init__(self):
        self.colour = (255, 255, 255, 255)  # rgba
        self.buildable_types = []
        self.walkable_types = {'air': 1.0, 'ground': 1.0, 'underground': 1.0, 'fluid': 0.0}

    def __repr__(self):
        return self.__class__.__name__


class Grass(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.colour = (30, 255, 100, 255)
        self.buildable_types = ['air', 'ground', 'underground']


class TileSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(TileSprite, self).__init__(self)
        self.image = None