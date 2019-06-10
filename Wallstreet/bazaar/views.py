from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *


# Create your views here.


def shift(Table, starting, ending):
    if ending - starting > 0:
        # Down Shift
        for i in range(ending, starting - 1, -1):
            t = Table.objects.get(pk=i)
            temp = t
            t.pk = t.pk + 1
            t.save()
            temp.delete()
    elif ending - starting < 0:
        # Up shift
        for i in range(ending, starting + 1):      # Changed !!!
            t = Table.objects.get(pk=i)
            temp = t
            t.pk = t.pk - 1
            t.save()
            temp.delete()


def insertFirst(Table, bidPrice, noShares, company, user, startIndex, endIndex):
    if startIndex != company.basePointer:
        Table.objects.create(pk=startIndex - 1, company=company, profile=user,
                             bidShares=noShares,
                             bidPrice=bidPrice)
    else:
        if endIndex - startIndex == 99:
            # Eliminate Last , User Processing
            shift(Table, startIndex, endIndex)
            Table.objects.create(pk=startIndex, company=company, profile=user,
                                 bidShares=noShares,
                                 bidPrice=bidPrice)
        else:
            shift(Table, startIndex, endIndex)
            Table.objects.create(pk=startIndex, company=company, profile=user,
                                 bidShares=noShares,
                                 bidPrice=bidPrice)


def insertMiddle(Table, bidPrice, noShares, company, user, startIndex, endIndex, position):
    midIndex = (startIndex + endIndex) / 2
    if position > midIndex:
        if endIndex != company.basePointer + 99:
            # If Last Position in table is/are empty and Position lies below midIndex then shift down
            shift(Table, position, endIndex)
        elif startIndex != company.basePointer:
            # If Position is greater than midIndex and Last Position not Empty but Starting positions are Empty then
            # Shift Up
            shift(Table, position, startIndex)
        else:
            # If Position is greater than midIndex and No free position in table then Delete Last entry from the table
            # Eliminate Last, User Processing Left
            shift(Table, position, endIndex)
    else:
        if startIndex != company.basePointer:
            # If Position lies in Upper Part and Starting Positions are free then Shift Up
            shift(Table, position, startIndex)
        elif endIndex != company.basePointer + 99:
            # If Position lies in Upper Part but Starting Positions are Full and Ending Positions are free then Shift Down
            shift(Table, position, endIndex)
        else:
            # If Position lies in Upper Part adn table is Full then Delete Last Entry and Shift Down
            # Eliminate Last, User Processing Left
            shift(Table, position, endIndex)

    Table.objects.create(pk=position, company=company, profile=user,
                         bidShares=noShares,
                         bidPrice=bidPrice)


def matchBuy(company, user, buyPrice, noShares):
    if company.tableType == 1:
        buyTable = BuyTableType1
        sellTable = SellTableType1
    elif company.tableType == 2:
        buyTable = BuyTableType2
        sellTable = SellTableType2
    elif company.tableType == 3:
        buyTable = BuyTableType3
        sellTable = SellTableType3
    elif company.tableType == 4:
        buyTable = BuyTableType4
        sellTable = SellTableType4
    else:
        buyTable = BuyTableType5
        sellTable = SellTableType5

    buyStartIndex = company.buyStartPointer
    buyEndIndex = company.buyEndPointer
    sellStartIndex = company.sellStartPointer
    sellEndIndex = company.sellEndPointer

    try:
        startValue = buyTable.objects.get(pk=buyStartIndex)
        endValue = buyTable.objects.get(pk=buyEndIndex)
        mid = int((buyStartIndex + buyEndIndex) / 2)

        if buyPrice > startValue.bidPrice:
            # Highest Bid, hence matching
            sellBid = sellTable.objects.get(pk=sellStartIndex)
            if noShares < sellBid.sellShares:
                # User Processing Remaining
                sellBid.sellShares -= noShares
                sellBid.save()

            if noShares > sellBid.sellShares:
                # User Processing Remaining
                insertFirst(buyTable, buyPrice, noShares - sellBid.sellShares, company, user, buyStartIndex,
                            buyEndIndex)



    except:
        buyTable.objects.create(pk=buyStartIndex, company=company, profile=user, bidShares=noShares, bidPrice=buyPrice)


class index(View):
    def get(self, request):
        return HttpResponse("<h1>Test</h1>")





















