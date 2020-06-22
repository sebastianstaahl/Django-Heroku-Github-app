from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
import requests
from django.template import RequestContext, Template
import json


# Create your views here.
def home(response):
    return render(response, "herokuapp/home.html", {})

def startpage(response):
    return render(response, "herokuapp/startpage.html")

def loggedin(request):
    url = 'https://github.com/login/oauth/authorize?client_id=6125bdde7cc22fdbde05&scope=user,repo'
    return redirect(url)

def session(response):
    return render(response, "herokuapp/session.html", {})

def callback(response, name):
    print("RESPONSE: ", response)
    code = str(response)[34:-2]

    url = 'https://github.com/login/oauth/access_token?client_id=6125bdde7cc22fdbde05&client_secret=97638a83270e9e66a1163ded4105d54cb826004e&code={}'.format(code)
    response2 = requests.post(url=url)
    print("RESPONSE 2: ", response2.text)
    access_token = str(response2.text)[13:-36]
    print(access_token)

    access_token = 'token ' + access_token
    print(access_token)

    headers = {
    'Authorization': access_token,
    }

    response3 = requests.get('https://api.github.com/user', headers=headers)
    print("RESPONSE 3: ", response3.json())

    return render(response, "herokuapp/callback.html", {})