from .models import *
import pandas as pd
from django.contrib.auth.models import User


def setPointers(n):
    # n is the mnumber of bids for each company
    cnt = 1
    from bazaar.models import Company

    for i in Company.objects.all():
        i.buyStartPointer = cnt
        i.sellStartPointer = cnt
        i.basePointer = cnt
        i.buyEndPointer = cnt + n - 1
        i.sellEndPointer = cnt + n - 1
        i.save()

        cnt = cnt + n
    print("Pointers Saved!")


def setCompanyTempName():
    for i in Company.objects.all():
        i.tempName = ''.join(filter(str.isalnum, i.name))
        i.save()

    print("Temp Name Set!")


def resetCash():
    from bazaar.models import Profile
    for p in Profile.objects.all():
        p.cash = 200000
        p.save()


def add_company(csvfile):
    companyData = pd.read_csv("company_data.csv")
    for cnt, i in enumerate(companyData["name"]):
        print(i)
        Company.objects.create(name=i, sharePrice=companyData["sharePrice"][cnt], totalNoOfShares=companyData["numberOfShares"][cnt], sharesLeft=companyData["numberOfShares"][cnt])

    setCompanyTempName()


def create_test_users(users):
    for i in users:
        user = User.objects.create_user(username=i)
        user.set_password(i)
        user.save()

        profile = Profile.objects.create(user=user)
        profile.save()
    print("Users Created!")
