from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StatusSerializer,ErrorSerializer,BattleSerializer



class StatusView(APIView):
    @swagger_auto_schema(responses={200: StatusSerializer})
    def get(self, request):
        serializer = StatusSerializer({"status": "ok"})
        return Response(serializer.data)


class BattleView(APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: BattleSerializer, status.HTTP_400_BAD_REQUEST: ErrorSerializer})
    def get(self, request):
        if (ships := request.GET.get("ships", None)) is None:
            return Response({"error": "No ships provided"},status=status.HTTP_400_BAD_REQUEST)

        ship_nums = ships.split(",")
        winner = self.run_battle(ship_nums)
        serializer = BattleSerializer({"winner": winner})
        return Response(serializer.data)

    def run_battle(self, ship_nums):
        raise NotImplementedError("You must implement this method")
