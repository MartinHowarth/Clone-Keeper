from pygame.locals import *


class KeyBind:
    """
    Maps a key to a function. Optionally passes in function_parameters as a dict of keyword: value pairs.
    """
    def __init__(self, function=None, key=None, function_parameters=None, name='default'):
        self.function_down = function[0]
        self.function_up = function[1]
        self.name = name
        self.key = key
        self.repeat = False
        self.first_press = True
        if function_parameters:
            if 'repeat' in function_parameters.keys():
                self.repeat = function_parameters['repeat']
                del function_parameters['repeat']
        self.function_parameters = function_parameters

    def key_down(self):
        if self.repeat:
            self.execute_down()
        else:
            if self.first_press:
                self.execute_down()
                self.first_press = False

    def key_up(self):
        self.first_press = True
        self.execute_up()

    def execute_up(self):
        if self.function_up:
            if self.function_parameters:
                self.function_up(**self.function_parameters)
            else:
                self.function_up()

    def execute_down(self):
        if self.function_down:
            if self.function_parameters:
                self.function_down(**self.function_parameters)
            else:
                self.function_down()

    def __repr__(self):
        return 'Key:' + repr(self.key) + '\n\tUp Function:' + repr(self.function_up) + '\n\tDown Function:' + repr(self.function_down)


class KeyMap:
    """
    KeyBind container, KeyBinds are stored as lists for their respective letter in a dict.
    e.g. KEY_K: [KeyBind1, KeyBind2]

    Expects input of function_map = {'key_name': <function>}
    """
    def __init__(self, function_map):
        self.map = {}
        self.function_map = function_map
        self.currently_down = set()
        self.load_from_file()

    def receive_event(self, event):
        if not event.key in self.map.keys():
            return

        if event.type == KEYDOWN:
            self.currently_down.add(event.key)
        elif event.type == KEYUP:
            self.currently_down.discard(event.key)
            for key_bind in self.map[event.key]:
                key_bind.key_up()

    def receive_tick(self):
        for key in self.currently_down:
            for key_bind in self.map[key]:
                key_bind.key_down()

    def load_from_file(self):
        f = open("config/keybind.txt", 'r')
        for l in f:
            name = l[:l.find(':')].rstrip()
            key = int(l[l.find(':') + 1:].rstrip())

            function = self.function_map[name][0]
            function_parameters = self.function_map[name][1]

            if key in self.map.keys():
                self.map[key].append(KeyBind(function, key, function_parameters, name))
            else:
                self.map[key] = [KeyBind(function, key, function_parameters, name)]

        f.close()

    def save_to_file(self):
        f = open("config/keybind.txt", 'w')
        for key, bind in self.map.iteritems():
            for b in bind:
                f.writelines(str(b.name) + ':' + str(key) + '\n')

        f.close()