import pickle
import os
import grid_2d


class A(object):
    def __init__(self, x):
        self.x = x
        print 'hi'


class B(object):
    def __init__(self, x):
        self.y=x


a = A(5)
b = B(10)
c = A(b)
d = B(b)
e = grid_2d.Grid2d((2,2))
e[0, 0] = 5
e[1, 0] = d

print a, b, c, a.x, b.y, c.x
print c.x, c.x.y
print d.y, d.y.y

print c.x == b, d.y == b
with open(os.getcwd() + '/saves/default0.txt', 'wb') as f:
    pickle.dump([a, b, c, d, e], f, protocol=2)

with open(os.getcwd() + '/saves/default0.txt', 'rb') as f:
    a, b, c, d, e = pickle.load(f)


print a, b, c, a.x, b.y, c.x, c.x.y
print c.x, c.x.y
print d.y, d.y.y
print c.x == b, d.y == b
print e
print e[1, 0] == d
