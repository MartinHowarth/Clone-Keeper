from inventory_plugin import PluginInventory, PluginItem
from position_plugin import PluginPosition
from movement_plugin import PluginMovement


class DefaultEntity(object):
    def __init__(self):
        self.inventory = None
        self.item = None


def create_entity_from_dict(entity_dict):
    ent = DefaultEntity()

    for plugin, plugin_dict in entity_dict.items():
        if plugin == "inventory":
            ent.inventory = {}
            for name, init_dict in plugin_dict.items():
                ent.inventory[name] = PluginInventory(init_dict=init_dict)
        elif plugin == "item":
            ent.item = PluginItem(init_dict=plugin_dict)
