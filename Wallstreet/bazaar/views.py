from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import *
from .matchUtilities import *


# Create your views here.

class Register(View):
    template = 'bazaar/register.html'

    def get(self, request):
        return render(request, self.template, {})

    def post(self, request):
        try:
            user = User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            return render(request, self.template, {})
        except IntegrityError:
            return render(request, self.template, {"error": "Invalid Registration"})


class Login(View):
    template = 'bazaar/login.html'
    template1 = 'bazaar/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('../')
        return render(request, self.template, {})

    def post(self, request):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("../")
        else:
            return render(request, self.template, {})


def Logoff(request):
    template = 'bazaar/login.html'
    if request.user.is_authenticated:
        logout(request)
    return redirect("/login")


class postlogin(View):
    template = 'bazaar/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')
        all_companies = Company.objects.all()
        profile = Profile.objects.filter(user=User.objects.get(username=request.user))
        context = {"all_companies": all_companies, "profile": profile}
        return render(request, self.template, context)


class CompanyView(View):
    template = 'bazaar/company.html'

    def get(self, request):
        return render(request, self.template, {})


class Buy(View):
    template = 'bazaar/buy.html'

    def get(self, request):
        return render(request, self.template, {})


class Sell(View):
    template = 'bazaar/sell.html'

    def get(self, request):
        return render(request, self.template, {})


class News(View):
    template = 'bazaar/news.html'

    def get(self, request):
        return render(request, self.template, {})


class Transactions(View):
    template = 'bazaar/transactions.html'

    def get(self, request):
        return render(request, self.template, {})


class LeaderBoardView(View):
    template = 'bazaar/leaderboard.html'

    def get(self, request):
        return render(request, self.template, {})
