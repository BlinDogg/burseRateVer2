from flask import Flask, request
import logging
import MySQLdb
from jsonsList import pair_variant
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.INFO, filename="backend.log")

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="all_price")

data=[]

def sensor():
    my_cursor = db.cursor()
    my_cursor.execute("SELECT * FROM price_result")
    rate_data = my_cursor.fetchall()
    my_cursor.execute("SELECT * FROM сurrent_market")
    name = my_cursor.fetchall()[0]
    my_cursor.close()
    data.clear()
    data.append((rate_data, name))
    print('aaaa')

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=5)
sched.start()



app = Flask(__name__)



@app.route("/")
def index():
    return "<h1>Главная страница"

@app.route("/courses")
def courses_all():
    logging.info("Запрос на все курсы")
    data_string = str()
    rate_data=data[0][0]
    name=data[0][1]

    for element in rate_data:
        data_string=data_string+element[0]+' = '+str(element[1])+'<br>'

    return f"<h1>{data_string}{name[0]+' '+name[1]}"

@app.route("/pare")
def courses_pair():
    logging.info("Запрос на пару")

    first_pare = request.args.get('coin')
    second_pare = request.args.get('currency')
    logging.info(f"Пара {first_pare}, {second_pare}")
    pair={first_pare: second_pare}
    name_pair = first_pare+second_pare
    rate_data = data[0][0]
    name = data[0][1]

    if pair in pair_variant:
        for elem in rate_data:
            if elem[0]==name_pair:
                return "<h1>coin = {}; currency = {}; Currently rate = {}<br>{} {}".format(first_pare, second_pare, elem[1],name[0],name[1])

    else:
        return "<h1>Wrong pare"




if __name__ == '__main__':
    app.run(debug=True)




