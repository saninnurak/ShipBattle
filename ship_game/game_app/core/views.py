import logging
import random
import uuid

from game_app.api.serializers import BattleSerializer, ErrorSerializer, ShipQuerySerializer
from game_app.models import Battle, BattleResult, Ship

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

logger = logging.getLogger(__name__)

class ShipBattleView(APIView):

    @staticmethod
    def create_and_get_ship_ids(ships: list[int]):
        ship_ids = []
        for soldier_count in ships:
            num_soldiers = soldier_count
            seasickness_soldiers = random.randint(0, num_soldiers)
            death_soldiers = 0
            eligible_soldiers = num_soldiers - seasickness_soldiers - death_soldiers

            ship = Ship.objects.create(
                name=f"Ship {str(uuid.uuid4())[:6]}",
                num_soldiers=num_soldiers,
                seasickness_soldiers=seasickness_soldiers,
                eligible_soldiers=eligible_soldiers,
                death_soldiers=death_soldiers,
                destroyed=False,
            )
            ship_ids.append(ship.id)
        return ship_ids

    @staticmethod
    def get_random_attacker_defender(ship_ids: list[int]):
        attacker_id = random.choice(ship_ids)
        defender_id = random.choice(ship_ids)
        while attacker_id == defender_id:
            defender_id = random.choice(ship_ids)

        ships = Ship.objects.filter(id__in=[attacker_id, defender_id])
        return ships.first(), ships.last()

    @swagger_auto_schema(responses={status.HTTP_200_OK: BattleSerializer, status.HTTP_400_BAD_REQUEST: ErrorSerializer},
                         query_serializer=ShipQuerySerializer, )
    def get(self, request):

        serializer = ShipQuerySerializer(data=request.query_params)
        if serializer.is_valid():
            ships = serializer.validated_data["ships"]
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f"ships: {ships}")
        ship_ids = self.create_and_get_ship_ids(ships)


        response = []
        while Ship.objects.filter(id__in=ship_ids, destroyed=False).count() > 1:
            attacker, defender = self.get_random_attacker_defender(ship_ids)

            while attacker.eligible_soldiers > 0 and defender.eligible_soldiers > 0:
                attacker.eligible_soldiers -= random.randint(0,attacker.eligible_soldiers)
                defender.eligible_soldiers -= random.randint(0, defender.eligible_soldiers)

            attacker.death_soldiers = (
                                              attacker.num_soldiers - attacker.seasickness_soldiers
                                      ) - attacker.eligible_soldiers

            defender.death_soldiers = (
                                              defender.num_soldiers - defender.seasickness_soldiers
                                      ) - defender.eligible_soldiers

            attacker.save()
            defender.save()

            attacker.refresh_from_db()
            defender.refresh_from_db()

            assert (
                    attacker.num_soldiers
                    == attacker.eligible_soldiers + attacker.seasickness_soldiers + attacker.death_soldiers
            )

            winner = attacker if defender.eligible_soldiers == 0 else defender
            loser = defender if attacker.eligible_soldiers == 0 else attacker

            loser.destroyed = True
            loser.save()
            ship_ids.remove(loser.id)

            battle = Battle.objects.create(attacker=attacker, defender=defender)
            BattleResult(battle=battle, winner=winner, loser=loser).save()

            response.append(
                {
                    "winner": {
                        "name": winner.name,
                        "num_soldiers": winner.num_soldiers,
                        "eligible_soldiers": winner.eligible_soldiers,
                        "seasickness_soldiers": winner.seasickness_soldiers,
                        "death_soldiers": winner.death_soldiers,
                        "destroyed": winner.destroyed,
                    },
                    "loser": {
                        "name": loser.name,
                        "num_soldiers": loser.num_soldiers,
                        "eligible_soldiers": loser.eligible_soldiers,
                        "seasickness_soldiers": loser.seasickness_soldiers,
                        "death_soldiers": loser.death_soldiers,
                        "destroyed": loser.destroyed,
                    },
                }
            )

        Ship.objects.filter(id__in=ship_ids, destroyed=False).update(destroyed=True)  # because the war is over.
        return Response(BattleSerializer(response, many=True).data)