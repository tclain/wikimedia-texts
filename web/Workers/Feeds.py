
import threading
import time

class WikimediaThread(threading.Thread):
    ### holders for the socket object
    socketio = None
    def __init__(self, socketio):
        self.socketio = socketio
        threading.Thread.__init__(self)

    def run(self):
        count = 0
        while True :
            time.sleep(1)
            self.socketio.emit('server.data.new',
                      {'lang': "fr", 'count': count},
                      namespace='/wiki')
            print count
            count+=1
