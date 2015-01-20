from plugin_plugin import Plugin


class PluginItem(Plugin):
    def __init__(self, init_dict=None):
        self.id = "default"
        self.stack_size = 1
        self.stack_max = 50
        self.name = "Default"
        self.health = 100
        super(PluginItem, self).__init__(init_dict=init_dict)

    def is_equivalent_item(self, other):
        if not hasattr(other, 'inherited_types'):
            return False
        if 'PluginItem' not in other.inherited_types:
            return False
        if self.id != other.id:
            return False
        if self.health != other.health:
            return False

        return True

    def receive_from(self, item):
        """
        Receives an item to stack into this item
        :param item:
        :return:
        item passed in has it's stack size changed accordingly
        True: Success (item accepted)
        False: No Space (item rejected)
        int: Number of items that did not fit (item partially accepted)
        """
        if not self.is_equivalent_item(item):
            return False

        total = self.stack_size + item.stack_size
        if total > self.stack_max:
            self.stack_size = self.stack_max
            remain = total - self.stack_max
            item.stack_size = remain
            return remain
        else:
            self.stack_size = total
            item.stack_size = 0
            return True

    def give_to(self, item, quantity, accept_partial=True):
        """
        Try to take from this item stack
        :param item:
        :param accept_partial: Whether partial success is allowed
        :return:
        item passed in has it's stack size changed accordingly
        True: Request successful
        False: Request unsuccessful
        int: Number of items that were given (partial success)
        """
        if not self.is_equivalent_item(item):
            return False

        if self.stack_size == 0:
            return False

        if self.stack_size > quantity:
            if item.stack_max - item.stack_size <= quantity:
                self.stack_size -= quantity
                item.stack_size += quantity
                return True
            elif accept_partial:
                given = item.stack_max - item.stack_size
                item.stack_size = item.stack_max
                self.stack_size -= given
                return given
            else:
                return False
        elif accept_partial:
            partial = self.stack_size
            if item.stack_max - item.stack_size <= partial:
                self.stack_size = 0
                item.stack_size += partial
                return partial
            else:
                remain = partial - (item.stack_max - item.stack_size)
                item.stack_size = item.stack_max
                self.stack_size = remain
                return partial - remain
        else:
            return False


class PluginInventory(Plugin):
    def __init__(self, init_dict=None):
        self.inventory = []
        self._slot_count = 0
        super(PluginInventory, self).__init__(init_dict=init_dict)

    @property
    def slot_count(self):
        return self._slot_count

    @slot_count.setter
    def slot_count(self, value):
        # If inventory gets reduced in size, delete the slots:
        if value < self.slot_count:
            self.inventory = self.inventory[:value]
        # If inventory grows, initialise new slots
        else:
            for i in range(self.slot_count, value):
                self.inventory.append(None)

        self._slot_count = value

    def receive_item(self, item):
        """
        Attempts to stack a passed in item with another item in this inventory.
        Failing that, places in vacant slot.
        :param item:
        Item to be placed in inventory
        :return:
        item passed in will have it's stack size adjusted accordingly
        True: item stacked successfully
        False: item not accepted
        int: number of items that did not fit (partial success)
        """
        vacant_flag = -1
        result = False  # result is False if item did not stack at all
        for i, it in enumerate(self.inventory):
            if it is None:
                if vacant_flag == -1:  # remember where a vacant slot was incase stacking fails
                    vacant_flag = i
                continue

            result = it.receive_from(item)
            if result is True:  # stack successful
                return True
            elif type(result) == int:
                item.stack_size = result

        if vacant_flag > -1:
            self.inventory[vacant_flag] = item
            return True
        return result

    def give_item(self, item, quantity, accept_partial=True):
        """
        Try to get items from this inventory
        Pass an item in and request how large a stack you want in it.
        :param item:
        :param quantity:
        :param accept_partial:
        :return:
        item passed in will have it's stack size increase accordingly
        True: request successful
        False: request unsuccessful
        int: number of items that were available, and given (partial success)
        """
        quantity_remaining = quantity
        for it in self.inventory:
            if it.is_equivalent_item(item):
                result = it.give_to(item, quantity_remaining, accept_partial)
                if result is True:
                    return True
                if type(result) == int:
                    quantity_remaining -= result  # result is number that were given

        if quantity_remaining == quantity:
            return False
        else:
            return quantity - quantity_remaining

    def merge_into(self, inventory):
        """
        Push all of this inventory into other inventory
        :param inventory:
        :return:
        True: Success, this inventory is now empty
        False: Failure (potentially partial failure)
        """
        if not type(inventory) == PluginInventory:
            return False

        success_flag = True
        for it in self.inventory:
            result = inventory.receive_item(it)
            if result is not True:  # if either False or int are returned, this merge was unsuccessful
                success_flag = False

        return success_flag

    def get_item_count(self, item_id):
        """
        Finds whether this inventory holds a given item, and if so returns the amount contained.
        :param item_id:
        :return:
        int: number of specified item in this inventory
        """
        count = 0
        for item in self.inventory:
            if item.id == item_id:
                count += item.stack_size
        return count