from django.urls import path, re_path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("loggedin/", views.loggedin, name="Logged in"),
path("session", views.session, name="Session"),
path("startpage/", views.startpage, name="Start page"),
path("linkedrepo/", views.linkedrepo, name="Linked Repo"),
path("webbhooks/", views.webbhooks, name="Web Hooks"),
path("listofhooks/", views.listofhooks, name="List of hooks"),
re_path(r'callback?(?P<name>.*)$', views.callback, name="Callback"),
]
