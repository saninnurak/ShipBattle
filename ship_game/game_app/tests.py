from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class StatusTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_status(self):
        response = self.client.get('/api/status/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,{'status':'ok'})

class ShipBattleViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_ship_battle_view_3_ships(self):
        response = self.client.get("/api/battle/?ships=5,10,4")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        first_result = response.json()[0]
        second_result = response.json()[1]


        self.assertEqual(
            first_result["winner"]["num_soldiers"],
            first_result["winner"]["eligible_soldiers"]
            + first_result["winner"]["seasickness_soldiers"]
            + first_result["winner"]["death_soldiers"],
        )
        self.assertEqual(
            first_result["loser"]["num_soldiers"],
            first_result["loser"]["eligible_soldiers"]
            + first_result["loser"]["seasickness_soldiers"]
            + first_result["loser"]["death_soldiers"],
        )

        self.assertEqual(
            second_result["winner"]["num_soldiers"],
            second_result["winner"]["eligible_soldiers"]
            + second_result["winner"]["seasickness_soldiers"]
            + second_result["winner"]["death_soldiers"],
        )
        self.assertEqual(
            second_result["loser"]["num_soldiers"],
            second_result["loser"]["eligible_soldiers"]
            + second_result["loser"]["seasickness_soldiers"]
            + second_result["loser"]["death_soldiers"],
        )

    def test_ship_battle_view_4_ships(self):
        response = self.client.get("/api/battle/?ships=5,10,4,6")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_ship_battle_view_5_ships(self):
        response = self.client.get("/api/battle/?ships=5,10,4,6,12")

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(len(response.data), 4)