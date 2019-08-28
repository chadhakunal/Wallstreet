from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(UserShareTable)
admin.site.register(UserHistory)
admin.site.register(BuyTable)
admin.site.register(SellTable)
admin.site.register(News)
admin.site.register(Global)
admin.site.register(LeaderBoard)

try:
    for i in Company.objects.all():
        exec("""
admin.site.register(BuyTable_""" + i.tempName.replace(" ", "_") + """)
admin.site.register(SellTable_""" + i.tempName.replace(" ", "_") + """)
        """)
except:
    print("Buy Tables and Sell Tables Not Created")
