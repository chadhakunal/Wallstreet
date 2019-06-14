from __future__ import absolute_import, unicode_literals
from celery import task
from .models import *
from django.utils.crypto import get_random_string


# pip install eventlet
# install redis

# Run Redis Server  - "redis-server"
# Run Worker - "celery -A Wallstreet worker --pool=eventlet -l info"
# Run Scheduler Beat - "celery -A Wallstreet beat -l info"

# Add tasks in settings


@task()
def addNews():
    News.objects.create(title=get_random_string(10), description=get_random_string(50))


@task()
def LeaderBoardUpdateTask():
    cashValuationPercent = 0.4
    shareValuationPercent = 0.6

    companyStockPrices = {}

    for i in Company.objects.all():
        companyStockPrices[i.name] = i.sharePrice

    all_profiles = Profile.objects.all()
    for p in all_profiles:
        shareValuation = 0
        shareTableEntries = UserShareTable.objects.filter(profile=p)
        for entry in shareTableEntries:
            shareValuation += companyStockPrices[entry.company] * entry.bidShares

        p.netWorth = (cashValuationPercent * p.cash) + (shareValuationPercent * shareValuation)
        p.save()

    g = Global.objects.get(pk=1)
    numberOfEntries = min(g.LeaderboardSize,len(all_profiles))
    g.LeaderBoardUpdateTime = datetime.now()
    g.save()

    sorted_profiles = Profile.objects.all.order_by('-netWorth')[:numberOfEntries]

    LeaderBoard.objects.all().delete()

    for p in sorted_profiles:
        LeaderBoard.objects.create(profile=p)


