from django.urls import path
from .views import BattleView,StatusView

urlpatterns = [
    path('battle/',BattleView.as_view(),name="battle"),
    path('status/',BattleView.as_view(),name="status"),
    ]