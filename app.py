from flask_socketio import SocketIO
from flask import Flask, render_template
from functools import partial, wraps
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)

socketio = SocketIO(app)

delay = 3


def emit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        """ Decorator that emits result of wrapped function over websocket.
        """
        result = f(*args, **kwargs)
        socketio.emit(
            'new_result', {
                'result': result
            }, namespace='/app'
        )
        return result
    return wrapper


def run_until_stopped(f):
    thread_stop_event = Event()

    @wraps(f)
    def wrapper(*args, **kwargs):
        """ Decorator that runs code in thread until stop event.
        """
        while not thread_stop_event.isSet():
            sleep(delay)
            f(*args, **kwargs)
    return wrapper


@run_until_stopped
@emit
def random_number(max_num, round_to_places):
    return round(random() * max_num, round_to_places)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/app')
def app_connect():
    print('Client connected')

    thread = Thread(target=partial(random_number, 10, 3))

    if not thread.isAlive():
        print('Starting Thread')
        thread.start()


@socketio.on('disconnect', namespace='/app')
def app_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
