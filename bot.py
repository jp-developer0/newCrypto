import config
from binance.client import Client
from binance.enums import *
import time

client = Client(config.API_KEY, config.API_SECRET, tld='com')

#FUNCTIONS
def truncate(number, digits) -> float:
    startCounting = False
    if number < 1:
      number_str = str('{:.20f}'.format(number))
      resp = ''
      count_digits = 0
      for i in range(0, len(number_str)):
        if number_str[i] != '0' and number_str[i] != '.' and number_str[i] != ',':
          startCounting = True
        if startCounting:
          count_digits = count_digits + 1
        resp = resp + number_str[i]
        if count_digits == digits:
            break
      return float(resp)
    else:
      return round(number)


prevCryptos = client.get_all_tickers()
prevLen = len(prevCryptos)

while 1:

  currentCryptos = client.get_all_tickers()
  currentLen = len(currentCryptos)
  
  if prevLen < currentLen:
    print("New Coin")
    newCoin = prevLen
    break
  print(prevLen)
  
for i in range (newCoin , currentLen):
  amount = 0
  symbol_to_buy = currentCryptos[i].get('symbol')
  price_to_buy = currentCryptos[i].get('price')
  if symbol_to_buy[-3:] == 'BTC':
    amount = 0.0013
  if symbol_to_buy[-3:] == 'ETH':
    amount = 0.03
  if symbol_to_buy[-4:] == 'USDT':
    amount = 15
  if symbol_to_buy[-4:] == 'BUSD':
    amount = 15
  if symbol_to_buy[-3:] == 'BNB':
    amount = 0.7

  if amount == 0:
    continue
  elif amount > 0:
    quantity_to_buy = truncate( (float(amount) / float(price_to_buy)) ,3 )
    initial_buy_order = client.order_limit_buy(
      symbol= symbol_to_buy,
      quantity = quantity_to_buy,
      price = truncate( price_to_buy ,3)
    )
    time.sleep(2)
    
    orderOCO = client.order_oco_sell(
                        symbol = symbol_to_buy,
                        quantity = quantity_to_buy,
                        price = truncate( price_to_buy *1.1,3),
                        stopPrice = truncate( price_to_buy *0.98,3),
                        stopLimitPrice = truncate( price_to_buy *0.975,3),
                        stopLimitTimeInForce = 'GTC'
                    )
    


