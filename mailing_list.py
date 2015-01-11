import share


class MailingList(object):
    def __init__(self, identifier):
        self.subscribers = set()
        self.identifier = identifier

    def receive_mail(self, mail):
        """
        Receives an event (mail).
        Either keeps it (e.g. a subscribe or unsubscribe request
        Or distributes it.
        :param mail:
        :return:
        """
        sub = mail.data['subscriber']
        request = mail.data['request']
        if request == 'subscribe':
            self.subscribers.add(sub)
        elif request == 'unsubscribe':
            self.subscribers.remove(sub)

    def distribute_mail(self, mail):
        for sub in self.subscribers:
            sub.receive_mail(mail)

    def receive_event(self, event):
        self.receive_mail(event)


class MailListSubscriber(object):
    def __init__(self):
        self._subscribed_lists = {}

    @property
    def subscribed_lists(self):
        return self._subscribed_lists

    def subscribe_to_list(self, list_identifier):
        if list_identifier not in self._subscribed_lists.keys():
            request = create_subscribe_request(self, list_identifier)
            share.receive_event(request)
            self._subscribed_lists[list_identifier] = list_identifier
        else:
            print "Already subscribed to list %s", list_identifier

    def unsubscribe_from_list(self, list_identifier):
        if list_identifier in self._subscribed_lists.keys():
            request = create_unsubscribe_request(self, list_identifier)
            share.receive_event(request)
            del self._subscribed_lists[list_identifier]
        else:
            print 'Cannot unsubscribe, not a member of %s list', list_identifier

    def receive_mail(self, mail):
        pass


def create_subscribe_request(subscriber, list_identifier):
    data = {
        'subscriber': subscriber,
        'list': list_identifier,
        'request': 'subscribe'
    }
    event = share.Event(data=data, event_type='mail')
    return event


def create_unsubscribe_request(subscriber, list_identifier):
    data = {
        'subscriber': subscriber,
        'list': list_identifier,
        'request': 'unsubscribe'
    }
    event = share.Event(data=data, event_type='mail')
    return event


if __name__ == "__main__":
    pass