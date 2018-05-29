import threading
from flask import Flask
from Generator.main import classic
from Generator.main import extended

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
    return extended()


if __name__ == '__main__':
    app.run(threaded=True)
