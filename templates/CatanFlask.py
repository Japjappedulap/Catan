import threading
from flask import Flask
from Generator.main import classic

app = Flask(__name__)


@app.route('/catan/classic')
def classic_map():
    print(threading.active_count())
    return classic()


@app.route('/catan')
def catan_help():
    print(threading.active_count())
    return 'help here'


@app.route('/catan/extended')
def extended_map():
    print(threading.active_count())
    return 'Hello World! extended'


if __name__ == '__main__':
    app.run(port=80)
