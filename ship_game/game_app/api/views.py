import logging
import random
import uuid


from drf_yasg.utils import swagger_auto_schema
from game_app.api.serializers import BattleSerializer, ErrorSerializer, ShipQuerySerializer, StatusSerializer
from game_app.models import Battle, BattleResult, Ship

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class StatusView(APIView):
    @swagger_auto_schema(responses={200: StatusSerializer})
    def get(self, request):
        serializer = StatusSerializer({"status": "ok"})
        return Response(serializer.data)


class ShipBattleView(APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: BattleSerializer, status.HTTP_400_BAD_REQUEST: ErrorSerializer},query_serializer=ShipQuerySerializer,)
    
    def get(self, request):
    
        serializer = ShipQuerySerializer(data=request.query_params)
        if serializer.is_valid():
            ships = serializer.validated_data["ships"]
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f"ships: {ships}")

        ship_ids = []
        for soldier_count in ships:
            num_soldiers = soldier_count
            seasickness_soldiers = random.randint(0, num_soldiers)
            eligible_soldiers = num_soldiers - seasickness_soldiers

            ship = Ship.objects.create(
                name=f"Ship {str(uuid.uuid4())[:6]}",
                num_soldiers=num_soldiers,
                seasickness_soldiers=seasickness_soldiers,
                eligible_soldiers=eligible_soldiers,
            )
            ship_ids.append(ship.id)

        response = []
        while Ship.objects.filter(id__in=ship_ids, destroyed=False).count() > 1:
            attacker_id = random.choice(ship_ids)
            defender_id = random.choice(ship_ids)
            while attacker_id == defender_id:
                defender_id = random.choice(ship_ids)

            attacker = Ship.objects.get(id=attacker_id)
            defender = Ship.objects.get(id=defender_id)
            while attacker.eligible_soldiers > 0 and defender.eligible_soldiers > 0:
                attacker.death_soldiers = random.randint(0, attacker.eligible_soldiers)
                attacker.eligible_soldiers = attacker.eligible_soldiers - attacker.death_soldiers
                attacker.save(update_fields=["eligible_soldiers", "death_soldiers"])
                attacker.refresh_from_db()

                defender.death_soldiers = random.randint(0, defender.eligible_soldiers)
                defender.eligible_soldiers = defender.eligible_soldiers - defender.death_soldiers
                defender.save(update_fields=["eligible_soldiers", "death_soldiers"])
                defender.refresh_from_db()

            if defender.eligible_soldiers == 0:
                winner = attacker
                loser = defender
                defender.destroyed = True
                defender.save(update_fields=["destroyed"])
                ship_ids.remove(defender_id)
            else:
                winner = defender
                loser = attacker
                attacker.destroyed = True
                attacker.save(update_fields=["destroyed"])
                ship_ids.remove(attacker_id)

            battle = Battle.objects.create(attacker=attacker, defender=defender)
            BattleResult(battle=battle, winner=winner, loser=loser).save()

            attacker.refresh_from_db()
            defender.refresh_from_db()

            response.append(
                {
                    "attacker": {
                        "name": attacker.name,
                        "num_soldiers": attacker.num_soldiers,
                        "eligible_soldiers": attacker.eligible_soldiers,
                        "seasickness_soldiers": attacker.seasickness_soldiers,
                        "death_soldiers": attacker.death_soldiers,
                        "destroyed": attacker.destroyed,
                    },
                    "defender": {
                        "name": defender.name,
                        "num_soldiers": defender.num_soldiers,
                        "eligible_soldiers": defender.eligible_soldiers,
                        "seasickness_soldiers": defender.seasickness_soldiers,
                        "death_soldiers": defender.death_soldiers,
                        "destroyed": defender.destroyed,
                    },
                    "winner": winner.name,
                    "loser": loser.name,
                }
            )

        Ship.objects.filter(id__in=ship_ids, destroyed=False).update(destroyed=True)  # because the war is over.
        return Response(BattleSerializer(response, many=True).data)