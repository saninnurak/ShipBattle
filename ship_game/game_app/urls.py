from django.urls import include, path

urlpatterns = [
    path("api/", include("game_app.api.urls")),
]