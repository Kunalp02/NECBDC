from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from .settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
import razorpay
import hmac


def index(request):
    return render(request, 'index.html')

