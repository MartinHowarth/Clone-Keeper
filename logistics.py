import share
import inventory_plugin
import movement_plugin
import mailing_list
from collections import OrderedDict


class LogisticRequester(inventory_plugin.PluginInventory):
    def __init__(self, init_dict=None, position=None):
        super(LogisticRequester, self).__init__(init_dict=init_dict)
        self.mail_subscriber = mailing_list.MailListSubscriber(self)

        self._requested_items = {}
        self._in_transit_items = {}  # stuff that is on the way to this requester
        self._list_of_suppliers = {}
        # _list_of_suppliers:
        # {item_id: OrderedDict([(supplier, distance), ...])}
        self._position = position

        self.distribution_centre = None
        self._distribution_centre_distance = float('inf')
        self._find_closest_distribution_centre()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):  # when this requester moves, update ranking of suppliers
        self._position = value

        self._find_closest_distribution_centre()

        for k, v in self._list_of_suppliers.items():
            for supplier in v:
                self._update_supplier(k, supplier)

            self._sort_list_of_suppliers(k)

    def _update_supplier(self, item_id, supplier):
        sup_pos = supplier.position
        self_pos = self.position
        distance = sup_pos**2 + self_pos**2
        if distance < self._distribution_centre_distance:
            self._list_of_suppliers[item_id][supplier] = distance

    def _sort_list_of_suppliers(self, item_id):
        self._list_of_suppliers[item_id] = OrderedDict(sorted(self._list_of_suppliers[item_id].items(),
                                                              key=lambda t: t[1]))

    def _find_closest_distribution_centre(self):
        min_dist = float('inf')
        result = None
        for dc in share.distribution_centres:
            dist = self.position**2 + dc.position**2
            if dist < min_dist:
                result = dc
                min_dist = dist
        self.distribution_centre = result
        self._distribution_centre_distance = min_dist

    def _refresh_all_suppliers(self):
        for item_id, suppliers in share.suppliers:
            for sup in suppliers:
                self._update_supplier(item_id, sup)

    def receive_mail(self, mail):
        """
        Receive mail.
        This will be one of:
            - Notify of change of position / creation of logistic supplier.
        :param mail:
        :return:
        """
        if mail['request'] == 'update_supplier':
            item_id = mail.data['list']
            supplier = mail.data['supplier']

            if item_id not in self._requested_items.keys():
                return

            if item_id not in self._list_of_suppliers.keys():
                self._list_of_suppliers[item_id] = OrderedDict()

            # if position is set for this requester, then assume position is set for all
            if self.position is not None:
                self._update_supplier(item_id, supplier)
                self._sort_list_of_suppliers(item_id)
            else:  # if position is not enabled, just add to list
                self._list_of_suppliers[item_id][supplier] = None

    def add_new_request(self, item_id, amount):
        if item_id not in share.item_ids:
            raise Exception("This item ID does not exist.")
        self._requested_items[item_id] = amount

        self.calculate_and_send_new_request()

    def calculate_and_send_new_request(self):
        """
        Calculates what this inventory is lacking. Compares current items + those in transit against the requested
        amount. Calls self.send_requests(dict of items lacking).
        :return:
        """
        to_request = {}

        for item_id, requested_amount in self._requested_items.items():
            current_amount = self.get_item_count(item_id)
            if item_id in self._in_transit_items.keys():
                current_amount += self._in_transit_items[item_id]

            if current_amount >= requested_amount:
                continue
            else:
                to_request[item_id] = requested_amount - current_amount
        self.send_requests(to_request)

    def send_requests(self, to_request):
        """
        Takes in a dictionary of item_id: amount to distribute to list of known suppliers
        :param to_request:
        :return:
        """
        pass

    def update(self):
        pass


class LogisticDistributionCentre(inventory_plugin.PluginInventory):
    def __init__(self, init_dict=None):
        share.distribution_centres.add(self)
        super(LogisticDistributionCentre, self).__init__(init_dict=init_dict)
        self.mail_subscriber = mailing_list.MailListSubscriber(self)

    def receive_mail(self, mail):
        self.mail_subscriber.receive_mail(mail)


class LogisticSupplier(inventory_plugin.PluginInventory):
    def __init__(self, init_dict=None):
        super(LogisticSupplier, self).__init__(init_dict=init_dict)
        self.mail_subscriber = mailing_list.MailListSubscriber(self)

    def receive_mail(self, mail):
        self.mail_subscriber.receive_mail(mail)

    def receive_item(self, item):
        super(LogisticSupplier, self).receive_item(item)
        share.suppliers[item.id].add(self)


def create_supplier_update(supplier, item_id):
    data = {
        'list': item_id,
        'supplier': supplier,
        'request': 'update_supplier'
    }
    event = share.Event(data=data, event_type='mail')
    return event