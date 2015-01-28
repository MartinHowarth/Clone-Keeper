from Vec2d import Vec2d
from plugin_plugin import Plugin
import math


class PluginPosition(Plugin):
    def __init__(self, pos=(0.0, 0.0), init_dict=None):
        """
        x, y are 'world positions' (float)
        screen_x, screen_y are 'screen positions' (int) (i.e. where they will be drawn in the window)
        is_screen_object = True - to ignore x, y
        :return:
        """
        self._coord = Vec2d(pos[0], pos[1])
        self._screen_pos = Vec2d(0, 0)
        self.is_screen_object = False
        super(PluginPosition, self).__init__(init_dict=init_dict)

    @property
    def x(self):
        return self.coord.x

    @x.setter
    def x(self, value):
        self.coord.x = value

    @property
    def y(self):
        return self.coord.y

    @y.setter
    def y(self, value):
        self.coord.y = value

    @property
    def coord(self):
        return self._coord

    @coord.setter
    def coord(self, value):
        self._coord = value
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
            self._screen_pos = int(self.coord)
        else:
            pass

    def get_distance_from(self, other):
        """
        Returns the square root of self.get_distance_from_squared(other).
        :param other:
        :return:
        """
        return math.sqrt(self.get_distance_from_squared(other))

    def get_distance_from_squared(self, other):
        """
        Find distance between this position object and another position object.
        Use this instead of get_distance_from when exact distance doesn't matter.
        :param other: Another position/movement object, or a Vec2d object
        :return: Distance squared.
        """
        if hasattr(other, '_coord'):
            dx = self.x - other.x
            dy = self.y - other.y
            dist = dx**2 + dy**2
            return dist
        elif type(other, Vec2d):
            dx = self.x - other[0]
            dy = self.y - other[1]
            dist = dx**2 + dy**2
            return dist