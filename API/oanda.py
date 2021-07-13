

import requests
import numpy as np
import requests.api
import time
import threading
import traceback
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
        if update == True:
            t1 = threading.Thread(target = self.get_update)
            t1.daemon = True
            t1.start()
    #background update
    def get_update(self):
        while True:
            self.account_info = self.get_acct_info()
            # self.USD_CAD = self.get_USD_CAD()
            # self.USD_JPY = self.get_USD_JPY()
            # self.EUR_USD = self.get_EUR_USD()
            # self.EUR_CAD= self.get_EUR_CAD()
            # self.open_positions = self.get_open_positions()
            time.sleep(5)

    def __call_account(self):
        return self.s.get("https://api-fxpractice.oanda.com/v3/accounts/"+self.AccountID+"/summary",headers = {**self.Auth},timeout = 5)

    # get 500 mid candles datas in 2 minutes interval
    def __call_M_candles(self,pair,count):
        return self.s.get( "https://api-fxpractice.oanda.com/v3/instruments/"+pair+"/candles?count="+count+"&price=M&granularity="+TRADING_DATA_INTERVAL, headers = {**self.Auth},timeout = 5)

    # get 5000 ask+bid candles datas in 2 minutes interval
    def __call_BA_candles(self,pair,count):
        return self.s.get( "https://api-fxpractice.oanda.com/v3/instruments/"+pair+"/candles?count="+count+"&price=BA&granularity="+TRADING_DATA_INTERVAL, headers = {**self.Auth},timeout = 5)

    def __call_Positions(self):
        return self.s.get("https://api-fxpractice.oanda.com/v3/accounts/"+self.AccountID+"/openPositions",headers = {**self.Auth},timeout = 5)

    def __make_order(self,order):
        return self.s.post("https://api-fxpractice.oanda.com/v3/accounts/"+self.AccountID+"/orders", headers = {**self.Auth}, json = {**order},timeout = 5)

    # NAV = net asset value of this account || pl = life time total profit/loss || AVLmargin = the amount avaliable for invest
    def get_acct_info(self):
        try:
            response = self.__call_account()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return None
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
            return None