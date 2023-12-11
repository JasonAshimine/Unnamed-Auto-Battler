from django.test import TestCase
from django.urls import reverse

from .settings import *
from api.models import Item

# Create your tests here.

class TestDraft(TestCase):
    def setUp(self):
        self.expected_data = []
        for i in range(1,5):
            self.expected_data.append(Item.objects.create(name=f"first {i}", tier=i, value=i).serialize())
            self.expected_data.append(Item.objects.create(name=f"second {i}", tier=i, value=i).serialize())


    def test_draft_list_no_param(self):
        response = self.client.get(reverse('draft'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

        self.assertJSONEqual(str(response.content, encoding='utf8'), self.expected_data[:2])

    def test_draft_list_tier_5(self):
        tier = 5
        response = self.client.get(reverse('draft') + f'?tier={tier}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

        data = response.json()

        self.assertEqual(len(data), DRAFT_MAX_SHOW)
        self.assertEqual(len(list(filter(lambda o: o['tier'] <= tier, data))), DRAFT_MAX_SHOW)


