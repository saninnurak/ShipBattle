import logging

from game_app.api.serializers import StatusSerializer


from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class StatusView(APIView):
    @swagger_auto_schema(responses={200: StatusSerializer})
    def get(self, request):
        serializer = StatusSerializer({"status": "ok"})
        return Response(serializer.data)


