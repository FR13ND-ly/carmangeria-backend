from . import views
from django.urls import path

urlpatterns = [
    path("register/", views.register),
    path("authentification/", views.authentificate),
    path("authorization/<str:token>/", views.authorization),
]