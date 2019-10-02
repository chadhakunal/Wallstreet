from __future__ import absolute_import, unicode_literals
from celery import task
from .models import *

from .matchUtilities import *
from datetime import datetime
import pandas as pd
import pytz

# pip install eventlet
# install redis

# Run Redis Server  - "redis-server"
# Run Worker - "celery -A Wallstreet worker --pool=eventlet -l info"
# Run Scheduler Beat - "celery -A Wallstreet beat -l info"

# Add tasks in settings

### ToDo: User bidshares validation
### ToDo: Send range to template
### ToDo: Hide validations
### ToDo: add spread
# ToDo: add sensex
### ToDO: add matchUtilities as a celery task
### ToDO: add 'spread' task
### ToDo: news upload only when market starts
# ToDo: Testing: Cash,NetWorth,Spread,Sensex,News,Leaderboard,matchUtilities in Celery,Buy/Sell Matching,emptyBuySellTable
# ToDo: Documentation
# ToDo: WebSockets
# ToDo: AWS hosting


news = pd.read_csv('news.csv')
buyTable = None
sellTable = None


@task()
def addNews():
    # ToDo: retrieve news from CSV file
    print("News Called")
    g = Global.objects.get(pk=1)
    if g.startStopMarket and g.startNews:
        global news
        if g.NewsCounter < news.shape[0]:
            new_news = news.iloc[g.NewsCounter, :]
            title = new_news.title
            description = new_news.description
            g.NewsCounter += 1
            g.save()
            #print(title, description)
            News.objects.create(title=title, description=description)
        else:
            return


@task()
def LeaderBoardUpdateTask():
    print("Leaderboard Task Called")
    cashValuationPercent = 0.4  # Values for netWorth
    shareValuationPercent = 0.6  # Values for netWorth

    # Dictionary to store the company and sharePrice
    companyStockPrices = {}

    for i in Company.objects.all():
        companyStockPrices[i.name] = i.sharePrice

    # Calculate Net Worth
    all_profiles = Profile.objects.all()  # Get all Profiles
    for p in all_profiles:
        # Calculate total value of shares
        shareValuation = 0
        shareTableEntries = UserShareTable.objects.filter(profile=p)  # Get all user shares
        for entry in shareTableEntries:
            shareValuation += companyStockPrices[entry.company.name] * entry.bidShares

        p.netWorth = (cashValuationPercent * p.cash) + (
                shareValuationPercent * shareValuation)  # Calculate net worth of user
        p.save()

    g = Global.objects.get(pk=1)  # Get Global Values
    numberOfEntries = min(g.LeaderboardSize, len(all_profiles))  # Get number of entries for leaderboard
    g.LeaderBoardUpdateTime = datetime.now()  # Set the latest leaderboard update time
    g.save()

    sorted_profiles = Profile.objects.all().order_by('-netWorth')

    LeaderBoard.objects.all().delete()  # Empty leader board

    for index, p in enumerate(sorted_profiles):
        # Updating ranks of all users
        profile = Profile.objects.get(pk=p.pk)
        profile.rank = index + 1
        profile.save()

    for p in sorted_profiles[:numberOfEntries]:
        # Add Entries to leader board
        LeaderBoard.objects.create(profile=p)


@task()
def emptyBuyTableSellTableTask():
    print("Rollback Called")
    for company in Company.objects.all():
        exec("global buyTable; buyTable = BuyTable_" + company.tempName)
        exec("global sellTable; sellTable = SellTable_" + company.tempName)

        sorted_buyTable = buyTable.objects.all().order_by('-bidPrice', 'transactionTime')  # Sort BuyTable Entries
        sorted_sellTable = sellTable.objects.all().order_by('bidPrice', 'transactionTime')  # Sort SellTable Entries

        i = 0  # Counter for sorted_buyTable
        j = 0  # counter for sorted_sellTable

        if sorted_buyTable:
        
            # If buying bids exist
            print("in sorted_buytable")

            while i < len(sorted_buyTable) and (j < len(sorted_sellTable) or company.sharesLeft):
                # Matching entries as long as possible
                if company.sharesLeft:
                    # if company has shares to sell
                    if not (j < len(sorted_sellTable)):
                        # If sorted_sellTable is empty check for company
                        if sorted_buyTable[i].bidPrice >= company.sharePrice:
                            # Buy Request is greater than comapany current price
                            flag = userCompanyTrasaction(company, buyTable, sorted_buyTable[
                                i])  # Perform transaction for company and buying user
                            i = i + (flag == 0)  # Update counter only if buyTable entry deleted
                            continue
                    # If sorted_sellTable has entry, but company.sharePrice is lesser than sellTable entry then
                    # sell shares of company
                    elif (j < len(sorted_sellTable)) and company.sharePrice < sorted_sellTable[j].bidPrice and \
                            sorted_buyTable[
                                i].bidPrice >= company.sharePrice:
                        # User Match with sorted_buyTable[i] with company shares (company shares is least priced)
                        flag = userCompanyTrasaction(company, buyTable,
                                                     sorted_buyTable[i])
                        # Perform transaction for company and buying user
                        i = i + (flag == 0)  # Update counter only if buyTable entry deleted
                        continue

                if (j < len(sorted_sellTable)) and sorted_sellTable and sorted_buyTable[i].bidPrice >= sorted_sellTable[
                    j].bidPrice:
                    # User Match with sorted_buyTable[i] and sorted_sellTable[j]
                    flag = userTransaction(company, buyTable, sellTable, sorted_buyTable[i],
                                           sorted_sellTable[j])  # Perform Transaction
                    i = i + (flag == -1 or flag == 0)
                    j = j + (flag == 1 or flag == 0)

                    # Based on the flag if buy shares are less then buy entry is deleted and i is incremented
                    # Based on the flag if buy shares are more then sell entry is deleted and j is incremented
                    # if flag is 0 then both are entries are delted and i,j are incremented
                else:
                    # None of the buy bids are higher than the sell bids (including company share price)
                    break

        # User Revoke if user placed a bid 1 hour ago or earlier
        tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now().astimezone(tz)
        #print("i: "+str(i)+" "+str(len(sorted_buyTable)))
        #print("j: "+str(j)+" "+str(len(sorted_sellTable)))
        #print(sorted_sellTable)
        while i < len(sorted_buyTable):
            if (current_time - sorted_buyTable[i].transactionTime).seconds >= 3600:
                #current_time.hour - sorted_buyTable[i].transactionTime.hour >= 1:
                userRevoke(sorted_buyTable[i], True)
                buyTable.objects.get(pk=sorted_buyTable[i].pk).delete()
            i += 1

        while j < len(sorted_sellTable):
            if (current_time - sorted_sellTable[j].transactionTime).seconds >= 3600:
                #current_time.hour - sorted_sellTable[i].transactionTime.hour >= 1:
                userRevoke(sorted_sellTable[j], False)
                sellTable.objects.get(pk=sorted_sellTable[j].pk).delete()
            j += 1


@task()
def spreadTask():
    print("Spread Distribution Called")
    profiles = {}
    totalTransaction = 0
    g = Global.objects.get(pk=1)
    for p in Profile.objects.all():
        profiles[p] = 0

    for u in UserHistory.objects.all():
        value = u.bidShares * u.bidPrice
        totalTransaction += value

        profiles[u.profile] += value

    for p in Profile.objects.all():
        spreadRatio = profiles[p]/totalTransaction
        p.cash += (spreadRatio * g.spread)
        p.save()

    g.spread = 0
    g.save()
