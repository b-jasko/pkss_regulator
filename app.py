from flask import Flask
from flask import request
import requests
import json

app = Flask(__name__)

T_o = 0
T_zco = 0
e_n_1 = 0
Um_n_1 = 0

SUMA = []
global time
time = "1999-01-29 04:05:06"

def regulation():
    global SUMA
    global e_n_1
    global T_zco
    global T_o
    global Um_n_1
    global Fzm
    global Um
    global time

    Kp = 0.1
    Ki = 1
    Kd = 0.1

    SP = 55 - 1.75 * T_o
    e = SP - T_zco
    SUMA.append(e)
    if len(SUMA) > 10:
        SUMA.pop(0)

    Um = Kp * e + Ki * sum(SUMA) + Kd * (e - e_n_1)
    if Um > 1:
        Um = 1
    elif Um < 0:
        Um = 0
    e_n_1 = e
    Um_n_1 = Um
    Fzm = 80*1000/3600*Um

    url_logger = "http://e4d48e57.ngrok.io"
    json_logger = {
        "U_m": Um,
        "F_zm": Fzm,
        "T_zcoref": SP,
        "timestamp": time
    }

    r = requests.post(url=url_logger + "/5", json = json_logger)
    print(r.content)

    return 'Um = %.2f, <br/> e = %.2f <br/>T_zco = %.2f <br/>T_o = %.2f <br/>SP = %.2f' % (Um, e, T_zco, T_o, SP)


@app.route('/to', methods=['PUT'])
def index():
    global T_o
    T_o_json = json.loads(request.data)
    print(T_o_json)
    T_o = float(T_o_json['T_o'])
    return "T_o received"

@app.route('/regulation', methods=['PUT'])
def index_1():
    global T_zco
    T_zco_json = json.loads(request.data)
    print(T_zco_json)
    T_zco = float(T_zco_json['Tzco'])
    print(regulation())
    return {"Fzm":Fzm,
            "Um":Um
            }

@app.route('/time', methods=['PUT'])
def index_2():
    global speed
    global time
    time_module_json = json.loads(request.data)
    speed = time_module_json['speed']
    time = time_module_json['symTime']
    print(time)
    return "module 5: timestamp received"

@app.route('/start', methods=['PUT'])
def index_3():
    global start_speed
    global start_time
    time_module_json = json.loads(request.data)
    start_speed = time_module_json['speed']
    start_time = time_module_json['startTime']
    print(start_time)
    return "module 5 started"



if __name__ == '__main__':
    app.run()
