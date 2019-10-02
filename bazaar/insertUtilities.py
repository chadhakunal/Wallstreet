
def shift(Table, starting, ending):
    # Shift a companies buy table and sell table entries up/down
    if ending - starting > 0:
        # Down Shift
        for i in range(ending, starting - 1, -1):
            # Start from last object to entry object, shift each entry down( -1 )
            t = Table.objects.get(pk=i)
            temp = t
            t.pk = t.pk + 1
            t.save()
            temp.delete()
    elif ending - starting < 0:
        # Up shift
        for i in range(ending, starting + 1):  # Changed !!!
            # here ending < starting
            t = Table.objects.get(pk=i)
            temp = t
            t.pk = t.pk - 1
            t.save()
            temp.delete()


def insertFirst(Table, bidPrice, noShares, company, user, startIndex, endIndex):
    """
        Function: This function will be called when we want to insert the entry at the top in the table
        Use-cases: 1. If the new-buyEntry is having highest buyPrice than the current top entry
                   2. If the new-sellEntry is having highest sellPrice than the current top entry
                   - Used when nothing can be matched
        Algorithm:
            1. check whether the starting entry in the table exists at the base location of table or not
            2. If the index does not match (means there is free space at top of the table):
                2.1. Directly add the new entry above the current startindex of the table
            3. Otherwise:
                3.1. Check if table is full (by checking the difference in the startindex and endindex):
                    3.1.i. If the table is full:
                        3.1.i.a. eliminate last user and do its processing
                        3.1.i.b. shift all the entries down by 1
                        3.1.i.c. create the new entry at the startindex
                    3.1.ii. Else:
                        3.1.ii.a. shift all entries down by 1
                        3.1.ii.b. create the new entry at the startindex
    """
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
    """
        Function: This function will be used to add the entry in the middle of the table
        Algorithm:
            1. calculate the midindex of the table associated with company
            2. if the position at which new entry to be inserted is greater than midindex:
                2.1. Check if the table is not full:
                    # Means last position is entry
                    2.1.i. shift the entries from the position down by 1
                2.2. else if starting entries are empty:
                    2.2.i. shift the entries from start to the position up by 1
                2.3. otherwise:
                    # Means table is full
                    2.3.i. eliminate last user and do user processing
                    2.3.ii. shift the entries from position down by 1
            3. if the position lies above the midindex:
                3.1. if starting entries are empty:
                    3.1.i. shift the entries from start to position up by 1
                3.2. if the starting entries are full:
                    3.2.ii. shift the entries from position down by 1
                3.3 otherwise:
                    # Means table is full
                    3.3.i. eliminate last user and do user processing
                    3.3ii. shift the entries from position down by 1
            4. Now the position is free, add the new entry at that position
    """
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
            # If Position lies in Upper Part but Starting Positions are Full & Ending Positions are free then Shift Down
            shift(Table, position, endIndex)
        else:
            # If Position lies in Upper Part and table is Full then Delete Last Entry and Shift Down
            # Eliminate Last, User Processing Left
            shift(Table, position, endIndex)

    Table.objects.create(pk=position, company=company, profile=user,
                         bidShares=noShares,
                         bidPrice=bidPrice)


def insertLast(Table, bidPrice, noShares, company, user, startIndex, endIndex):
    """
        Function: This function will be used to add the entry in the last of the table
        Algorithm:
            1. Check if the last entries are empty:
                1.1. Insert the new entry at endIndex + 1 position
            2. Otherwise:
                2.1. If the starting positions are free:
                    2.1.i. Shift the entries from start to end up by 1
                    2.1.ii. Insert the new entry at the endIndex
    """
    if endIndex != company.basePointer + 99:
        Table.objects.create(pk=endIndex + 1, company=company, profile=user,
                             bidShares=noShares,
                             bidPrice=bidPrice)
    else:
        if startIndex != company.basePointer:
            shift(Table, endIndex, startIndex)
            Table.objects.create(pk=endIndex, company=company, profile=user,
                                 bidShares=noShares,
                                 bidPrice=bidPrice)