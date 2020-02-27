import pandas as pd
import json
from itertools import groupby
import pymongo
import re
import sys
import json


def convert(ind):
    outlist = [ind['word'],]
    for k, v in ind['position'].items():
        outlist.append(k)
        outlist.append(str(len(v)))
        outlist.append(str(len(v)))
        for item in v:
            outlist.append(item)
    return outlist

    
def get_position(query):
    
    myclient = pymongo.MongoClient("8.209.74.127:27017")

    mydb = myclient["reverseIndex"]
    mycol = mydb["index"]
    
    r = []

    for  word in query:
        for i in mycol.find({"word" : word}):
            r.append(i)
            
    totallist = [convert(i) for i in r]
    
    return json.dumps(totallist)