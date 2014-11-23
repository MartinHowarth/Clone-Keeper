from Vec2d import Vec2d


class PluginPosition(object):
    def __init__(self, pos=(0.0, 0.0)):
        """
        x, y are 'world positions' (float)
        screen_x, screen_y are 'screen positions' (int) (i.e. where they will be drawn in the window)
        is_screen_object = True - to ignore x, y
        :return:
        """
        self._pos = Vec2d(pos[0], pos[1])
        self._screen_pos = Vec2d(0, 0)
        self.is_screen_object = False

    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = value

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos.x = value[0]
        self._pos.y = value[1]
        self.update_screen_position()

    @property
    def screen_pos(self):
        return self._screen_pos

    def update_screen_position(self):
        """
        Upgrade this to handle camera and stuff?
        Perhaps inherit from camera object?
        This maps world position to screen position
        :return:
        """
        if self.is_screen_object:
            self._screen_pos.x = int(self._pos.x)
            self._screen_pos.y = int(self._pos.y)
        else:
            pass