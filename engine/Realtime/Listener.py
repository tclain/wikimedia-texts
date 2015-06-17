__author__ = 'tclain'

import socketIO_client
import threading

class ListenerNamespace(socketIO_client.BaseNamespace) :
    delegate = None
    ## delegate callback is called when data arrived
    def on_change(self, change):
        ListenerNamespace.delegate.onChange(change)

    #handle connection to the service
    def on_connect(self):
        self.emit("subscribe", "commons.wikimedia.org")

class ListenerWorker(threading.Thread):
    ### holders for the socket object
    def __init__(self, delegate):
        # configure socketIO
        self.socketio = socketIO_client.SocketIO("stream.wikimedia.org",80)
        ListenerNamespace.delegate = self
        self.socketio.define(ListenerNamespace, "/rc")
        #setup levelup delegate
        self.delegate = delegate
        # constructor of super class
        threading.Thread.__init__(self)

    def onChange(self, change):
        self.delegate.onChange(change)
    def run(self):
        self.socketio.wait()

if __name__ == "__main__" :
    worker = ListenerWorker()
    worker.start()