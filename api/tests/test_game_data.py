import json
from django.test import TestCase
from api.models import GameData, Player,Item

from api.settings import *
from api.tests.test_item import genBaseItem


# TODO - game data
def set_junk_data(obj, value = 99):
    for key in START_GAME_DATA:
        setattr(obj, key, value)    
    obj.save()


class TestGameData(TestCase):
    def setUp(self):
        player = Player.objects.create()
        GameData.objects.create(**START_GAME_DATA, player=player)
        genBaseItem()

    def test_fn_buy_item(self):
        data = GameData.objects.first()
        data.gold = ITEM_COST

        data.new_store_list()
        expect_item = Item.objects.get(pk= data.store_list[2]['id'])
        item = data.buyItem(2)

        self.assertEqual(data.gold, 0)
        self.assertJSONEqual(json.dumps(item), expect_item.serialize())
        self.assertEqual(len(data.store_list), DRAFT_MAX_SHOW - 1)

        with self.assertRaises(ValueError,msg="Should not have enough gold to buy tier"):
            data.buyItem(1)

    def test_fn_buy_tier(self):
        data = GameData.objects.first()
        expect_gold = 100

        with self.assertRaises(ValueError,msg="Should not have enough gold to buy tier"):
            data.buyTier()

        data.gold = expect_gold

        for tier in range(2, MAX_TIER + 1):
            expect_gold -= data.tier_cost
            data.buyTier()
            self.assertEqual(data.tier, tier, f"Tier not match: tier{tier}")            
            self.assertEqual(data.gold, expect_gold, f"Gold not match: tier {tier}")

        with self.assertRaises(OverflowError, msg=f"Should be maxed tier - data.tier:{data.tier} max:{MAX_TIER}"):
            data.buyTier()
        
    
    def test_fn_reroll(self):
        data = GameData.objects.first()
        data.reroll()

        self.assertEqual(data.gold, START_GAME_DATA.get("gold") - REROLL_COST)
        self.assertEqual(len(data.store_list), DRAFT_MAX_SHOW)

        data.gold = 0
        with self.assertRaises(ValueError,msg="Should not have enough gold"):
            data.reroll()

    def test_fn_spend(self):
        data = GameData.objects.first()

        data.spend(data.gold)
        self.assertAlmostEqual(data.gold, 0)

        with self.assertRaises(ValueError,msg="Should not have enough gold"):
            data.spend(10)
    
    def test_fn_update_store_list(self):
        data = GameData.objects.first()
        data.new_store_list()
        self.assertEqual(len(data.store_list), DRAFT_MAX_SHOW)

    def test_fn_remove_item(self):
        data = GameData.objects.first()
        data.new_store_list()
        expect_item = Item.objects.get(pk= data.store_list[2]['id'])
        item = data.remove_item(2)

        self.assertJSONEqual(json.dumps(item), expect_item.serialize())
        self.assertEqual(len(data.store_list), DRAFT_MAX_SHOW - 1)


    def test_fn_reset(self):
        data = GameData.objects.first()
        set_junk_data(data, 99)

        data.reset()
        data = GameData.objects.first()

        for key in START_GAME_DATA:
            self.assertEqual(getattr(data, key), START_GAME_DATA[key], f"On {key}")
        
        self.assertEqual(len(data.store_list), 0)

    def test_serialize(self):
        data = GameData.objects.first()
        item = Item.objects.first()
        data.store_list.append(item.serialize())

        self.assertJSONEqual(json.dumps(data.serialize()), {
            **START_GAME_DATA,
            "store_list": [item.serialize()]
        })