import requests


url = "https://api.telegram.org/bot543539841:AAHDUPtmz1UHkj4UX7GvtrZoxlmmHI1Us0M/"
proxiesDick = {'socks':'tglive:tglive1@socks5://socks5.gq:1080'}
#proxiesDick = {'socks':'tglive:tglive1@91.211.247.111:1080'}
#offset_param={'offset': '343103821'}



#telega_params={'offset': offset}

okexUrl='https://www.okex.com/api/v1/future_ticker.do'
deriUrl='https://www.deribit.com/api/v1/public/getsummary'
#btmxUrl='https://www.bitmex.com/api/v1/quote'  #changed to L2 orderbook
btmxUrl='https://www.bitmex.com/api/v1/orderBook/L2'
deriSym = 'BTC-27SEP19'
btmxSym = ['XBTU19', 'ETHU19', 'LTCU19', 'BCHU19', 'XRPU19', 'EOSU19', 'TRXU19']
okexSym = ['btc_usd', 'eth_usd', 'ltc_usd', 'bch_usd', 'xrp_usd', 'eos_usd', 'trx_usd']

def okexGet(okSym):
    okexMarkt=[]
    okexParams = {'symbol': okSym, 'contract_type': 'quarter'}
    reqOkex = requests.get(okexUrl, okexParams)
    okexMarkt.append(reqOkex.json()['ticker']['buy'])
    okexMarkt.append(reqOkex.json()['ticker']['sell'])
    return(okexMarkt)

def deriGet(derSym):
    deriMarkt=[]
    deriParams={'instrument': derSym}
    reqDeri=requests.get(deriUrl, deriParams)
    deriMarkt.append(reqDeri.json()['result']['bidPrice'])
    deriMarkt.append(reqDeri.json()['result']['askPrice'])
    return(deriMarkt)

#def btmxGet(btxSym):     ## bitmex api do not respond. request changed to L2 orderbook
#    btmxMarkt = []
#    btmxParams = {'symbol': btxSym, 'count':'1', 'reverse':'true'}
#    reqBtmx = requests.get(btmxUrl, btmxParams)
#    btmxMarkt.append(reqBtmx.json()[0]['bidPrice'])
#    btmxMarkt.append(reqBtmx.json()[0]['askPrice'])
#    return(btmxMarkt)

def btmxGet(btxSym):
    btmxMarkt = []
    btmxParams = {'symbol': btxSym, 'depth':'1'}
    reqBtmx = requests.get(btmxUrl, btmxParams)
    btmxMarkt.append(reqBtmx.json()[1]['price'])
    btmxMarkt.append(reqBtmx.json()[0]['price'])
    return(btmxMarkt)

deriQ = [deriGet(deriSym)[0], deriGet(deriSym)[1]]
bitmexQ = {k: btmxGet(k) for k in btmxSym}
okexQ = {k: okexGet(k) for k in okexSym}


basisBTC = {'btc okex': [(okexQ['btc_usd'][0] - deriQ[1]), (okexQ['btc_usd'][1] - deriQ[0])],
                'btc btmx': [(bitmexQ['XBTU19'][0] - deriQ[1]), (bitmexQ['XBTU19'][1] - deriQ[0])]}
basis = {'ltc': [2 * (okexQ['ltc_usd'][0] / (bitmexQ['XBTU19'][1]) - (bitmexQ['LTCU19'][1])) / (
                bitmexQ['LTCU19'][0] + bitmexQ['LTCU19'][1]),
                     2 * (okexQ['ltc_usd'][1] / (bitmexQ['XBTU19'][0]) - (bitmexQ['LTCU19'][0])) / (
                                 bitmexQ['LTCU19'][0] + bitmexQ['LTCU19'][1])]}
basis['eth'] = [2 * (okexQ['eth_usd'][0] / (bitmexQ['XBTU19'][1]) - (bitmexQ['ETHU19'][1])) / (
                    bitmexQ['ETHU19'][0] + bitmexQ['ETHU19'][1]),
                        2 * (okexQ['eth_usd'][1] / (bitmexQ['XBTU19'][0]) - (bitmexQ['ETHU19'][0])) / (
                                    bitmexQ['ETHU19'][0] + bitmexQ['ETHU19'][1])]
basis['bch'] = [2 * (okexQ['bch_usd'][0] / (bitmexQ['XBTU19'][1]) - (bitmexQ['BCHU19'][1])) / (
                    bitmexQ['BCHU19'][0] + bitmexQ['BCHU19'][1]),
                        2 * (okexQ['bch_usd'][1] / (bitmexQ['XBTU19'][0]) - (bitmexQ['BCHU19'][0])) / (
                                    bitmexQ['BCHU19'][0] + bitmexQ['BCHU19'][1])]
basis['xrp'] = [2 * (okexQ['xrp_usd'][0] / (bitmexQ['XBTU19'][1]) - (bitmexQ['XRPU19'][1])) / (
                    bitmexQ['XRPU19'][0] + bitmexQ['XRPU19'][1]),
                        2 * (okexQ['xrp_usd'][1] / (bitmexQ['XBTU19'][0]) - (bitmexQ['XRPU19'][0])) / (
                                    bitmexQ['XRPU19'][0] + bitmexQ['XRPU19'][1])]
basis['eos'] = [2 * (okexQ['eos_usd'][0] / (bitmexQ['XBTU19'][1]) - (bitmexQ['EOSU19'][1])) / (
                    bitmexQ['EOSU19'][0] + bitmexQ['EOSU19'][1]),
                        2 * (okexQ['eos_usd'][1] / (bitmexQ['XBTU19'][0]) - (bitmexQ['EOSU19'][0])) / (
                                    bitmexQ['EOSU19'][0] + bitmexQ['EOSU19'][1])]
basis['trx'] = [2 * (okexQ['trx_usd'][0] / (bitmexQ['XBTU19'][1]) - (bitmexQ['TRXU19'][1])) / (
                    bitmexQ['TRXU19'][0] + bitmexQ['TRXU19'][1]),
                        2 * (okexQ['trx_usd'][1] / (bitmexQ['XBTU19'][0]) - (bitmexQ['TRXU19'][0])) / (
                                    bitmexQ['TRXU19'][0] + bitmexQ['TRXU19'][1])]

mess=str('BTC:\nOkex - Deribit (%.2f %.2f)\nBitmex - Deribit (%.2f %.2f)\nIchpochmak:\nLTC: (%.4f %.4f)\nETH: (%.4f %.4f)\nBCH: (%.4f %.4f)\nXRP: (%.4f %.4f)\nEOS: (%.4f %.4f)\nTRX: (%.4f %.4f)' %(basisBTC['btc okex'][0],basisBTC['btc okex'][1],basisBTC['btc btmx'][0],basisBTC['btc btmx'][1], basis['ltc'][0],basis['ltc'][1],basis['eth'][0],basis['eth'][1],basis['bch'][0],basis['bch'][1], basis['xrp'][0],basis['xrp'][1], basis['eos'][0],basis['eos'][1], basis['trx'][0],basis['trx'][1]))
print( mess)







