pair_variant=({'BTC': 'KZT'},{'BTC': 'GEL'},
              {'ETH': 'RUB'},{'ETH': 'USD'},
              # {'USDT': 'EUR'},{'USDT': 'KZT'},{'USDT': 'GEL'},
              # {'USDT': 'RUB'},{'USDT': 'USD'}
              )

valuta = ['USD', 'KZT', 'GEL', 'EUR']


addToLinkBinance=[
    'btcusdt@aggTrade',
    'ethusdt@aggTrade'
]

msgs_okx =\
    [
    {
        "op": "subscribe",  #Тикер возвращает только одну пару.
        "args": [
            {
              "channel": "tickers",
              "instId": "BTC-USD-SWAP"
            }

        ]
    },
    {
        "op": "subscribe",  #Тикер возвращает только одну пару.
        "args": [
            {
              "channel": "tickers",
              "instId": "ETH-USD-SWAP"
            }

        ]
    }
    ]



wss_list = \
    {
        "okx_wss": "wss://ws.okx.com:8443/ws/v5/public",#Ссылка верна
        "binance_wss": "wss://stream.binance.com:9443/ws/",#Ссылка верна. Тикер неверен
        'cbrf': 'https://www.cbr-xml-daily.ru/latest.js'#Не wss
    }

response_code= \
    {
        "oxk_codes" : [
            'okx', 'instId', 'last' #Данные коды являются верными
        ],
        "binance_codes" : [
            'binance', 's', 'p'  #Данные коды верны
        ]
    }

#python wsForAll.py
#python main.py
#locust -f locus_tests.py     http://127.0.0.1:5000