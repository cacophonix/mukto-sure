from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from restapp.serializers import UserSerializer, GroupSerializer
import json
import requests


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
    try:
        response = requests.get('http://quotesondesign.com/api/3.0/api-3.0.json')
        json_data = json.loads(response.text)
        answer = json_data['quote']
    except:
        answer = 'this is purely random text'
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
