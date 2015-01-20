global_event_distributor = None
item_ids = set()
# suppliers is a dict of item_id: set([suppliers of item_id])
suppliers = {}
# distribution_centres is a list of all distribution centres
distribution_centres = set()


class Event(object):
    def __init__(self, data=None, event_type=None):
        """
        :param data: Information to be passed
        :param event_type: Likely to be the parameter used to route this event
        :return:
        """
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.event_type = event_type


def receive_event(event):
    print event, global_event_distributor
    if global_event_distributor is not None:
        global_event_distributor.receive_event(event)