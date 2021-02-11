# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
from enum import Enum, auto
import time

class StockList(Enum):
     CODE = 0 #code of stocks (str)
     NAME = auto()
     UPDOWN = auto() #when to tell TRUE:UP FALSE:DOWN
     NOWPRICE = auto() #nowprice of stocks (int)
     STANDARD = auto() #standard value (int)
     STATE = auto() #Is it OK tweet? (Boolan)
     TWEET = auto() #Should we tweet? (Boolean)

class Request(Enum) :
    CODE = 0
    UPDOWN = auto()
    STANDARD = auto()

request = []
price = []
now_price = []
request.append(["5019", "DOWN", 2479])
request.append(["3390", "UP", 91])
price_list = [[0] * 2 for i in range(len(request))] #[[now_price][past_price]]
stock_list = [["0"] * len(StockList) for i in range(2)]

def makeStockList(prm_stock_list, prm_request) :
    for i in range(len(prm_request)) :
        prm_stock_list[i][StockList.CODE.value] = prm_request[i][Request.CODE.value]

        if prm_request[i][Request.UPDOWN.value] == "DOWN" :
            prm_stock_list[i][StockList.UPDOWN.value] = False
        else :
            prm_stock_list[i][StockList.UPDOWN.value] = True

        prm_stock_list[i][StockList.STANDARD.value] = prm_request[i][Request.STANDARD.value]

        if prm_stock_list[i][StockList.STATE.value] == "0" :
            prm_stock_list[i][StockList.STATE.value] = True

    return prm_stock_list

def getStockPrice(prm_stock_list) :
    ret = []
    for i in range(len(prm_stock_list)) :

        url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code={x}.T".format(x=request[i][Request.CODE.value])
        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response, "html.parser")

        tmp_price = str(soup.select("td.stoksPrice:nth-child(3)"))
        # tmp_price.replace('<td class="stoksPrice">', '')
        tmp_price = tmp_price.replace('[<td class="stoksPrice">', '')
        tmp_price = tmp_price.replace('</td>]', '')
        tmp_price = tmp_price.replace(',', '')
        tmp_price = int(tmp_price)
        prm_stock_list[i][StockList.NOWPRICE.value] = tmp_price

        tmp_name = str(soup.select(".symbol > h1:nth-child(1)"))
        tmp_name = tmp_name.replace('<h1>', '')
        tmp_name = tmp_name.replace('</h1>', '')
        tmp_name = tmp_name.replace('[', '')
        tmp_name = tmp_name.replace(']', '')
        prm_stock_list[i][StockList.NAME.value] = tmp_name

        if prm_stock_list[i][StockList.STATE.value] == True :
            if prm_stock_list[i][StockList.NOWPRICE.value] < prm_stock_list[i][StockList.STANDARD.value] :
                if prm_stock_list[i][StockList.UPDOWN.value] == False :
                    prm_stock_list[i][StockList.TWEET.value] = True
                else :
                    prm_stock_list[i][StockList.TWEET.value] = False
            elif prm_stock_list[i][StockList.NOWPRICE.value] >= prm_stock_list[i][StockList.STANDARD.value] :
                if prm_stock_list[i][StockList.UPDOWN.value] == True :
                    prm_stock_list[i][StockList.TWEET.value] = True
                else :
                    prm_stock_list[i][StockList.TWEET.value] = False
            else :
                prm_stock_list[i][StockList.TWEET.value] = False
        else :
            prm_stock_list[i][StockList.TWEET.value] = False
            if prm_stock_list[i][StockList.NOWPRICE.value] <= prm_stock_list[i][StockList.STANDARD.value] :
                if prm_stock_list[i][StockList.UPDOWN.value] == True :
                    prm_stock_list[i][StockList.STATE.value] = True
            elif prm_stock_list[i][StockList.NOWPRICE.value] > prm_stock_list[i][StockList.STANDARD.value] :
                if prm_stock_list[i][StockList.UPDOWN.value] == False :
                    prm_stock_list[i][StockList.STATE.value] = True
            else :
                prm_stock_list[i][StockList.STATE.value] = False
    return prm_stock_list

# for i in getStockPrice(request) :
#     print(i)

def genTweet(prm_stock_list) :
    tweet_list = []
    for i in prm_stock_list :
        # print(i)
        if i[StockList.TWEET.value] == True :
            if i[StockList.UPDOWN.value] == True :
                tmp_tweet = "{x0}(コード:{x1})の株価が基準値({x2}円)を上回りました".format(x0=i[StockList.NAME.value], x1=i[StockList.CODE.value], x2=i[StockList.STANDARD.value])
                tweet_list.append(tmp_tweet)
                i[StockList.STATE.value] = False
                i[StockList.TWEET.value] = False
            else :
                tmp_tweet = "{x0}(コード:{x1})の株価が基準値({x2}円)を下回りました".format(x0=i[StockList.NAME.value], x1=i[StockList.CODE.value], x2=i[StockList.STANDARD.value])
                tweet_list.append(tmp_tweet)

            i[StockList.STATE.value] = False
            i[StockList.TWEET.value] = False

    return tweet_list

# print(genTweet(pre_stock_list))

# stock_list = makeStockList(stock_list, request)
def main(prm_stock_list, prm_request) :
    while True :
        prm_stock_list = makeStockList(prm_stock_list, prm_request)
        # print(stock_list)
        prm_stock_list = getStockPrice(prm_stock_list)
        # print(stock_list)
        print(genTweet(prm_stock_list))
	# genTweetの内容をツイートする
        # print(stock_list)
        time.sleep(10)
        print("10")
        time.sleep(10)
        print("20")

main(stock_list, request)

