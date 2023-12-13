import json
from django.test import TestCase
from api.models import Creature, CreatureItemCount, Item
from django.db.models import Sum

from api.settings import *

from .test_item import genBaseItem

# DONE basic test

def count_items(creature):
    return creature.counts.aggregate(total_count=Sum('count'))['total_count']

def set_junk_data(creature, data = 99):
    for key in START_CREATURE:
        setattr(creature, key, data)    
    creature.save()

def check_item_calc(self, creature, fn = lambda val, index:val):
    data = dict(START_CREATURE)

    for index, item in enumerate(self.expected_item):
        key = item.type.type
        data[key] += fn(item.value, index)

    for key, value in data.items():
        self.assertEqual(data[key], value)

# ----------------------------------------------------------------------
# class test

class TestCreature(TestCase):
    def setUp(self):
        self.expected_item = genBaseItem()        
        self.creature = Creature.objects.create(name="test",**START_CREATURE)

    def test_fn_reset(self):
        item = Item.objects.get(pk=1)
        creature = Creature.objects.get(pk=1)

        creature.items.add(item)
        set_junk_data(creature)
        creature.reset()
        
        creature = Creature.objects.get(pk=1)

        for key, value in START_CREATURE.items():
            self.assertEqual(getattr(creature, key), value)

        self.assertEqual(len(creature.items.all()), 0)

    def test_fn_calc_item(self):
        creature = Creature.objects.get(pk=1)

        for index, item in enumerate(self.expected_item):
            creature.calc_item(item, index + 1)

        check_item_calc(self, creature, lambda val, index: (index + 1) * val)

    def test_fn_recalc(self):
        creature = Creature.objects.get(pk=1)
        set_junk_data(creature)        
        
        for item in self.expected_item:
            creature.items.add(item)

        creature.recalc()

        check_item_calc(self, creature)

    def test_fn_add(self):
        creature = Creature.objects.get(pk=1)      
        
        for item in self.expected_item:
            creature.add(item)

        check_item_calc(self, creature)

    def test_fn_addRandomItem(self):
        creature = Creature.objects.get(pk=1)
        creature.addRandomItem(2, 5)

        self.assertEqual(count_items(creature), 5)

    def test_serialize(self):
        creature = Creature.objects.get(pk=1)
        set_junk_data(creature, 99)
        item = self.expected_item[1]

        count = CreatureItemCount.objects.create(creature=creature, item=item, count=2)

        self.assertJSONEqual(json.dumps(count.serialize()), {
            **item.serialize(),
            "count": 2
        })

        self.assertJSONEqual(json.dumps(creature.serialize()),{
            "name": "test",
            "level": 99,
            "health": 99,
            "defense": 99,
            "attack": 99,
            "items":[count.serialize()]
        })
