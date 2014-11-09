import pygame


class Graphics(object):
    def __init__(self):
        self._screen_size = self._screen_width, self._screen_height = 640, 480
        self._fullscreen = False
        self._borderless = False

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        self._fullscreen = value
        self._set_screen_mode()

    @property
    def borderless(self):
        return self._borderless

    @borderless.setter
    def borderless(self, value):
        self._borderless = value
        self._set_screen_mode()

    @property
    def screen_size(self):
        return self._screen_size

    @screen_size.setter
    def screen_size(self, value):
        self._screen_size = value
        self._set_screen_mode()

    @property
    def screen_width(self):
        return self._screen_width

    @screen_width.setter
    def screen_width(self, value):
        self._screen_width = value
        self.screen_size = (self._screen_width, self._screen_height)

    @property
    def screen_height(self):
        return self._screen_height

    @screen_height.setter
    def screen_height(self, value):
        self._screen_height = value
        self.screen_size = (self._screen_width, self._screen_height)

    def _set_screen_mode(self):
        flags = 0
        if self._fullscreen:
            flags = flags | pygame.FULLSCREEN
        if self._borderless:
            flags = flags | pygame.NOFRAME
        self.screen = pygame.display.set_mode(self._screen_size, flags)