import requests
import time
i=0
adresWex = 'https://wex.nz/api/3/ticker/'
adresYoba = 'https://yobit.net/api/3/ticker/'
adresFinex = 'https://api.bitfinex.com/v2/ticker/'
thresh=0.01
tickerWex=['btc_usd', 'ltc_btc', 'ltc_usd', 'dsh_btc', 'dsh_usd', 'dsh_ltc', 'dsh_eth', 'dsh_zec', 'eth_btc', 'eth_usd', 'eth_ltc', 'eth_zec', 'bch_usd', 'bch_btc', 'bch_ltc', 'bch_eth', 'bch_dsh', 'bch_zec', 'zec_btc', 'zec_usd', 'zec_ltc']
tickerYoba=['btc_usd', 'ltc_btc', 'ltc_usd', 'dash_btc', 'eth_btc', 'eth_usd', 'ltc_eth', 'zec_eth', 'bcc_usd', 'bcc_btc', 'bcc_eth', 'zec_btc', 'zec_usd']
tickerFinex=['BTCUSD', 'LTCBTC', 'LTCUSD', 'DSHBTC', 'ETHBTC', 'ETHUSD', 'BCHUSD', 'BCHBTC', 'ZECBTC', 'ZECUSD']






def pairsGetter():
    allinfo=requests.get('https://wex.nz/api/3/info')
    infoFromWex=(allinfo.json()['pairs'])
    return(list(infoFromWex.keys()))

#pairs=pairsGetter()
#print(pairs)
#pairs=list(filter(lambda x: x.find('eur')==-1, pairs))
#for el in pairs:
#    print(el.find('eur'))
#print(pairs)


#while i>5:
#    for j in range(len(pairs)-11):
#        ticker=pairs[j]
#        rWex=requests.get(adresWex+ticker)
#        rYoba = requests.get(adresYoba + ticker)
#        if rWex.json()[ticker]['sell'] > (rYoba.json()[ticker]['buy'])*(1+thresh):
#            print('Achtung %s'%ticker)
#        print(str(rWex.json()[ticker]['sell'])+' // ' + str(rWex.json()[ticker]['buy']))
#        print(str(rYoba.json()[ticker]['sell']) + ' // ' + str(rYoba.json()[ticker]['buy']))
    i+=1
    time.sleep(5)

#get Wex quotes and put into dicktionary
wexTickString=str()
wexQuotes={}
for n in range(len(tickerWex)):
    wexTickString+=tickerWex[n]
    if n==(len(tickerWex)-1):
        pass
    else:
        wexTickString+='-'

reqWex=requests.get(adresWex+wexTickString)

for u in tickerWex:
    wexQuotes[u]=[reqWex.json()[u]['sell'],reqWex.json()[u]['buy']]


#get Yoba quotes and put into dicktionary

yobaTickString=str()
yobaQuotes={}
for p in range(len(tickerYoba)):
    yobaTickString+=tickerYoba[p]
    if p==(len(tickerYoba)-1):
        pass
    else:
        yobaTickString+='-'

reqYoba=requests.get(adresYoba+yobaTickString)

for e in tickerYoba:
    yobaQuotes[e]=[reqYoba.json()[e]['buy'],reqYoba.json()[e]['sell']]
print(wexQuotes)
print(yobaQuotes)

#get Bitfinex quotes and put into dicktionary
finexQuotes={}
for b in tickerFinex:
    reqFinex = requests.get(adresFinex +'t'+ b)
    finexQuotes[b]=[reqFinex.json()[0],reqFinex.json()[2]]
    time.sleep(1)

print(finexQuotes)

wex=[wexQuotes['btc_usd'][0]/finexQuotes['BTCUSD'][0]-1, wexQuotes['eth_usd'][0]/finexQuotes['ETHUSD'][0]-1,wexQuotes['zec_usd'][0]/finexQuotes['ZECUSD'][0]-1,wexQuotes['dsh_btc'][0]/finexQuotes['DSHBTC'][0]-1,wexQuotes['ltc_usd'][0]/finexQuotes['LTCUSD'][0]-1,wexQuotes['bch_usd'][0]/finexQuotes['BCHUSD'][0]-1]
yoba=[yobaQuotes['btc_usd'][0]/finexQuotes['BTCUSD'][0]-1, yobaQuotes['eth_usd'][0]/finexQuotes['ETHUSD'][0]-1,yobaQuotes['zec_usd'][0]/finexQuotes['ZECUSD'][0]-1,yobaQuotes['dash_btc'][0]/finexQuotes['DSHBTC'][0]-1,yobaQuotes['ltc_usd'][0]/finexQuotes['LTCUSD'][0]-1,yobaQuotes['bcc_usd'][0]/finexQuotes['BCHUSD'][0]-1]
print(wex)
print(yoba)

zecUsdBtcY=((0.1*0.998*yobaQuotes['btc_usd'][0])/(1.002*yobaQuotes['zec_usd'][1])-0.02)*((0.998*wexQuotes['zec_usd'][0])/(wexQuotes['btc_usd'][1]*1.002))-0.1
print('Yield BTC-ZEC-BTC through USD Yoba %s'%zecUsdBtcY)
zecBtc=(1/(1.002*yobaQuotes['zec_btc'][1])-0.02)*0.998*(wexQuotes['zec_btc'][0])-1
print('zec throgh btc %s'%zecBtc)
zecEth=(1/(1.002*yobaQuotes['zec_eth'][1])-0.02)/(1.002*(wexQuotes['eth_zec'][1]))-1
print('zec throgh eth %s'%zecEth)