import websockets
import asyncio
import logging
import json
from db_adder import *
from jsonsList import *
from switcher import switcher
from coursesRate import *

logging.basicConfig(level=logging.INFO, filename="socket.log")

message1 = msgs_okx[0]
message2 = msgs_okx[1]

adder1=addToLinkBinance[0]
adder2=addToLinkBinance[1]


async def streamBin(url, add):
    url=url+add
    data_bin = response_code.get("binance_codes")
    while True:
        try:
            logging.info("Начинаем подключение к вебсокету Бинанса")
            async with websockets.connect(url, ping_interval=None) as client:
                while True:
                    data = json.loads(await client.recv())
                    addToDBBinance(data, f'{data_bin[0]}', f'{data_bin[1]}', f'{data_bin[2]}')
                    await asyncio.sleep(5)
            switcher.update({'binance':0})

        except Exception:
            switcher.update({'binance':1})
            logging.error("не получилось подключиться в Binance")
            await asyncio.sleep(50)



async def streamOKX(url, message):
    data_okx = response_code.get("oxk_codes")
    while True:
        try:
            logging.info("Начинаем подключение к вебсокету ОКХ")
            async with websockets.connect(url, ping_interval=None) as client:
                await client.send(json.dumps(message))
                while True:
                    data = json.loads(await client.recv())
                    addToDBOKX(data, f'{data_okx[0]}', f'{data_okx[1]}', f'{data_okx[2]}')
                    await asyncio.sleep(5)
            switcher.update({'okx':0})

        except Exception:
            switcher.update({'okx':1})
            logging.error("не удалось подключиться в ОКХ")
            await asyncio.sleep(50)



async def streamForex(url):
    while True:
        list_rate = rateToday(url)
        addToDBcourseRate(list_rate)
        await asyncio.sleep(60)



async def updateDB(switcher):
    while True:
        if switcher.get('okx')==0:
            addToDBResult(name='okx')
        elif switcher.get('binance')==0:
            addToDBResult(name='binance')
        else:
            name = 'conection lost'
            DBUpdateError()
            logging.warning('отсутствует подключение по всем вебсокетам')
        await asyncio.sleep(5)



def mainSouth():
    data = wss_list
    tasks = [
                data.get("okx_wss"),
                data.get("binance_wss"),
                data.get('cbrf')
            ]
    asyncio.get_event_loop().run_until_complete(asyncio.wait([
        streamOKX(tasks[0], message1),
        streamOKX(tasks[0], message2),
        streamBin(tasks[1], adder1),
        streamBin(tasks[1], adder2),
        streamForex(tasks[2]),
        updateDB(switcher)
    ]))

if __name__ == '__main__':
    mainSouth()
