from django.urls import path

from . import views

urlpatterns = [
path("login2/", views.login, name="login"),
path("", views.home, name="home"),
]
