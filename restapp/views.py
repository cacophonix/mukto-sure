from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from restapp.serializers import UserSerializer, GroupSerializer
import json
import requests
import duckduckgo
from restapp.models import Question
import unirest
from collections import OrderedDict
from bs4 import BeautifulSoup as bs
import requests
import opener


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def greetings(request):
    answer = 'this is purely random text'
    try:
        # response = requests.get('http://quotesondesign.com/api/3.0/api-3.0.json')
        # json_data = json.loads(response.text)
        # answer = json_data['quote']
        url='http://ivyjoy.com/quote.shtml'

        data=opener.fetch(url)['data']

        soup=bs(data)

        l=soup.text[1878:].split()

        l=l[:len(l)-1]

        t=" ".join(l)
        answer=t

    except:
        response = requests.get('http://quotesondesign.com/api/3.0/api-3.0.json')
        json_data = json.loads(response.text)
        answer = json_data['quote']
        
    answer = answer.replace('\r', ' ')
    answer = answer.replace('\n', ' ')
    answer = " ".join(answer.split())
    answer = 'Hello, Kitty! ' + answer
    return JsonResponse({"answer": answer})


def weather(request):
    question = request.GET.get('q', "temperature in Dhaka")

    lw = question.split()
    city = lw[len(lw) - 1]
    json_data = {}
    try:

        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city

        response = requests.get(url)

        json_data = json.loads(response.text)

    except:
        JsonResponse({"answer": "openweathermap is down"})

    if "temperature" in question:
        return JsonResponse({"answer": str(json_data["main"]["temp"]) + " K"})

    elif "humidity" in question:
        return JsonResponse({"answer": str(json_data["main"]["humidity"])+"%"})

    else:
        cur = lw[2]
        cur = cur.lower()
        flag = False
        if len(json_data['weather']) == 0 and cur == 'clear':
            return JsonResponse({"answer": "Yes"})

        for w in json_data['weather']:
            if cur in w['description'].lower():
                flag = True

        if flag:
            return JsonResponse({"answer": "Yes"})
        else:
            return JsonResponse({"answer": "No"})

def qa(request):
    # print("hic")
    question = request.GET.get('q', "muktosoft")

    if question=="Tell me! What don't you know?":
        questions=Question.objects.all()
        ans={}
        cnt=1
        print(len(questions))
        for q in questions:
            ans["#"+str(cnt)]=q.question
            cnt=cnt+1
        ans=OrderedDict(sorted(ans.items(), key=lambda t: int(t[0][1:])))
        return JsonResponse({"answer": ans})

    answer="Your majesty! Jon Snow knows nothing! So do I!"

    try:
        answer=duckduckgo.get_zci(question)
    except:
        q=Question(question=question)
        q.save()

    if answer[0:4]=="http":
        q=Question(question=question)
        q.save()
        answer="Your majesty! Jon Snow knows nothing! So do I!"

    return JsonResponse({"answer": answer})

