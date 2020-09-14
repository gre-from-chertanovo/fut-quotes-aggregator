import requests

okexUrl='https://okex.com/api/futures/v3/instruments/'


def okexGet(okSym):
    okexMarkt=[]
    reqOkex = requests.get(str(okexUrl+'/'+okSym+'/book'))
    okexMarkt.append(reqOkex.json()['bids'][0][0])
    okexMarkt.append(reqOkex.json()['asks'][0][0])
    return(okexMarkt)
print(okexGet('BTC-USD-201225'))


#print(okexGet('btc_usd'))