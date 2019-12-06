# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:22:55 2018
挖掘twitter tweets,找共现词,具体可见machine learning in action 235页
@author: Max Yang
"""

import twitter
from time import sleep
import re
import pandas as pd
import fpGrowth

def getLotsofTweets(searchStr):
    CONSUMER_KEY='4nDxF5gYmarjAcAVCs8B0zSEA'
    CONSUMER_SECRET='at8BWgNXWEWewqFLZD7fd1KK45x2hIRvUIGQvtZK8cGhzJMbiS'
    ACCESS_TOKEN_KEY='2181272090-8S7mIynrCwEpSrEoD5UsFOIF23YSvK6Z2RpcCQs'
    ACCESS_TOKEN_SECRET='4EZ7g4ZlaxDaxQ9F4qdcBAq63aGYCSmKVc0DUdzOvyAGU'
    api=twitter.Api(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN_KEY,
                    access_token_secret=ACCESS_TOKEN_SECRET)
    #you can get 1500 results 15 pages * 100 per page
    resultsPages=[]
    date_r=pd.date_range('2018-07-01','2018-07-14')
    date_list=date_r.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    for i in range(14):
        print("fetching page %d" % i)
        searchResults=api.GetSearch(searchStr, count=100,lang='en',since=date_list[i])
        resultsPages.append(searchResults)
        sleep(6)
    return(resultsPages)
    
def textParse(bigString):
    urlsRemoved=re.sub('(http[s]?:[/][/]|www.)([a-z][A-Z][0-9]|[/.][~])*','',bigString)
    if urlsRemoved=='':
        return(urlsRemoved)
    else:
        listofTokens=re.split(r'\W*',urlsRemoved)
        return([tok.lower() for tok in listofTokens if len(tok)>2])
    
def mineTweets(tweetArr,minSup=5):
    parsedList=[]
    for i in range(len(tweetArr)):
        for j in range(len(tweetArr[i])):
            #twitter爬出的数据是status类，因此需要status.text来找到实际需要的文本
            parsedList.append(textParse(tweetArr[i][j].text))
    initSet=fpGrowth.createInitSet(parsedList)
    myFPtree,myHeaderTab=fpGrowth.createTree(initSet,minSup)
    myFreqList=[]
    fpGrowth.mineTree(myFPtree,myHeaderTab,minSup,set([]),myFreqList)
    return(myFreqList)