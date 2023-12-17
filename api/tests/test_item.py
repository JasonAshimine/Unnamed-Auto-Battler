import json
from django.test import TestCase
from api.models import ItemType, Item

from api.settings import *

# DONE basic Item test

def genItem(tier, prefix, type):
    return Item.objects.create(name=f"{prefix} {tier}", tier=tier, value=tier, type_id=type.id)

def genItemType(name):
    return ItemType.objects.create(name=f"name:{name}", type=name)

def genBaseItem():
    expected_items = []

    attack = genItemType("attack")
    defense = genItemType("defense")
    hp = genItemType("max_health")

    for tier in range(1, 6):
        expected_items.append(genItem(tier, "atk", attack))
        expected_items.append(genItem(tier, "def", defense))
        expected_items.append(genItem(tier, "hp", hp))

    return expected_items

# ----------------------------------------------------------------------
# class test

class TestItem(TestCase):
    def setUp(self):
        self.data = []
        genBaseItem()

    def test_serialize(self):
        itemType = ItemType.objects.get(type="attack")
        self.assertEqual(itemType.serialize()['type'], "attack")
        
        item = Item.objects.get(pk=2)

        expected = {
            "id":2, 
            "name": "def 1",
            "tier": 1,
            "type": item.type.serialize(),
            "value": 1
        }
        
        self.assertEqual(item.id, 2)

        item_json = json.dumps(item.serialize())
        self.assertJSONEqual(item_json, expected)