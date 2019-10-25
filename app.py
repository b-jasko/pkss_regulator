from flask import Flask
from math import exp

app = Flask(__name__)

T_o = 10
T_zco = 0
e_n_1 = 0
Um_n_1 = 0

SUMA = []


def regulation():
    global SUMA
    global e_n_1
    global T_zco
    global T_o
    global Um_n_1

    Kp = 1
    Ki = 10
    Kd = 0

    SP = 55 - 1.75 * T_o
    e = SP - T_zco
    SUMA.append(e)
    if len(SUMA) > 10:
        SUMA.pop(0)

    Um = Kp * e + Ki * sum(SUMA) + Kd * (e - e_n_1)
    e_n_1 = e
    T_zco = (Um - Um_n_1) *(1 - exp(-1/100))
    Um_n_1 = Um

    return 'Um = %.2f, <br/> e = %.2f <br/>T_zco = %.2f' % (Um, e, T_zco)


@app.route('/')
def index():
    return regulation()

if __name__ == '__main__':
    app.run()
