from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
from .matchUtilities import *


# Create your views here.


class index(View):
    def get(self, request):
        return HttpResponse("<h1>Test</h1>")
