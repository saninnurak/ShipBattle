from django.db import models

__all__ = (
    "Ship",
    "Battle",
    "BattleResult",
)


class Battle(models.Model):
    attacker = models.ForeignKey("Ship", on_delete=models.CASCADE, related_name="attacker")
    defender = models.ForeignKey("Ship", on_delete=models.CASCADE, related_name="defender")

    class Meta:
        unique_together = (("attacker", "defender"),)

    def __str__(self):
        return f"{self.attacker} vs {self.defender}"


class BattleResult(models.Model):
    battle = models.ForeignKey("Battle", on_delete=models.CASCADE)
    winner = models.ForeignKey("Ship", on_delete=models.CASCADE, related_name="winner")
    loser = models.ForeignKey("Ship", on_delete=models.CASCADE, related_name="loser")

    class Meta:
        unique_together = (("battle",),)

    def __str__(self):
        return f"{self.winner} won against {self.loser}"


class Ship(models.Model):
    name = models.CharField(max_length=100)
    num_soldiers = models.IntegerField()
    eligible_soldiers = models.IntegerField()
    seasickness_soldiers = models.IntegerField(default=0)
    death_soldiers = models.IntegerField(default=0)
    destroyed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("name", "destroyed"),)

    def __str__(self):
        return self.name

    @classmethod
    def get_random_ship(cls):
        return cls.objects.filter(destroyed=False).order_by("?").first()