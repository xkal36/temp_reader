from flask_socketio import SocketIO
from flask import Flask, render_template
from functools import wraps
from time import sleep
from threading import Thread, Event
from temp_reader import read_temp
import random
import sys

app = Flask(__name__)

socketio = SocketIO(app)

delay = int(sys.argv[1])


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
def random_number():
    return random.randint(1, 101)


@run_until_stopped
@emit
def get_temperature():
    return read_temp()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/app')
def app_connect():
    print('Client connected')

    thread = Thread(target=random_number)

    if not thread.isAlive():
        print('Starting Thread')
        thread.start()


@socketio.on('disconnect', namespace='/app')
def app_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
