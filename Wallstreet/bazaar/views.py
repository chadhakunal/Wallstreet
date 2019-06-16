from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import *
from .matchUtilities import *


# Create your views here.


# Create your views here.

class Register(View):
    template = 'bazaar/register.html'

    def get(self, request):
        return render(request, self.template, {})

    def post(self, request):
        try:
            g = Global.objects.get(pk=1)
            if request.POST["password"] == g.registrationKey:
                user = User.objects.create_user(username=request.POST["username"])
                password = User.objects.make_random_password(length=6)
                user.set_password(password)
                user.save()

                profile = Profile.objects.create(user=user)
                profile.save()
                return render(request, self.template, {"pass": password})
            return render(request, self.template, {"error": "Invalid Registration"})
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
            return render(request, self.template, {"error": "Invalid Username or Password"})


def Logoff(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("../login")


class postlogin(View):
    template = 'bazaar/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')
        all_companies = Company.objects.all()
        profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
        shares = UserShareTable.objects.filter(profile=profile)
        context = {"companies": all_companies, "profile": profile, "userShareTable": shares}
        return render(request, self.template, context)


class CompanyView(View):
    template = 'bazaar/company.html'

    def get(self, request):
        return render(request, self.template, {})


class Buy(View):
    template = 'bazaar/buy.html'
    context = {}

    # ToDo: Add validations in frontend
    def get(self, request):
        companies = Company.objects.all()
        context = {'companies': companies}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        company = Company.objects.get(name=request.POST["companyName"])
        bidShares = int(request.POST["quantity"])
        bidPrice = int(request.POST["price"])
        profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
        match(company, profile, bidPrice, bidShares, True)

        companies = Company.objects.all()
        context = {'companies': companies, "message": "We have received your bid! We will process it soon! Thank you"}
        return render(request, self.template, context)


class Sell(View):
    template = 'bazaar/sell.html'

    # ToDo: Add validations in frontend
    def get(self, request):
        companies = []
        user = User.objects.get(username=request.user)
        userShares = UserShareTable.objects.filter(profile=Profile.objects.filter(user=user).first())
        for entry in userShares:
            if entry.company not in companies:
                companies.append(entry.company)
        context = {'companies': companies}
        return render(request, self.template, context)

    def post(self, request):
        company = Company.objects.get(name=request.POST["companyName"])
        bidShares = int(request.POST["quantity"])
        bidPrice = int(request.POST["price"])
        profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()

        match(company, profile, bidPrice, bidShares, False)

        companies = []
        user = User.objects.get(username=request.user)
        userShares = UserShareTable.objects.filter(profile=Profile.objects.filter(user=user).first())
        for entry in userShares:
            if entry.company not in companies:
                companies.append(entry.company)
        context = {'companies': companies, 'message': "We have received your bid! We will process it soon! Thank you"}
        return render(request, self.template, context)


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
