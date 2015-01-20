import inspect
import copy


class Plugin(object):
    def __init__(self, init_dict=None):
        self.load_from_dict(init_dict)

    def load_from_dict(self, dic):
        if dic is None:
            return
        for k, v in dic.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise Exception('Invalid input parameter: ' + str(k))
