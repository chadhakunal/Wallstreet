from .models import *

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

def setCompanyTempName():
    for i in Company.objects.all():
        i.tempName = ''.join(filter(str.isalnum,i.name))
        i.save()

    print("Temp Name Set!")


def resetCash():
    from bazaar.models import Profile
    for p in Profile.objects.all():
        p.cash = 380000
        p.save()