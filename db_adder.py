import MySQLdb
import logging
from jsonsList import valuta,pair_variant



def addToDBBinance(data, burseName, pairNameSym, valuesNameSym):
    logging.info("Начинаем заносить данные в бд")
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="all_price")
    cursor = db.cursor()

    for_add_name=data[f"{pairNameSym}"][:-1]
    for_add_value=str(data[f"{valuesNameSym}"])

    cursor.execute("INSERT INTO `price_" + burseName + "` (`symbol`, `value`) VALUES"
                                                       " ('" + for_add_name + "', '" + for_add_value + "') "
                                                                                                       "ON DUPLICATE KEY UPDATE value = '" +
                   for_add_value + "' , last_update = UNIX_TIMESTAMP();")

    db.commit()
    db.close()
    logging.info("Данные занесли в бд")



def addToDBOKX(data, burseName, pairNameSym, valuesNameSym):
    logging.info("Начинаем заносить данные в бд")
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="all_price")
    cursor = db.cursor()

    for_add_name=data.get("data")[0].get(f"{pairNameSym}")
    for_add_name=for_add_name[:-4].replace('-','')
    for_add_value=data.get("data")[0].get(f"{valuesNameSym}")
    cursor.execute("INSERT INTO `price_"+burseName+"` (`symbol`, `value`) VALUES"
                    " ('" + for_add_name  + "', '" + for_add_value + "') "
                                                                            "ON DUPLICATE KEY UPDATE value = '" +
                    for_add_value + "' , last_update = UNIX_TIMESTAMP();")


    db.commit()
    db.close()
    logging.info("Данные занесли в бд")



def addToDBcourseRate(data):
    logging.info("Обновляем таблицу валют")
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="all_price")
    cursor = db.cursor()
    symbol_num = 1
    for crypto_sym in data:
        el=str(crypto_sym[1])
        cursor.execute("INSERT INTO `price_valuta` (`symbol`, `value`) VALUES"
                                                           " ('" + crypto_sym[0] + "', '" + el + "') "
                                                 "ON DUPLICATE KEY UPDATE value = '" +
                       el + "' ;")
        symbol_num += 1

    db.commit()
    db.close()



def addToDBResult(name):
    fin_list=[]
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="all_price")
    cursor = db.cursor()
    cursor.execute("SELECT value FROM price_valuta WHERE symbol IN('USD')")
    USDCur=cursor.fetchall()[0][0]
    for symbols in pair_variant:
        for symbol in symbols:
            cursor.execute(f"SELECT value FROM price_{name} WHERE symbol IN('{symbol}USD')")
            cryptoValue = cursor.fetchall()[0][0]
        for currency in symbols.values():
            fin_value=cryptoValue/USDCur
            if currency == "RUB":
                fin_list.append([symbol+currency,float(fin_value)])
            else:
                cursor.execute(f"SELECT value FROM price_valuta WHERE symbol IN('{currency}')")
                fin_value = fin_value*cursor.fetchall()[0][0]
                fin_list.append([symbol+currency,float(fin_value)])

    for crypto_sym in fin_list:
        el=str(crypto_sym[1])
        cursor.execute("INSERT INTO `price_result` (`symbol`, `value`) VALUES"
                                                           " ('" + crypto_sym[0] + "', '" + el + "') "
                                                 "ON DUPLICATE KEY UPDATE value = '" +
                       el + "' ;")

    cursor.execute("INSERT INTO `Сurrent_market` (`text`, `value`) VALUES"
                                                           " ('Сurrent market:', '" + name + "') "
                                                 "ON DUPLICATE KEY UPDATE value = '" +
                       name + "' ;")

    db.commit()
    db.close()



def DBUpdateError(name):
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="all_price")
    cursor = db.cursor()
    cursor.execute("INSERT INTO `Сurrent_market` (`text`, `value`) VALUES"
                   " ('Сurrent market:', '" + name + "') "
                                                     "ON DUPLICATE KEY UPDATE value = '" +
                   name + "' ;")

    db.commit()
    db.close()