import share
import inventory_plugin
import movement_plugin
import mailing_list
from collections import OrderedDict


class LogisticRequester(inventory_plugin.PluginInventory):
    def __init__(self, init_dict=None):
        super(LogisticRequester, self).__init__(init_dict=init_dict)
        self.mail_subscriber = mailing_list.MailListSubscriber(self)

        self._requested_items = {}
        self._in_transit_items = {}  # stuff that is on the way to this requester
        self._list_of_suppliers = {}
        # _list_of_suppliers:
        # {item_id: OrderedDict([(supplier, distance), ...])}
        self._position = movement_plugin.PluginPosition()

        self.distribution_centre = None
        self._distribution_centre_distance = float('inf')
        self._find_closest_distribution_centre()

    @property
    def position(self):
        return self._position.coord

    @position.setter
    def position(self, value):  # when this requester moves, update ranking of suppliers
        self._position.coord = value

        self._find_closest_distribution_centre()

        for k, v in self._list_of_suppliers.items():
            for supplier in v:
                self._update_supplier(k, supplier)

            self._sort_list_of_suppliers(k)

    def _update_supplier(self, item_id, supplier):
        sup_pos = supplier.position
        self_pos = self._position
        distance = self_pos.get_distance_from_squared(sup_pos)
        if distance < self._distribution_centre_distance:
            self._list_of_suppliers[item_id][supplier] = distance

    def _sort_list_of_suppliers(self, item_id):
        self._list_of_suppliers[item_id] = OrderedDict(sorted(self._list_of_suppliers[item_id].items(),
                                                              key=lambda t: t[1]))

    def _find_closest_distribution_centre(self):
        self.distribution_centre, self._distribution_centre_distance = find_closest_distribution_centre(self._position)

    def _refresh_all_suppliers(self):
        for item_id, suppliers in share.logistics.suppliers:
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
        if item_id not in share.logistics.item_ids:
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
        share.logistics.distribution_centres.add(self)
        super(LogisticDistributionCentre, self).__init__(init_dict=init_dict)
        self.mail_subscriber = mailing_list.MailListSubscriber(self)

    def receive_mail(self, mail):
        pass


class LogisticSupplier(inventory_plugin.PluginInventory):
    def __init__(self, init_dict=None):
        super(LogisticSupplier, self).__init__(init_dict=init_dict)
        self.mail_subscriber = mailing_list.MailListSubscriber(self)

        self._position = movement_plugin.PluginPosition()

    @property
    def position(self):
        return self._position.coord

    @position.setter
    def position(self, value):
        self._position.coord = value

    def receive_mail(self, mail):
        pass

    def receive_item(self, item):
        super(LogisticSupplier, self).receive_item(item)
        share.logistics.suppliers[item.id].add(self)

    def _find_closest_distribution_centre(self):
        self.distribution_centre, self._distribution_centre_distance = find_closest_distribution_centre(self._position)


class LogisticCarrierCoordinator(object):
    def __init__(self):
        self._to_deliver = {}  # dict of int: delivery pairs. int is delivery ID

    def new_delivery(self, origin, destination, item_id, count):
        delivery_dict = {
            'origin': origin,
            'destination': destination,
            'item_id': item_id,
            'count': count
        }

        i = 0
        while True:
            if i not in self._to_deliver.keys():
                break
            else:
                i += 1

        self._to_deliver[i] = delivery_dict

        return i

    def cancel_delivery(self, i):
        if i in self._to_deliver.keys():
            self._to_deliver[i]['origin'].cancel_delivery(i)
            self._to_deliver[i]['destination'].cancel_delivery(i)
            # TODO recall carrier
            del self._to_deliver[i]

    def update_deliveries(self):
        for i, delivery in self._to_deliver.items():
            delivery['origin'].give_item()




class _LogisticShare(object):
    def __init__(self):
        self.suppliers = {}
        self.distribution_centres = set()
        self.carrier_coordinator = LogisticCarrierCoordinator()


def find_closest_distribution_centre(position):
        min_dist = float('inf')
        result = None
        for dc in share.logistics.distribution_centres:
            dist = position.get_distance_from_squared(dc.position)
            if dist < min_dist:
                result = dc
                min_dist = dist
        return result, min_dist


def create_supplier_update(supplier, item_id):
    data = {
        'list': item_id,
        'supplier': supplier,
        'request': 'update_supplier'
    }
    event = share.Event(data=data, event_type='mail')
    return event


if __name__ == "__main__":
    share.logistics = _LogisticShare()