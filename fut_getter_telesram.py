import requests
import time
#import socks
#import socket

#ip='167.99.139.100'
#port = 1080
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
#socket.socket = socks.socksocket

url = "https://api.telegram.org/bot543539841:AAHDUPtmz1UHkj4UX7GvtrZoxlmmHI1Us0M/"
#proxiesDick = {'socks':'tglive:tglive1@socks5://socks5.gq:1080'}
#proxiesDick = {'socks':'tglive:tglive1@91.211.247.111:1080'}
#offset_param={'offset': '343103821'}


def get_updates_json(request, params={'offset': '178787816'}):
    response = requests.get(request + 'getUpdates', params)
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response


update_id = last_update(get_updates_json(url))['update_id']

#offset = last_update(get_updates_json(url))['update_id']
#telega_params={'offset': offset}

okexUrl='https://okex.com/api/futures/v3/instruments/'
deriUrl='https://www.deribit.com/api/v1/public/getsummary'
btmxUrl='https://www.bitmex.com/api/v1/orderBook/L2'
deriSym = 'BTC-25DEC20'
btmxSym = ['XBTZ20', 'ETHZ20', 'LTCZ20', 'BCHZ20', 'XRPZ20', 'EOSZ20']
okexSym = ['BTC-USD-201225', 'ETH-USD-201225', 'LTC-USD-201225', 'BCH-USD-201225', 'XRP-USD-201225', 'EOS-USD-201225']


#def okexGet(okSym):
#    okexMarkt=[]
#    okexParams = {'symbol': okSym, 'contract_type': 'quarter'}
#    reqOkex = requests.get(okexUrl, okexParams)
#    okexMarkt.append(reqOkex.json()['ticker']['buy'])
#    okexMarkt.append(reqOkex.json()['ticker']['sell'])
#    return(okexMarkt)

def okexGet(okSym):
    okexMarkt=[]
    reqOkex = requests.get(str(okexUrl+'/'+okSym+'/book'))
    okexMarkt.append(reqOkex.json()['bids'][0][0])
    okexMarkt.append(reqOkex.json()['asks'][0][0])
    okexMarkt=list(map(float, okexMarkt))
    return(okexMarkt)

def deriGet(derSym):
    deriMarkt=[]
    deriParams={'instrument': derSym}
    reqDeri=requests.get(deriUrl, deriParams)
    deriMarkt.append(reqDeri.json()['result']['bidPrice'])
    deriMarkt.append(reqDeri.json()['result']['askPrice'])
    return(deriMarkt)

#def btmxGet(btxSym):
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



while True:
    if update_id == last_update(get_updates_json(url))['update_id']:

        deriQ = [deriGet(deriSym)[0], deriGet(deriSym)[1]]
        bitmexQ = {k: btmxGet(k) for k in btmxSym}
        okexQ = {k: okexGet(k) for k in okexSym}

        basisBTC = {'btc okex': [(okexQ['BTC-USD-201225'][0] - deriQ[1]), (okexQ['BTC-USD-201225'][1] - deriQ[0])],
                    'btc btmx': [(bitmexQ['XBTZ20'][0] - deriQ[1]), (bitmexQ['XBTZ20'][1] - deriQ[0])]}
        basis = {'ltc': [2 * (okexQ['LTC-USD-201225'][0] / (bitmexQ['XBTZ20'][1]) - (bitmexQ['LTCZ20'][1])) / (
                    bitmexQ['LTCZ20'][0] + bitmexQ['LTCZ20'][1]),
                         2 * (okexQ['LTC-USD-201225'][1] / (bitmexQ['XBTZ20'][0]) - (bitmexQ['LTCZ20'][0])) / (
                                     bitmexQ['LTCZ20'][0] + bitmexQ['LTCZ20'][1])]}
        basis['eth'] = [2 * (okexQ['ETH-USD-201225'][0] / (bitmexQ['XBTZ20'][1]) - (bitmexQ['ETHZ20'][1])) / (
                    bitmexQ['ETHZ20'][0] + bitmexQ['ETHZ20'][1]),
                        2 * (okexQ['ETH-USD-201225'][1] / (bitmexQ['XBTZ20'][0]) - (bitmexQ['ETHZ20'][0])) / (
                                    bitmexQ['ETHZ20'][0] + bitmexQ['ETHZ20'][1])]
        basis['bch'] = [2 * (okexQ['BCH-USD-201225'][0] / (bitmexQ['XBTZ20'][1]) - (bitmexQ['BCHZ20'][1])) / (
                    bitmexQ['BCHZ20'][0] + bitmexQ['BCHZ20'][1]),
                        2 * (okexQ['BCH-USD-201225'][1] / (bitmexQ['XBTZ20'][0]) - (bitmexQ['BCHZ20'][0])) / (
                                    bitmexQ['BCHZ20'][0] + bitmexQ['BCHZ20'][1])]
        basis['xrp'] = [2 * (okexQ['XRP-USD-201225'][0] / (bitmexQ['XBTZ20'][1]) - (bitmexQ['XRPZ20'][1])) / (
                    bitmexQ['XRPZ20'][0] + bitmexQ['XRPZ20'][1]),
                        2 * (okexQ['XRP-USD-201225'][1] / (bitmexQ['XBTZ20'][0]) - (bitmexQ['XRPZ20'][0])) / (
                                    bitmexQ['XRPZ20'][0] + bitmexQ['XRPZ20'][1])]

        mess=str('BTC:\nOkex - Deribit (%.2f %.2f)\nBitmex - Deribit (%.2f %.2f)\nIchpochmak:\nLTC: (%.4f %.4f)\nETH: (%.4f %.4f)\nBCH: (%.4f %.4f)\nXRP: (%.4f %.4f)' %(basisBTC['btc okex'][0],basisBTC['btc okex'][1],basisBTC['btc btmx'][0],basisBTC['btc btmx'][1], basis['ltc'][0],basis['ltc'][1],basis['eth'][0],basis['eth'][1],basis['bch'][0],basis['bch'][1], basis['xrp'][0],basis['xrp'][1]))
        send_mess(get_chat_id(last_update(get_updates_json(url))), mess)
        update_id += 1
    time.sleep(30)





