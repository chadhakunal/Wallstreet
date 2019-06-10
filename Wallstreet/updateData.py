from bazaar.models import *
import pandas as pd

df = pd.read_csv("ws.csv")
cnt = 1
startpointer = 1
 
for i in range(1, 42):
    if (i == cnt * 8 + 1):
        cnt += 1
        startpointer=1

    volume = int(df.loc[i].loc["Volume"].split(",")[0])+int(df.loc[i].loc["Volume"].split(",")[1])
    Company.objects.create(name=df.loc[i].loc["NAME"], sharePrice=int(df.loc[i].loc["Share Price"])
    , totalNoOfShares=volume, sharesLeft=volume, tableType=cnt
    , startPointer=(((i % 8 - 1) * 100) + 1), endPointer=(((i % 8 - 1) * 100) + 1))
    
