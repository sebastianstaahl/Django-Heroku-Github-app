from django.urls import path, re_path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("loggedin/", views.loggedin, name="Logged in"),
path("session", views.session, name="Session"),
path("startpage/", views.startpage, name="Start page"),
re_path(r'callback?(?P<name>.*)$', views.callback, name="Callback"),
]
