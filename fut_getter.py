import requests
import time


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

i=0

while i<20000:
    i+=1

    deriQ=[deriGet(deriSym)[0],deriGet(deriSym)[1]]
    bitmexQ={k:btmxGet(k) for k in btmxSym}
    okexQ={k:okexGet(k) for k in okexSym}


    basisBTC={'btc okex': [(okexQ['btc_usd'][0]-deriQ[1]),(okexQ['btc_usd'][1]-deriQ[0])], 'btc btmx': [(bitmexQ['XBTM18'][0]-deriQ[1]),(bitmexQ['XBTM18'][1]-deriQ[0])]}
    basis={'ltc':[2*(okexQ['ltc_usd'][0]/(bitmexQ['XBTM18'][1])-(bitmexQ['LTCM18'][1]))/(bitmexQ['LTCM18'][0]+bitmexQ['LTCM18'][1]), 2*(okexQ['ltc_usd'][1]/(bitmexQ['XBTM18'][0])-(bitmexQ['LTCM18'][0]))/(bitmexQ['LTCM18'][0]+bitmexQ['LTCM18'][1])]}
    basis['eth']=[2*(okexQ['eth_usd'][0]/(bitmexQ['XBTM18'][1])-(bitmexQ['ETHM18'][1]))/(bitmexQ['ETHM18'][0]+bitmexQ['ETHM18'][1]), 2*(okexQ['eth_usd'][1]/(bitmexQ['XBTM18'][0])-(bitmexQ['ETHM18'][0]))/(bitmexQ['ETHM18'][0]+bitmexQ['ETHM18'][1])]
    basis['bch']=[2*(okexQ['bch_usd'][0]/(bitmexQ['XBTM18'][1])-(bitmexQ['BCHM18'][1]))/(bitmexQ['BCHM18'][0]+bitmexQ['BCHM18'][1]), 2*(okexQ['bch_usd'][1]/(bitmexQ['XBTM18'][0])-(bitmexQ['BCHM18'][0]))/(bitmexQ['BCHM18'][0]+bitmexQ['BCHM18'][1])]
    basis['xrp']=[2*(okexQ['xrp_usd'][0]/(bitmexQ['XBTM18'][1])-(bitmexQ['XRPM18'][1]))/(bitmexQ['XRPM18'][0]+bitmexQ['XRPM18'][1]), 2*(okexQ['xrp_usd'][1]/(bitmexQ['XBTM18'][0])-(bitmexQ['XRPM18'][0]))/(bitmexQ['XRPM18'][0]+bitmexQ['XRPM18'][1])]

#print(basisBTC)
#print(basis)


    toWrite=list(basisBTC.values())
    toWrite+=(list(basis.values()))
    toWriteFlat=[]

    for el in toWrite:
        for i in el:
            toWriteFlat.append(i)

    csv_file=open('data.csv', 'a+')
    now=time.strftime("%Y-%m-%d %H:%M; ")
    csv_file.write(now)
    for k in range(len(toWriteFlat)):
        csv_file.write(str(toWriteFlat[k]))
        if k <(len(toWriteFlat)-1):
            csv_file.write('; ')
        else:
            csv_file.write('\n')
    csv_file.close()

    time.sleep(60)


