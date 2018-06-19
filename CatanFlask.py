import threading
from flask import Flask, redirect
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
    return app.send_static_file('index.html')


@app.route('/catan/extended')
def extended_map():
    print(threading.active_count())
    return extended()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect('/catan')


if __name__ == '__main__':
    app.run(threaded=True)
