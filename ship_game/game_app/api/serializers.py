from rest_framework import serializers

__all__ = (
    "StatusSerializer",
    "BattleSerializer",
)

class StatusSerializer(serializers.Serializer):
    status = serializers.CharField()

class BattleSerializer(serializers.Serializer):
    winner = serializers.CharField()

class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()