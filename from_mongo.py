import pandas as pd
import json
from itertools import groupby
import pymongo
import re
import sys


query = sys.argv[1:]
myclient = pymongo.MongoClient("8.209.74.127:27017")

mydb = myclient["reverseIndex"]
mycol = mydb["index"]

r = []

for  word in query:
    for i in mycol.find({"word" : word}):
        r.append(i)



def convert(ind):
    outlist = [ind['word'],]
    for k, v in ind['position'].items():
        outlist.append(k)
        outlist.append(str(len(v)))
        outlist.append(str(len(v)))
        for item in v:
            outlist.append(item)

    return " ".join(outlist)



a = ""
for i in r:
    a += convert(i) + "\n"
    
with open("index1.txt", 'w', encoding='uft-8') as f:
    f.write(a)
f.close()