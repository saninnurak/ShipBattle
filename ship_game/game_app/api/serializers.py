from game_app.models import Ship
from rest_framework import serializers

__all__ = (
    "StatusSerializer",
    "BattleSerializer",
    "ErrorSerializer",
    "ShipQuerySerializer",
)


class StatusSerializer(serializers.Serializer):
    status = serializers.CharField()


class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ("name", "num_soldiers", "eligible_soldiers", "seasickness_soldiers", "death_soldiers", "destroyed")
        read_only_fields = (
            "name",
            "num_soldiers",
            "eligible_soldiers",
            "seasickness_soldiers",
            "death_soldiers",
            "destroyed",
        )


class BattleSerializer(serializers.Serializer):
    winner = ShipSerializer()
    loser = ShipSerializer()



class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class ShipQuerySerializer(serializers.Serializer):
    ships = serializers.CharField(
        required=True,
        help_text="A comma-separated list of ship IDs",
        max_length=100,
    )

    def validate_ships(self, value):
        ships = value.split(",")
        try:
            ships = [int(s) for s in ships]
        except ValueError:
            raise serializers.ValidationError("Invalid ship IDs in the query parameter 'ships'.")
        if any(i <= 0 for i in ships):
            raise serializers.ValidationError("Invalid ship IDs in the query parameter 'ships'.")
        if not (10 > len(ships) > 2):
            raise serializers.ValidationError("ships length must be between 2 and 10")
        return ships