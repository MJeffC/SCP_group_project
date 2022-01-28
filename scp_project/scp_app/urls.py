from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("logout", views.logout),
]