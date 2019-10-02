from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime


# User share table and User history - Improve Efficiency

# Create your models here.

class Global(models.Model):
    # Global Table
    sensex = models.FloatField(default=0)
    spread = models.IntegerField(default=0)
    LiveText = models.CharField(max_length=100)
    LeaderboardSize = models.IntegerField(default=100)
    LeaderBoardUpdateTime = models.DateTimeField(default=datetime.now)
    bidRangePercent = models.IntegerField(default=10, validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])
    registrationKey = models.CharField(max_length=20, default="abcde")
    startStopMarket = models.BooleanField(default=True)  # True => start, False => Stop
    startNews = models.BooleanField(default=False)
    NewsCounter = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Extending User Model
    rank = models.IntegerField(default=-1)  # Rank of the user
    numberOfShares = models.IntegerField(default=0)  # Number of shares owned by the user
    cash = models.IntegerField(default=200000)  # Cash remaining
    netWorth = models.IntegerField(default=0)  # Users networth; Required for leaderboard;

    # Calculated using cash and number of shares

    def __str__(self):
        return self.user.username


class Company(models.Model):
    # Table to store all the company data
    name = models.CharField(max_length=25)  # Name of the company
    tempName = models.CharField(max_length=25)
    sharePrice = models.IntegerField(default=0)  # Company's share price
    totalNoOfShares = models.IntegerField(default=0)  # Total number of shares available for sale
    sharesLeft = models.IntegerField(default=0)  # Number of shares left  ########(Redundant?)ny.objects.all()

    def __str__(self):
        return self.name


class UserShareTable(models.Model):
    # Table to store shares owned by the user
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company
    bidShares = models.IntegerField(default=0)  # Number of Shares owned

    def __str__(self):
        return str(self.profile) + ", " + str(self.company) + ", number: " + str(self.bidShares)


class UserHistory(models.Model):
    # Table to store transaction history of user
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company
    bidShares = models.IntegerField(default=0)  # Number of shares bought/sold
    bidPrice = models.IntegerField(default=0)  # Price at which shares were bought/sold
    buySell = models.BooleanField(default=1)  # Bought/sold flag; buy = 1, sell = 0
    transactionTime = models.DateTimeField(default=datetime.now)  # Transaction Time

    def __str__(self):
        return str(self.profile) + ", " + str(self.company) + ", Buy: " + str(self.buySell) + ", bidPrice: " + str(self.bidPrice) + ", bidShares: "+str(self.bidShares)


class BuyTable(models.Model):
    # Table to store buy requests
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    bidPrice = models.IntegerField(default=0)  # Buy Price
    bidShares = models.IntegerField(default=0)  # Number of shares
    transactionTime = models.DateTimeField(default=datetime.now)  # Transaction Time


class SellTable(models.Model):
    # Table to store sell requests
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    bidPrice = models.IntegerField(default=0)  # Sell Price
    bidShares = models.IntegerField(default=0)  # Number of shares
    transactionTime = models.DateTimeField(default=datetime.now)  # Transaction Time


class News(models.Model):
    # Table to store news
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class LeaderBoard(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.profile)


try:
    for i in Company.objects.all():
        exec("""
class BuyTable_""" + i.tempName + """(models.Model):
    # Table to store buy requests
    company = models.IntegerField(default=""" + str(i.pk) + """)  # Company
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    bidPrice = models.IntegerField(default=0)  # Buy Price
    bidShares = models.IntegerField(default=0)  # Number of shares
    transactionTime = models.DateTimeField(default=datetime.now)  # Transaction Time
    
    def __str__(self):
        return str(self.profile) + "- bidShares: " + str(self.bidShares) + ", bidPrice: " +str(self.bidPrice)

class SellTable_""" + i.tempName + """(models.Model):
    # Table to store sell requests
    company = models.IntegerField(default=""" + str(i.pk) + """)  # Company
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User
    bidPrice = models.IntegerField(default=0)  # Sell Price
    bidShares = models.IntegerField(default=0)  # Number of shares
    transactionTime = models.DateTimeField(default=datetime.now)  # Transaction Time
    
    def __str__(self):
        return str(self.profile) + "- bidShares: " + str(self.bidShares) + ", bidPrice: " +str(self.bidPrice)
    
        """)
except Exception as e:
    print("Partial MakeMigrations! Please Run migrate and then makemigrations Again")
