from os import replace
import requests
import numpy as np
import requests.api
import time
import threading
import traceback
from typing import List
PAIR_LIST = [
    "USD_CAD",
    "USD_JPY",
    "USD_HKD",
    "USD_CHF",
    "EUR_USD",
    "EUR_GBP",
    "EUR_CAD",
    "EUR_HKD",
    "GBP_USD",
    "GBP_CAD",
    "GBP_HKD",
    "AUD_USD",
    "AUD_CAD",
    "AUD_CHF",
    "CAD_CHF",
    "CAD_JPY",
    "CAD_HKD",
    "CAD_SGD",
    "NZD_CHF"]
TRADING_DATA_INTERVAL = "H1"

class OandaAPI:
    #initialization
    def __init__(self,AccountID,Token,update = False):
        self.AccountID = AccountID#"101-002-17879507-001"
        self.Token = Token#"a73b2d755e6ddfb8a2698158df957ab4-43cf4f968c9bbe8447b8a036f505a67a"
        self.Auth = {"Content-Type":"application/json","Authorization":"Bearer "+self.Token}
        self.interval = TRADING_DATA_INTERVAL
        self.s = requests.session()
        self.s.verify = True
        self.acct_info = []
        self.rates = []
        self.open_positions = []
        if update == True:
            t1 = threading.Thread(target = self.get_update)
            t1.daemon = True
            t1.start()
    #background update
    def get_update(self):
        while True:
            self.acct_info = self.get_acct_info()
            self.rates = self.rate_list(PAIR_LIST,count = 300)
            # self.USD_CAD = self.get_USD_CAD()
            # self.USD_JPY = self.get_USD_JPY()
            # self.EUR_USD = self.get_EUR_USD()
            # self.EUR_CAD= self.get_EUR_CAD()
            self.open_positions = self.get_open_positions()
            time.sleep(5)
#............................................................API CALLs...................................................
    def __call_account(self):
        return self.s.get("https://api-fxpractice.oanda.com/v3/accounts/"+self.AccountID+"/summary",headers = {**self.Auth},timeout = 5)
    # get 500 mid candles datas in 2 minutes interval
    def __call_M_candles(self,pair,count):
        return self.s.get( "https://api-fxpractice.oanda.com/v3/instruments/"+pair+"/candles?count="+str(count)+"&price=M&granularity="+TRADING_DATA_INTERVAL, headers = {**self.Auth},timeout = 5)
    # get 5000 ask+bid candles datas in 2 minutes interval
    def __call_BA_candles(self,pair,count):
        return self.s.get( "https://api-fxpractice.oanda.com/v3/instruments/"+pair+"/candles?count="+str(count)+"&price=BA&granularity="+TRADING_DATA_INTERVAL, headers = {**self.Auth},timeout = 5)
    def __call_Positions(self):
        return self.s.get("https://api-fxpractice.oanda.com/v3/accounts/"+self.AccountID+"/openPositions",headers = {**self.Auth},timeout = 5)
    def __make_order(self,order):
        return self.s.post("https://api-fxpractice.oanda.com/v3/accounts/"+self.AccountID+"/orders", headers = {**self.Auth}, json = {**order},timeout = 5)
    def __call_price(self,pair):
        return self.s.get("https://api-fxpractice.oanda.com/v3/accounts/"+self.AccountID+"/pricing?instruments="+pair,headers = {**self.Auth},timeout = 5)
#.........................................................................................................................
    # NAV = net asset value of this account || pl = life time total profit/loss || AVLmargin = the amount avaliable for invest
    def get_acct_info(self):
        try:
            response = self.__call_account()
        except:
            traceback.print_exc()
            return []
        if response.status_code == 200:
            response = response.json()
            return np.array(
                [response['account']['NAV'],
                response['account']['pl'],
                response['account']['marginAvailable'],
                response['account']['unrealizedPL'],
                response['account']['positionValue']
                ])
        else:
            return []
    
    # Return formant [['pair name','units','average price','pl']]
    def get_open_positions(self):
        try:
            response = self.__call_Positions()
        except:
            traceback.print_exc()
            return []
        if response.status_code == 200:
            response = response.json()
            postions = []
            if len(response) > 0:
                for i in range(len(response['positions'])):
                    if int(response['positions'][i]['long']['units']) != 0:
                        postions.append([
                            response['positions'][i]['instrument'].replace('_','/'),
                            response['positions'][i]['long']['units'],
                            response['positions'][i]['long']['averagePrice'],
                            response['positions'][i]['unrealizedPL'],
                            response['positions'][i]['marginUsed']
                            ])
                return np.array(postions)
            else:
                return []
        else:
            return []
    
    #return the pricelist (ask:[open,high,low,close],sell:[open,high,low,close]) To get just the buy and sell price use price[-1,:,3]
    def get_rate(self,pair,count = 300):
        try:
            response = self.__call_BA_candles(pair,count)
        except:
            traceback.print_exc()
            return []
        if response.status_code == 200:
            response = response.json()
            prices = []
            for i in range(len(response['candles'])):
                prices.append(
                    [
                        [
                            response['candles'][i]['ask']['o'],
                            response['candles'][i]['ask']['h'],
                            response['candles'][i]['ask']['l'],
                            response['candles'][i]['ask']['c']
                        ],
                        [
                            response['candles'][i]['bid']['o'],
                            response['candles'][i]['bid']['h'],
                            response['candles'][i]['bid']['l'],
                            response['candles'][i]['bid']['c']
                        ]
                    ])
            return [response['instrument'].replace('_','/'),np.array(prices)]
        else:
            return []
    
    #[pair name, pair rates][which pair][ask,bid][open,high,low,close]
    def rate_list(self,pair_list,count = 300) -> np.array:
        rates = []
        for i in pair_list:
            result = self.get_rate(i,count)
            if len(result) > 0:
                rates.append(result)
            else:
                return []
        return np.array(rates,dtype=object)
    
    #use negative value to sell
    def make_order(self,pair,units):
        order = {
            "order": {
                "units": units,
                "instrument": pair.replace('/','_'),
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT"
                } 
            }
        try:
            response = self.__make_order(order)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return None
        print(response.status_code)
        return response.status_code
    
    def get_price(self,pairs):
        pair_list=""
        for pair in pairs:
            if len(pairs) > 1:
                pair_list += pair.replace('/','_')+"%2C"
            else:
                pair_list = pair
        try:
            response = self.__call_price(pair_list)
            response = response.json()
            prices = []
            for i in range(len(response['prices'])):
                prices.append([
                    response['prices'][i]['instrument'],
                    response['prices'][i]['asks'][0]['price'],
                    response['prices'][i]['quoteHomeConversionFactors']['positiveUnits']
                ])
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return []
        return np.array(prices)
