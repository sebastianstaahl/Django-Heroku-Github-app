from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
import requests
from django.template import RequestContext, Template
import json
from .forms import MyForm
from .models import SelectedRepository
from django.contrib import messages


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

    response4 = requests.get('https://api.github.com/user/repos', headers=headers)
    print("RESPONSE 4: ", response4.json())
    data = response4.json()
    print("TYPE OF DATA: ", type(data))
    repos = list()
    context = {}
    my_form = MyForm()

    for repo in data:
        key = repo['name']
        #repos[key] = repo
        repos.append(key)

    context['names'] = repos
    context['form'] = my_form

    return render(response, "herokuapp/callback.html", context)

def linkedrepo(request):

    if request.method=="POST":
        print("POST")
        if request.POST.get('name'):
            savename = SelectedRepository()
            savename.name = request.POST.get('name')
            print("SAVENAME: ", savename)
            print("TYPE: ", type(savename))
            savename.save()
            messages.success(request, 'Selected repo saved successfully!')            
    
    context ={}
    context['name'] = savename.name

    return render(request, "herokuapp/linkedrepo.html", context)
