import requests

okexUrl='https://okex.com/api/futures/v3/instruments/'
binanceUrl='https://www.binance.com/api/v3/depth'
deriUrl='https://www.deribit.com/api/v1/public/getsummary'
btmxUrl='https://www.bitmex.com/api/v1/orderBook/L2'

def okexGet(okSym):
    okexMarkt=[]
    reqOkex = requests.get(str(okexUrl+'/'+okSym+'/book'))
    okexMarkt.append(reqOkex.json()['bids'][0][0])
    okexMarkt.append(reqOkex.json()['asks'][0][0])
    okexMarkt=list(map(float, okexMarkt))
    return(okexMarkt)
print(okexGet('EOS-USD-201225'))

def binanceGet(binSym):
    binanceParams={'symbol':binSym, 'limit':5}
    binanceMarkt = []
    reqBinance = requests.get(binanceUrl, binanceParams)
    binanceMarkt.append(reqBinance.json()['bids'][0][0])
    binanceMarkt.append(reqBinance.json()['asks'][0][0])
    binanceMarkt = list(map(float, binanceMarkt))
    return(binanceMarkt)
#print(binanceGet('ETHBTC'))
print((okexGet('BTC-USD-201225')[0])*(binanceGet('ETHBTC')[0]))

def deriGet(derSym):
    deriMarkt=[]
    deriParams={'instrument': derSym}
    reqDeri=requests.get(deriUrl, deriParams)
    deriMarkt.append(reqDeri.json()['result']['bidPrice'])
    deriMarkt.append(reqDeri.json()['result']['askPrice'])
    return(deriMarkt)

def btmxGet(btxSym):
    btmxMarkt = []
    btmxParams = {'symbol': btxSym, 'depth':'1'}
    reqBtmx = requests.get(btmxUrl, btmxParams)
    btmxMarkt.append(reqBtmx.json()[1]['price'])
    btmxMarkt.append(reqBtmx.json()[0]['price'])
    return(btmxMarkt)

print(btmxGet('XBTU20'))
