from django.contrib import admin

from .models import Battle, BattleResult, Ship


@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    list_display = ("name", "num_soldiers", "eligible_soldiers", "seasickness_soldiers", "death_soldiers", "destroyed")


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ("attacker", "defender")


@admin.register(BattleResult)
class BattleResultAdmin(admin.ModelAdmin):
    list_display = ("battle", "winner", "loser")