import time
import pyupbit
import datetime

access = "qTPxJ6qRyQRJva4oz5UZ58oyszWPXdi3E6dSoZil"          # 본인 값으로 변경
secret = "L0RAAxgDeUT228JFh2gt1xJq1PxDKo44Zr9b9s5c"          # 본인 값으로 변경

def get_balance(ticker):
    """보유량 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_avg_buy_price(ticker):
    """평단가 조회"""
    avg_buy_prices = upbit.get_balances()
    for a in avg_buy_prices:
        if a['currency'] == ticker:
            if a['avg_buy_price'] is not None:
                return float(a['avg_buy_price'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회 (=호가창 매수 희망 최고가) """
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["bid_price"]
      

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


# 필요변수
coin_name = "KRW-LINK"
coin = "LINK"
k = 0.06
seed = 1000000
split = 100
unit_price = 10000
balance = 0
avg_buy_price = 0
time_change = 0


# 자동매매 시작
input_qty = 0
while True:
    try:        
        now = datetime.datetime.now()
        start_time = pyupbit.get_ohlcv(coin_name, interval="day", count=1).index[0]
        end_time = start_time + datetime.timedelta(hours=24)
        
        if start_time < now < end_time:  
            avg_buy_price = get_avg_buy_price(coin)
            balance = get_balance(coin)   
            current_price = get_current_price(coin_name)
            df = pyupbit.get_ohlcv(coin_name, interval="minute60", count=2)
            increase_rate = (df.iloc[0]['close'] - df.iloc[0]['open']) / df.iloc[0]['open']
            if avg_buy_price == 0:
                if input_qty != 0:
                    input_qty = 0
                
            if (avg_buy_price == 0) | (avg_buy_price*(1+k) >= current_price):      
                if (time_change == 0) | (time_change == pyupbit.get_ohlcv(coin_name, interval="minute60", count=2).index[0]):   
                    if input_qty < split:
                        if (avg_buy_price > df.iloc[0]['close']) | (increase_rate < (k/2)):
                            if (avg_buy_price > df.iloc[0]['close']) & (increase_rate < (k/2)):
                                upbit.buy_market_order(coin_name, unit_price*2)
                                input_qty += 2
                            else:
                                upbit.buy_market_order(coin_name, unit_price)
                                input_qty += 1   
                    else:
                        upbit.sell_market_order(coin_name, balance)
                        input_qty = 0  
                        
                    time_change = pyupbit.get_ohlcv(coin_name, interval="minute60", count=2).index[1]

            else:
                upbit.sell_market_order(coin_name, balance)
                input_qty = 0 
                
        time.sleep(1)
            
    except Exception as e:
        print(e)
        time.sleep(1)

