import requests
import time

url = "https://api.telegram.org/bot543539841:AAHDUPtmz1UHkj4UX7GvtrZoxlmmHI1Us0M/"
proxiesDick = {'socks':'tglive:tglive1@socks5://socks5.gq:1080'}
#proxiesDick = {'socks':'tglive:tglive1@91.211.247.111:1080'}
#offset_param={'offset': '343103821'}


def get_updates_json(request, params={'offset': '343103873'}):
    response = requests.get(request + 'getUpdates', params, proxies=proxiesDick)
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

okexUrl='https://www.okex.com/api/v1/future_ticker.do'
deriUrl='https://www.deribit.com/api/v1/public/getsummary'
btmxUrl='https://www.bitmex.com/api/v1/quote'
deriSym = 'BTC-29JUN18'
btmxSym = ['XBTM18', 'ETHM18', 'LTCM18', 'BCHM18', 'XRPM18']
okexSym = ['btc_usd', 'eth_usd', 'ltc_usd', 'bch_usd', 'xrp_usd']

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

def btmxGet(btxSym):
    btmxMarkt = []
    btmxParams = {'symbol': btxSym, 'count':'1', 'reverse':'true'}
    reqBtmx = requests.get(btmxUrl, btmxParams)
    btmxMarkt.append(reqBtmx.json()[0]['bidPrice'])
    btmxMarkt.append(reqBtmx.json()[0]['askPrice'])
    return(btmxMarkt)

while True:
    if update_id == last_update(get_updates_json(url))['update_id']:

        deriQ = [deriGet(deriSym)[0], deriGet(deriSym)[1]]
        bitmexQ = {k: btmxGet(k) for k in btmxSym}
        okexQ = {k: okexGet(k) for k in okexSym}

        basisBTC = {'btc okex': [(okexQ['btc_usd'][0] - deriQ[1]), (okexQ['btc_usd'][1] - deriQ[0])],
                    'btc btmx': [(bitmexQ['XBTM18'][0] - deriQ[1]), (bitmexQ['XBTM18'][1] - deriQ[0])]}
        basis = {'ltc': [2 * (okexQ['ltc_usd'][0] / (bitmexQ['XBTM18'][1]) - (bitmexQ['LTCM18'][1])) / (
                    bitmexQ['LTCM18'][0] + bitmexQ['LTCM18'][1]),
                         2 * (okexQ['ltc_usd'][1] / (bitmexQ['XBTM18'][0]) - (bitmexQ['LTCM18'][0])) / (
                                     bitmexQ['LTCM18'][0] + bitmexQ['LTCM18'][1])]}
        basis['eth'] = [2 * (okexQ['eth_usd'][0] / (bitmexQ['XBTM18'][1]) - (bitmexQ['ETHM18'][1])) / (
                    bitmexQ['ETHM18'][0] + bitmexQ['ETHM18'][1]),
                        2 * (okexQ['eth_usd'][1] / (bitmexQ['XBTM18'][0]) - (bitmexQ['ETHM18'][0])) / (
                                    bitmexQ['ETHM18'][0] + bitmexQ['ETHM18'][1])]
        basis['bch'] = [2 * (okexQ['bch_usd'][0] / (bitmexQ['XBTM18'][1]) - (bitmexQ['BCHM18'][1])) / (
                    bitmexQ['BCHM18'][0] + bitmexQ['BCHM18'][1]),
                        2 * (okexQ['bch_usd'][1] / (bitmexQ['XBTM18'][0]) - (bitmexQ['BCHM18'][0])) / (
                                    bitmexQ['BCHM18'][0] + bitmexQ['BCHM18'][1])]
        basis['xrp'] = [2 * (okexQ['xrp_usd'][0] / (bitmexQ['XBTM18'][1]) - (bitmexQ['XRPM18'][1])) / (
                    bitmexQ['XRPM18'][0] + bitmexQ['XRPM18'][1]),
                        2 * (okexQ['xrp_usd'][1] / (bitmexQ['XBTM18'][0]) - (bitmexQ['XRPM18'][0])) / (
                                    bitmexQ['XRPM18'][0] + bitmexQ['XRPM18'][1])]

        mess=str('BTC:\nOkex - Deribit (%.2f %.2f)\nBitmex - Deribit (%.2f %.2f)\nIchpochmak:\nLTC: (%.4f %.4f)\nETH: (%.4f %.4f)\nBCH: (%.4f %.4f)\nXRP: (%.4f %.4f)' %(basisBTC['btc okex'][0],basisBTC['btc okex'][1],basisBTC['btc btmx'][0],basisBTC['btc btmx'][1], basis['ltc'][0],basis['ltc'][1],basis['eth'][0],basis['eth'][1],basis['bch'][0],basis['bch'][1], basis['xrp'][0],basis['xrp'][1]))
        send_mess(get_chat_id(last_update(get_updates_json(url))), mess)
        update_id += 1
    time.sleep(30)





