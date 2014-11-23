import inspect
import types

import tile
import grid_2d


def get_classes():
    """
    Getss class objects from all imported modules (except inspect, types).
    Designed for use with loading a save state to re-create all the objects.
    :return:
    """
    modules = []
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            if val.__name__ == 'inspect' or val.__name__ == 'types':
                continue
            modules.append(val.__name__)

    classes = {}
    for module in modules:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes[name] = obj

            if name == 'get_classes':
                classes = dict(classes.items() + module.get_classes().items())

    return classes