from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from datetime import datetime
from django.http import JsonResponse
import json

from .models import *
from .matchUtilities import *


# Create your views here.
buyTable = None
sellTable = None

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
            message = "Invalid Username or Password!"
            context = {"message": message}
            return render(request, self.template, context)


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
        sensex = Global.objects.filter(pk=1).first().sensex
        g = Global.objects.get(pk=1)
        context = {"companies": all_companies, "profile": profile, "userShareTable": shares, "sensex": sensex, "livetext": g.LiveText}
        return render(request, self.template, context)


class CompanyView(View):
    template = 'bazaar/company.html'

    def get(self, request):
        profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
        sensex = Global.objects.filter(pk=1).first().sensex
        companies = Company.objects.all()
        context = {"profile": profile, "sensex": sensex, "companies": companies}
        return render(request, self.template, context)


class Buy(View):
    template = 'bazaar/buy.html'
    error = 'bazaar/marketclose.html'
    context = {}

    # ToDo: Add validations in frontend
    def get(self, request):
        startStopMarket = Global.objects.get(pk=1).startStopMarket
        if startStopMarket:
            profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
            sensex = Global.objects.filter(pk=1).first().sensex
            companies = Company.objects.all()
            bidRange = Global.objects.filter(pk=1).first().bidRangePercent
            context = {'companies': companies, "profile": profile, "sensex": sensex, "bidRange": bidRange}
            return render(request, self.template, context)
        else:
            return render(request, self.error)

    def post(self, request, *args, **kwargs):
        startStopMarket = Global.objects.get(pk=1).startStopMarket

        if startStopMarket:
            companyName = request.POST["companyName"].split(' :')[0]
            company = Company.objects.get(name=companyName)
            profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
            sensex = Global.objects.filter(pk=1).first().sensex
            bidRange = Global.objects.filter(pk=1).first().bidRangePercent / 100
            bidShares = 0
            bidPrice = 0
            exec("global buyTable; buyTable = BuyTable_" + company.tempName)
            try:
                if request.POST["quantity"] and request.POST["price"]:
                    bidShares = int(request.POST["quantity"])
                    bidPrice = int(request.POST["price"])
                else:
                    companies = Company.objects.all()
                    context = {'companies': companies, "bidRange": bidRange,
                               "message": "Please Fill All The Fields",
                               "profile": profile, "sensex": sensex}
                    return render(request, self.template, context)
            except:
                companies = Company.objects.all()
                context = {'companies': companies, "bidRange": bidRange,
                           "message": "Invalid Bid",
                           "profile": profile, "sensex": sensex}
                return render(request, self.template, context)

            if 0 < bidShares <= 100 and bidPrice > 0 and (
                    1 - bidRange) * company.sharePrice <= bidPrice <= (
                    1 + bidRange) * company.sharePrice and profile.cash > 0 and profile.cash >= bidShares * bidPrice * 1.01:
                #moneyAlter(profile, bidPrice * bidShares, False)  # Subtract money for user

                moneyAlter(profile, bidPrice * bidShares, False)  # Subtract money for user
                buyTable.objects.create(company=company.pk, profile=profile, bidShares=bidShares,
                                        bidPrice=bidPrice)  # Add entry to buyTable

                match.delay(company, profile, bidPrice, bidShares, True)

                return render(request, 'bazaar/received_bid.html', {})
            else:
                companies = Company.objects.all()
                context = {'companies': companies, "bidRange": bidRange,
                           "message": "Invalid Bid",
                           "profile": profile, "sensex": sensex}
                return render(request, self.template, context)
        else:
            return render(request, self.error)


