import share


class EventDistributor(object):
    def __init__(self, targets=None):
        if targets is None:
            self.targets = {}
        else:
            self.targets = targets

    def receive_event(self, event):
        target = self.determine_target(event)
        if target in self.targets.keys():
            self.targets[target].receive_event(event)
        else:
            pass

    def determine_target(self, event):
        """
        Pulls out the required parameter from 'event' to check against known targets
        It is not advised to call super on this method.
        :param event:
        :return:
        A key to match against this classes self.targets
        Default is event.event_type
        """
        return event.event_type


class MailingListDistributor(EventDistributor):
    def determine_target(self, event):
        return event.data['list']


if __name__ == "__main__":
    import mailing_list
    share.global_event_distributor = EventDistributor()
    mailing_list_distributor = MailingListDistributor()
    share.global_event_distributor.targets['mail'] = mailing_list_distributor

    list1 = mailing_list.MailingList('test')
    sub1 = mailing_list.MailListSubscriber()

    mailing_list_distributor.targets['test'] = list1

    sub1.subscribe_to_list('test')

    print sub1.subscribed_lists
    print list1.subscribers
    for sub in list1.subscribers:
        print sub.subscribed_lists
