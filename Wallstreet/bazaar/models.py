from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


#User share table and User history - Improve Efficiency

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')  # Extending User Model
    rank = models.IntegerField(default=-1)  # Rank of the user
    numberOfShares = models.IntegerField(default=0)  # Number of shares owned by the user
    cash = models.IntegerField(default=380000)  # Cash remaining
    netWorth = models.IntegerField(
        default=0)  # Users networth; Required for leaderboard; Calculated using cash and number of shares
    numberOfCompanies = models.IntegerField(default=0)  ########################################################

    def __str__(self):
        return self.user.username


class Company(models.Model):
    # Table to store all the company data
    name = models.CharField(max_length=25)  # Name of the company
    sharePrice = models.IntegerField(default=0)  # Company's share price
    totalNoOfShares = models.IntegerField(default=0)  # Total number of shares available for sale
    sharesLeft = models.IntegerField(default=0)  # Number of shares left  ########(Redundant?)ny.objects.all()
    buyStartPointer = models.IntegerField(default=0)  # Start Location of company in buy table
    buyEndPointer = models.IntegerField(default=0)  # End location of comapany in buy table
    sellStartPointer = models.IntegerField(default=0)  # Start Location of company in sell table
    sellEndPointer = models.IntegerField(default=0)  # End Location of company in sell table
    basePointer = models.IntegerField(
        default=0)  # Base location in buy and sell table ;Required since start pointer can move down

    def __str__(self):
        return self.name


class UserShareTable(models.Model):
    # Table to store shares owned by the user
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    companyOwned = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company
    noOfCompanyShares = models.IntegerField(default=0)  # Number of Shares owned
    Price = models.IntegerField(default=0)  # Price at which the shares were bought


class UserHistory(models.Model):
    # Table to store transaction history of user
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company
    noShares = models.IntegerField(default=0)  # Number of shares bought/sold
    Price = models.IntegerField(default=0)  # Price at which shares were bought/sold
    buysell = models.BooleanField(default=0)  # Bought/sold flag; buy = 0, sell = 1
    transacTime = models.DateTimeField(default=datetime.now)  # Transaction Time
    pending = models.BooleanField(default=False)  # Pending transaction or approved transaction


class BuyTable(models.Model):
    # Table to store buy requests
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    bidPrice = models.IntegerField(default=0)  # Buy Price
    bidShares = models.IntegerField(default=0)  # Number of shares


class SellTable(models.Model):
    # Table to store sell requests
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company
    proile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    bidPrice = models.IntegerField(default=0)  # Sell Price
    bidShares = models.IntegerField(default=0)  # Number of shares


class News(models.Model):
    # Table to store news
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)


class Global(models.Model):
    # Global Table
    sensex = models.FloatField(default=0)
    spread = models.IntegerField(default=0)
    LiveText = models.CharField(max_length=100)


class LeaderBoard(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)