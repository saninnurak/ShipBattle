from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StatusSerializer



class StatusView(APIView):
    def get(self, request):
        serializer = StatusSerializer({'status':'ok'})
        return Response(serializer.data)

class BattleView(APIView):
    def get(self, request):
        if (ships := request.GET.get("ships", None)) is None:
            return Response({"error": "No ships provided"})

        ship_nums = ships.split(",")
        winner = self.run_battle(ship_nums)
        return Response({"winner": winner})

    def run_battle(self, ship_nums):
        raise NotImplementedError("You must implement this method")
