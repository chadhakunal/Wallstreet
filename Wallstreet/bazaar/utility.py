def setPointers(n):
    #n is the mnumber of bids for each company
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
