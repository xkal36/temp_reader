from flask_socketio import SocketIO
from flask import Flask, render_template
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)

socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()


class RandomThread(Thread):
    def __init__(self):
        self.delay = 3
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        while not thread_stop_event.isSet():
            number = round(random() * 10, 3)
            print(number)
            socketio.emit('newnumber', {'number': number}, namespace='/app')
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/app')
def app_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print('Starting Thread')
        thread = RandomThread()
        thread.start()


@socketio.on('disconnect', namespace='/app')
def app_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
