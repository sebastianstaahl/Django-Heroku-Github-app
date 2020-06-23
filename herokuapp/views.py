from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
import requests
from django.template import RequestContext, Template
import json
from .forms import MyForm
from .models import SelectedRepository, AccessToken, UserName, PayLoad
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

    token_db = AccessToken()
    token_db.token = access_token
    token_db.save()

    access_token = 'token ' + access_token
    print(access_token)

    headers = {
    'Authorization': access_token,
    }

    response3 = requests.get('https://api.github.com/user', headers=headers)
    print("RESPONSE 3: ", response3.json())

    username = response3.json()['login']
    user = UserName()
    user.username = username
    user.save()

    response4 = requests.get('https://api.github.com/user/repos', headers=headers)
    print("RESPONSE 4: ", response4.json())
    data = response4.json()
    # print("TYPE OF DATA: ", type(data))
    repos = list()
    # users = list()
    context = {}
    my_form = MyForm()

    for repo in data:
        key = repo['name']
        # user = repo['owner']['login']
        #repos[key] = repo
        repos.append(key)
        # users.append(user)

    context['names'] = repos
    context['form'] = my_form
    context['data'] = data

    return render(response, "herokuapp/callback.html", context)

def linkedrepo(request):

    if request.method=="POST":
        print("POST")
        if request.POST.get('name'):
            repo = SelectedRepository()
            repo.name = request.POST.get('name')
            print("REPO: ", repo)
            print("TYPE: ", type(repo))
            print("ID: ", type(repo.id))
            repo.save()
            messages.success(request, 'Selected repo saved successfully!')
    
    context ={}
    context['name'] = repo.name

    username = UserName.objects.all()[0].username
    print("user: ", username)

    token = AccessToken.objects.all()[0].token
    print("TOKEN: ", token)
    print("TYPE TOKEN: ", type(token))

    access_token = 'token ' + token
    print(access_token)

    headers = {
    'Authorization': access_token,
    }

    # Hittade inge merge webhook event.
    hook = {'config':{'url':'http://willandskill.herokuapp.com/webbhooks'}, 'events':['push','pull_request']}
    url = 'https://api.github.com/repos/' + username + '/' + repo.name + '/hooks'
    response = requests.post(url, json=hook, headers=headers)
    print("HOOK RESPONSE: ", response)
    print("HOOK RESPONSE TYPE: ", type(response))
    print("HOOK RESPONSE TEXT: ", response.content)

    AccessToken.objects.all().delete()
    SelectedRepository.objects.all().delete()

    return render(request, "herokuapp/linkedrepo.html", context)

def webbhooks(response):
    print("WEBB HOOK RESPONSE: ", response)

    payload = PayLoad()
    payload.payload = response
    payload.save()

    context = {}
    context['payload'] = payload.payload
    return render(response, "herokuapp/webbhooks.html", context)


