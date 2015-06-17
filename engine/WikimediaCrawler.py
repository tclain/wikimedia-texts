#-*- coding=utf-8-*-


from Realtime.Listener import ListenerWorker
from Datastore.Indexer import Indexer
import json

import threading
class WikimediaData(threading.Thread) :

    def __init__(self, serversocket):
        self.listener = ListenerWorker(delegate = self)
        self.indexer = Indexer({"index": "wikiactivities", "doc_type":"wikiactivity"})
        self.serversocket = serversocket
        threading.Thread.__init__(self)
    ## callback call when new data is captured from WikimediaFeed by listener
    def onChange(self, change):
        self.indexer.index(change)
        if self.serversocket is not None :
            self.serversocket.emit('server.data.new',
                      {"comment" : change.get("comment", "new Activity")},
                      namespace='/wiki')
    def handleSearch(self, input):
        if self.serversocket is not None :
            result = self.indexer.search(input)
            print result
            self.serversocket.emit('server.search.result',result,namespace='/wiki')
    def run(self):
        self.listener.start()



if __name__ == "__main__" :
    wiki = WikimediaData()
    wiki.start()