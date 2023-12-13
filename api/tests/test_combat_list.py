import json
from django.test import TestCase
from api.models import CombatList

from api.settings import *
from api.tests.test_creature import count_items
from api.tests.test_item import genBaseItem


# DONE - basic test
class TestCombatList(TestCase):
    def setUp(self):
        genBaseItem()

    def test_fn_get_opponent(self):
        creature = CombatList.get_opponent(10)
        combat = CombatList.objects.first()

        self.assertEqual(len(CombatList.objects.all()),1)
        self.assertEqual(combat.id, 10)

        self.assertEqual(count_items(creature), 10)

    def test_serialize(self):
        creature = CombatList.get_opponent(10)
        combat = CombatList.objects.first()

        self.assertJSONEqual(json.dumps(combat.serialize()), creature.serialize())
