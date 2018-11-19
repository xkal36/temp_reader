from flask_socketio import SocketIO
from flask import Flask, render_template
from functools import wraps
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)

socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()

delay = 3


def random_number():
    return round(random() * 10, 3)


class ThreadWorker(Thread):
    def __init__(self, f):
        self.func_to_call = f
        self.delay = delay
        super(ThreadWorker, self).__init__()

    def emitter(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            while not thread_stop_event.isSet():
                result = f(self, *args, **kwargs)
                socketio.emit(
                    'new_result', {'result': result}, namespace='/app'
                )
                sleep(self.delay)
        return wrapper

    @emitter
    def run(self, *args, **kwargs):
        return self.func_to_call(*args, **kwargs)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/app')
def app_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print('Starting Thread')
        thread = ThreadWorker(random_number)
        thread.start()


@socketio.on('disconnect', namespace='/app')
def app_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
