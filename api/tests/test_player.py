import json
from django.test import TestCase
from api.models import Creature, GameData, ItemType, Item, Player

from api.settings import *
from api.tests.test_item import genBaseItem

# DONE/PARTIAL player test

class TestItem(TestCase):
    def setUp(self):
        player = Player.objects.create(name="test")
        data = GameData.objects.create(**START_GAME_DATA, player=player)
        Creature.objects.create(**START_CREATURE, player=player)
        genBaseItem()

    def test_fn_buyTier(self):
        pass #ignore

    def test_fn_buyItem(self):
        player = Player.objects.first()
        creature = Creature.objects.first()

        player.data.new_store_list()
        player.data.gold = ITEM_COST

        expect_item = player.data.store_list[2]
        id = expect_item.get('id')
        item = player.buyItem(id, 2)

        self.assertEqual(expect_item, item.serialize())
        self.assertEqual(creature.items.get(pk=item.id), item)

        with self.assertRaises(ValueError):
            player.buyItem(0, 0)

        player.data.gold = ITEM_COST
        with self.assertRaises(Item.DoesNotExist):
            player.buyItem(0, 0)

        
    def test_fn_reroll(self):
        pass #ignore

    def test_fn_reset(self):
        pass #ignore

    def test_fn_save_all(self):
        pass #ignore

    def test_serialize(self):
        player = Player.objects.first()
        data = GameData.objects.first()
        creature = Creature.objects.first()
        self.assertJSONEqual(json.dumps(player.serialize()), {
            "name":"test",
            "data": data.serialize(),
            "creature": creature.serialize()
        })