from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth
from pprint import pprint
import requests

Api_key = 'aaa245439f6e4d2093fa3e4235bb8459'

def display_news(request):
    url = 'https://api.worldnewsapi.com/search-news'
    parameters = {
    'text': 'Bamboo Research', # query phrase
    'sort': 'publish-time',  # maximum is 100
    'api-key': Api_key,  # your own API key
    'source-countries' : 'in'
}
    response = requests.get(url, params=parameters)
    news_list = response.json()
    try:
        context = {
            'news_list' : list(news_list['news'][:2]),
        }
        return render(request, r'News\news.html', context)
    except:
        context = {
            'message' : 'Sorry No News Available This Time'
        }
        return render(request, r'News\news.html', context)
