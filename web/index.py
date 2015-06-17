from gevent import monkey
monkey.patch_all()

import sys
sys.path.append("..")
from flask import Flask, render_template, send_from_directory
from flask.ext.socketio import SocketIO, emit
from engine.WikimediaCrawler import *

#### CONFIG DATA
app = Flask(__name__)
app.debug = True
#SECRET
app.config['SECRET_KEY'] = 'lqfqfljbfqsmfknf!:fmqfmqnfdqugdskdhfkq'
socketio = SocketIO(app)
##
thread  = None

### STATIC ROUTE  ONLY
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = WikimediaData(socketio)
        thread.start()
    return render_template('index.html')

@socketio.on('client.new.connect', namespace='/wiki')
def client_new_connect():
    emit ('server.log', {'data' : 'new client'})

@socketio.on('connect', namespace='/wiki')
def test_connect():
    emit('server.log', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect', namespace='/wiki')
def test_disconnect():
    print('Client disconnected')

#handling message from client
@socketio.on('client.search.request', namespace='/wiki')
def handle_search(input):
    print("Searched requested"+input)
    thread.handleSearch(input)

if __name__ == '__main__':
    socketio.run(app)