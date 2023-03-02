from django.urls import path
from .views import BattleView

urlpatterns = [
    path('battle/',BattleView.as_view(),name="battle"),
    ]