import config
from binance.client import Client
from binance.enums import *
import time
import threading
import math
import datetime

client = Client(config.API_KEY, config.API_SECRET, tld='com')
threadList = []

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

def diff(list1, list2):
    r = list(itertools.filterfalse(lambda x: x in list1, list2)) + list(itertools.filterfalse(lambda x: x in list2, list1))
    return r

def _dinamic_stop_loss_(symbol_to_buy, quantity_to_buy, price_to_buy):
    prevPrice_of_Symbol = float(price_to_buy)
    prevPrice_to_Take = truncate(float(price_to_buy) - float(price_to_buy) * 0.03,4)
    prevStopPrevPrice_to_Take = truncate(float(prevPrice_to_Take) + float(prevPrice_to_Take) * 0.01,4)
    try:
      order = client.create_order(
                  symbol=symbol_to_buy,
                  side='SELL',
                  type='STOP_LOSS_LIMIT',
                  quantity=quantity_to_buy,
                  price=float(prevPrice_to_Take),
                  stopPrice=float(prevStopPrevPrice_to_Take),
                  timeInForce='GTC')
      while 1:
        list_of_tickers = client.get_all_tickers()
        # DEBO ENCONTRAR UNA FUNCION QUE ME DE EL PRECIO ACTUAL DE UN TICKET
        for tick in list_of_tickers:
            if tick['symbol'] == symbol_to_buy:
                currentPrice_of_Symbol = float(tick['price'])
        # DEBO ENCONTRAR UNA FUNCION QUE ME DE EL PRECIO ACTUAL DE UN TICKET                
        currentPrice_to_Take = truncate(float(currentPrice_of_Symbol) - float(currentPrice_of_Symbol) * 0.03, 4)
        currentStopCurrentPrice_to_Take = truncate(float(currentPrice_to_Take) + float(currentPrice_to_Take) * 0.01, 4)
        if float(prevStopPrevPrice_to_Take) < float(currentStopCurrentPrice_to_Take):
          result = client.cancel_order(
              symbol=symbol_to_buy,
              orderId=order.get('orderId'))
          time.sleep(2)
          new_order = client.create_order(
                      symbol=symbol_to_buy,
                      side='SELL',
                      type='STOP_LOSS_LIMIT',
                      quantity=quantity_to_buy,
                      price=float(currentPrice_to_Take),
                      stopPrice=float(currentStopCurrentPrice_to_Take),
                      timeInForce='GTC')

          order = new_order
          
          prevStopPrevPrice_to_Take = float(currentStopCurrentPrice_to_Take)
        prevPrice_of_Symbol = float(currentPrice_of_Symbol)
    except Exception as e:
        print("an ERORR EN EL DINAMIC LOSS exception occured - {}".format(e))
        with open(symbol_to_buy+".txt", "a") as myfile:
            myfile.write(str(datetime.datetime.now()) +" - an exception occured - {}".format(e)+ " Oops! ERORR EN EL DINAMIC LOSS   occurred.\n")

# MAIN
prevCryptos = client.get_all_tickers()
prevLen = len(prevCryptos)
while 1:
  try:
      currentCryptos = client.get_all_tickers()
      currentLen = len(currentCryptos)
      if prevLen < currentLen:
          print("NEW CRYPTO")
          newCryptos = prevLen)
          break
      print(prevLen)
  except Exception as e:
      print("an exception occured - {}".format(e))
      print("Oops!", e. __class__ , "occurred....")
      with open("test.txt", "a") as myfile:
        myfile.write(str(datetime.datetime.now()) +" - an exception occured - {}".format(e)+ " WHILE CRASH  \n")
      client = Client(config.API_KEY, config.API_SECRET, tld='com')

for i in range(newCryptos,len(currentCryptos)):
  try:
    amount = 0
    symbol_to_buy = currentCryptos[i].get('symbol')
    price_to_buy = currentCryptos[i].get('price')
    if symbol_to_buy[-3:] == 'BTC':
      amount = 0.0013
    elif symbol_to_buy[-3:] == 'BNB':
      amount = 0.7
    elif symbol_to_buy[-3:] == 'SDT':
      amount = 15
    elif symbol_to_buy[-3:] == 'USD':
      amount = 15
    #elif symbol_to_buy[-3:] == 'ETH':
    #  amount = 0.03
    if amount == 0: 
    	continue
    if amount > 0:
        quantity_to_buy = truncate((float(amount) / float(price_to_buy)) , 3)

        with open("test.txt", "a") as myfile:
          myfile.write(str(datetime.datetime.now()) + " - " + symbol_to_buy+ " ; quantity:" + str(quantity_to_buy) + " ; Price " + str(price_to_buy) + "\n")

        initial_buy_order = client.order_limit_buy(
                                symbol=symbol_to_buy,
                                quantity=quantity_to_buy,
                                price=truncate(price_to_buy,3))
        time.sleep(5)

        x = threading.Thread(target=_dinamic_stop_loss_, args = (symbol_to_buy, quantity_to_buy, price_to_buy))
        x.start()
        threadList.append(x)
  except Exception as e:
    print("Oops!", e. __class__ , "occurred. IN FOR STATEMENT 178")
    with open("test.txt", "a") as myfile:
        myfile.write(str(datetime.datetime.now()) +" - an exception occured - {}".format(e)+ " Oops !  IN FOR STATEMENT 178 occurred.\n")
    client = Client(config.API_KEY, config.API_SECRET, tld='com')
