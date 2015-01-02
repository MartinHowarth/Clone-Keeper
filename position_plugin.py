from Vec2d import Vec2d
from plugin_plugin import Plugin


class PluginPosition(Plugin):
    def __init__(self, pos=(0.0, 0.0), init_dict=None):
        """
        x, y are 'world positions' (float)
        screen_x, screen_y are 'screen positions' (int) (i.e. where they will be drawn in the window)
        is_screen_object = True - to ignore x, y
        :return:
        """
        self._pos = Vec2d(pos[0], pos[1])
        self._screen_pos = Vec2d(0, 0)
        self.is_screen_object = False
        super(PluginPosition, self).__init__(init_dict=init_dict)

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
        self._pos = value
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
            self._screen_pos = int(self.pos)
        else:
            pass