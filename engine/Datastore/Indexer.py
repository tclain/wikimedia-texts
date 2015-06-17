__author__ = 'tclain'

import elasticsearch

class Indexer :
    '''
    Index data in elasticSearch
    '''


    def __init__(self, connectionDetails = {}) :
        self.es = elasticsearch.Elasticsearch()
        self.index_name = connectionDetails.get("index","records")
        self.doc_type = connectionDetails.get("doc_type", "record")
    '''
    index a set of data in elasticsearch
    '''
    def index(self,data):
        self.es.index(index=self.index_name,doc_type=self.doc_type, body=data)
    def search(self, input):
        return self.es.search(
            index=self.index_name, body=
            {"query":
                 {"fuzzy_like_this_field" :
                      { "comment" :
                            {"like_text": input,
                             "max_query_terms":5
                             }
                        }
                  }
             })