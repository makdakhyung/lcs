import pyupbit

access = "qTPxJ6qRyQRJva4oz5UZ58oyszWPXdi3E6dSoZil"          # 본인 값으로 변경
secret = "L0RAAxgDeUT228JFh2gt1xJq1PxDKo44Zr9b9s5c"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

# print(upbit.get_balance("KRW-ETH"))     # KRW-XRP 조회
# print(upbit.get_balance("KRW"))         # 보유 현금 조회

# print(pyupbit.get_ohlcv("KRW-BTC", to="20210714", interval="minute1"))
# print(pyupbit.get_ohlcv("KRW-BTC", interval="minute1"))
print(pyupbit.get_orderbook(tickers="KRW-ETH")[0]["orderbook_units"][0]["ask_price"])

# balances = upbit.get_balances()
# balances
# for b in balances:
#     if b['currency'] == ticker:
#         if b['balance'] is not None:
#             return float(b['balance'])
#         else:
#             return 0
# return 0

df = pyupbit.get_ohlcv("KRW-ETH", interval="minute1", count=1)
start_time = df.index[0]
print(start_time)

balances = upbit.get_balances()
print(balances)