class Sell(View):
    template = 'bazaar/sell.html'
    error = 'bazaar/marketclose.html'

    # ToDo: Add validations in frontend
    def get(self, request):
        startStopMarket = Global.objects.get(pk=1).startStopMarket
        if startStopMarket:
            companies = []
            user = User.objects.get(username=request.user)
            profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
            sensex = Global.objects.filter(pk=1).first().sensex
            userShares = UserShareTable.objects.filter(profile=Profile.objects.filter(user=user).first())
            bidRange = Global.objects.filter(pk=1).first().bidRangePercent
            context = {'userShares': userShares, "profile": profile, "sensex": sensex, "bidRange": bidRange}
            return render(request, self.template, context)
        else:
            return render(request, self.error)

    def post(self, request):
        startStopMarket = Global.objects.get(pk=1).startStopMarket
        if startStopMarket:
            companyName = request.POST["companyName"].split(' :')[0]
            company = Company.objects.get(name=companyName)
            profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()

            sensex = Global.objects.filter(pk=1).first().sensex
            bidRange = Global.objects.filter(pk=1).first().bidRangePercent / 100
            bidShares = 0
            bidPrice = 0
            exec("global sellTable; sellTable = SellTable_" + company.tempName)

            try:
                if request.POST["quantity"] and request.POST["price"]:
                    bidShares = int(request.POST["quantity"])
                    bidPrice = int(request.POST["price"])
                else:
                    userShares = UserShareTable.objects.filter(profile=profile)
                    context = {'userShares': userShares, "bidRange": bidRange,
                               'message': "Please Fill All The Fields",
                               "profile": profile, "sensex": sensex}
                    return render(request, self.template, context)
            except:
                userShares = UserShareTable.objects.filter(profile=profile)
                context = {'userShares': userShares, "bidRange": bidRange,
                           'message': "Invalid Bid",
                           "profile": profile, "sensex": sensex}
                return render(request, self.template, context)

            sharesAvailable = UserShareTable.objects.filter(profile=profile, company=company).first().bidShares
            if bidPrice > 0 and 0 < bidShares <= sharesAvailable and (1 - bidRange) * company.sharePrice <= bidPrice <= (1 + bidRange) * company.sharePrice:

                u = UserShareTable.objects.filter(company=company,
                                                  profile=profile).first()  # Get entry in userShareTable to remove shares
                if bidShares < u.bidShares:
                    # Check If selling lesser number of shares than present
                    u.bidShares -= bidShares
                    u.save()
                elif bidShares == u.bidShares:
                    u.delete()
                sellTable.objects.create(company=company.pk, profile=profile, bidShares=bidShares,
                                         bidPrice=bidPrice)  # Create a sellTable Entry
                match.delay(company, profile, bidPrice, bidShares, False)

                return render(request, 'bazaar/received_bid.html', {})
            else:
                userShares = UserShareTable.objects.filter(profile=profile)
                context = {'userShares': userShares, "bidRange": bidRange,
                           'message': "Invalid Bid",
                           "profile": profile, "sensex": sensex}
                return render(request, self.template, context)
        else:
            return render(request, self.error)


class NewsView(View):
    template = 'bazaar/news.html'

    def get(self, request):
        profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
        sensex = Global.objects.filter(pk=1).first().sensex
        news = News.objects.all()
        context = {"profile": profile, "sensex": sensex, "news": news[::-1]}
        return render(request, self.template, context)


def getPendingTransactions(profile):
    pending_buy_transactions = []
    pending_sell_transactions = []
    for company in Company.objects.all():
        exec("global buyTable; buyTable = BuyTable_" + company.tempName)
        exec("global sellTable; sellTable = SellTable_" + company.tempName)
        for buy_transaction in buyTable.objects.filter(profile=profile):
            pending_buy_transactions.append({
                'company': Company.objects.get(pk=buy_transaction.company),
                'bidShares': buy_transaction.bidShares,
                'bidPrice': buy_transaction.bidPrice
            })
        for sell_transaction in sellTable.objects.filter(profile=profile):
            pending_sell_transactions.append({
                'company': Company.objects.get(pk=sell_transaction.company),
                'bidShares': sell_transaction.bidShares,
                'bidPrice': sell_transaction.bidPrice
            })
    return pending_buy_transactions, pending_sell_transactions


class Transactions(View):
    template = 'bazaar/transactions.html'

    def get(self, request):
        profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
        sensex = Global.objects.filter(pk=1).first().sensex
        completed_transactions = UserHistory.objects.filter(profile=profile)
        pending_buy_transactions, pending_sell_transactions = getPendingTransactions(profile)
        context = {"profile": profile, "sensex": sensex, "completed_transactions": completed_transactions,
                   "pending_buy_transactions": pending_buy_transactions,
                   "pending_sell_transactions": pending_sell_transactions}
        return render(request, self.template, context)


class LeaderBoardView(View):
    template = 'bazaar/leaderboard.html'

    def get(self, request):
        profile = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
        g = Global.objects.filter(pk=1).first()
        sensex = g.sensex
        leaderboard = LeaderBoard.objects.all()
        update_time = g.LeaderBoardUpdateTime
        context = {"profile": profile, "sensex": sensex, "leaderboard": leaderboard, "update_time": update_time}
        return render(request, self.template, context)
