def enumerate_grid(grid):
    for i, element in enumerate(grid):
        yield (i % grid.x, i / grid.x), element


class Grid2d(object):
    def __init__(self, dimensions=(10, 10)):
        self._dimensions = dimensions
        self._grid = [[None for i in range(dimensions[0])] for j in range(dimensions[1])]

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def x(self):
        return self._dimensions[0]

    @property
    def y(self):
        return self._dimensions[1]

    def __getitem__(self, item):
        if type(item) == slice:
            x1, y1 = item.start
            x2, y2 = item.stop
            return_grid = Grid2d((x2 - x1, y2 - y1))
            for i, x in enumerate(range(x1, x2)):
                for j, y in enumerate(range(y1, y2)):
                    return_grid[i, j] = self[x, y]
            return return_grid
        else:
            x, y = item
            return self._grid[y][x]

    def __setitem__(self, key, value):
        x, y = key
        self._grid[y][x] = value

    def __iter__(self):
        for row in self._grid:
            for value in row:
                yield value

    def __len__(self):
        return self.dimensions

    def __repr__(self):
        return self.represent()

    def resize(self, new_dimensions):
        new_grid = [[None for i in range(new_dimensions[0])] for j in range(new_dimensions[1])]
        for i, row in enumerate(self._grid):
            for j, val in enumerate(row):
                if i < new_dimensions[1] and j < new_dimensions[0]:
                    new_grid[i][j] = val

        self._grid = new_grid
        self._dimensions = new_dimensions

    def represent(self, x_range=None, y_range=None, length=4):
        if x_range is None and y_range is None:  # if printing entire grid, do this
            to_print = ''
            for row in self._grid:
                row_print = ''
                for value in row:
                    p_val = repr(value)[:length]
                    p_val += ' ' * (length - len(p_val))  # make sure each entry is precisely <length> characters
                    row_print += p_val + '\t'
                to_print += row_print + '\n'

            return to_print
        else:  # if printing sub-grid, print a sliced version of this grid
            x1, x2 = x_range
            y1, y2 = y_range
            return self[(x1, y1):(x2, y2)].represent(length=length)

    def populate(self, obj_type, kwargs=None, x_range=None, y_range=None):
        if x_range is None:
            x_r = 0, self.x
        else:
            x_r = x_range
        if y_range is None:
            y_r = 0, self.y
        else:
            y_r = y_range
        for x in range(*x_r):
            for y in range(*y_r):
                if kwargs is None:
                    self[x, y] = obj_type()
                else:
                    self[x, y] = obj_type(**kwargs)


class GridVector(object):
    def __init__(self, x, y=None):
        if y is None:  # initialise with tuple or list
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        return GridVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return GridVector(self.x - other.x, self.y - other.y)

# def range_2d(x, y):
#     for i in range(x):
#         for j in range(y):
#             yield (i, j)
#
#
# g = Grid2d()
# for pos in range_2d(5, 10):
#     g[pos] = pos[0] + 10 * pos[1]
# print g
# print g[(0, 1): (3,3)]
# print g.represent((1, 3), (0, 3))