from .models import *
from .insertUtilities import *


def MatchBuy(company, user, buyPrice, noShares):
    # Get all the indexes of the table startindex, endindex
    buyStartIndex = company.buyStartPointer
    buyEndIndex = company.buyEndPointer
    sellStartIndex = company.sellStartPointer
    sellEndIndex = company.sellEndPointer
    baseIndex = company.basePointer

    try:
        # Getting the entries at start position, end position in the table
        startValue = BuyTable.objects.get(pk=buyStartIndex)
        endValue = BuyTable.objects.get(pk=buyEndIndex)
        mid = int((buyStartIndex + buyEndIndex) / 2)

        # If the new-buyprice is greater than old top entry
        if buyPrice > startValue.bidPrice:
            # Highest Bid, hence matching

            # Get the sellbid at top in selltable
            sellBid = SellTable.objects.get(pk=sellStartIndex)

            # If the new-shares are less than total sellshares then process only new-shares and
            # keep selltable entry as it is by reducing sellshares
            if noShares < sellBid.sellShares:
                # User Processing Remaining
                sellBid.sellShares -= noShares
                sellBid.save()

            # If new-shares are more, then remove entry from sell table and add user in buy table at top with
            # remaining shares
            if noShares > sellBid.sellShares:
                # User Processing Remaining
                # Apply for loop here for eliminating all possible shares
                insertFirst(BuyTable, buyPrice, noShares - sellBid.sellShares, company, user, buyStartIndex,
                            buyEndIndex)

        # If the new-buyprice entry is less than least buyprice in table

    except:
        # If no entry exist then create one at startindex
        BuyTable.objects.create(pk=buyStartIndex, company=company, profile=user, bidShares=noShares, bidPrice=buyPrice)
