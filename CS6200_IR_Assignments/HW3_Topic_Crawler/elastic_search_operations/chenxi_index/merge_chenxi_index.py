from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import time
import sys
class Combiner:
    def __init__(self):

        self.read_es = Elasticsearch(["http://104.196.4.140:9200"])
        self.write_es = Elasticsearch()
        self.read_index = "maritimeaccidents"
        self.write_index = "team_1526"

    def merge(self):

        count = 0
        time_start = time.time()
        for rel in scan(self.read_es, index=self.read_index, doc_type="document", query={"query": {"match_all": {}}}):


            old_rec = rel['_source']
            new_index_rel = self.write_es.search(index=self.write_index,
                                                 doc_type='document',
                                                 body={
                                                     "query": {
                                                         "match": {
                                                             "_id":rel['_id']
                                                         }
                                                     }
                                                 },
                                                 request_timeout=100)

            if len(new_index_rel['hits']['hits'])==1:

                new_rec = new_index_rel['hits']['hits'][0]['_source']
                self.write_es.update(index=self.write_index, doc_type="document", id=new_index_rel['hits']['hits'][0]['_id'],
                              body={"doc":
                                    {
                                    "in_links": list(set(old_rec['in_links']+new_rec['in_links'])),
                                    "out_links": list(set(old_rec['out_links']+new_rec['out_links'])),
                                    "author": old_rec['author'] +' , '+ new_rec['author']}
                              },

                              request_timeout=100)
            else:
                self.write_es.index(index=self.write_index, doc_type="document", id=rel['_id'],
                              body={"docno": old_rec['url'],
                                    "HTTPheader": old_rec['HTTPheader'],
                                    "title": old_rec['title'],
                                     "text": old_rec['text'],
                                     "html_Source": old_rec['html_Source'],
                                    "in_links": old_rec['in_links'],
                                    "out_links": old_rec['out_links'],
                                    "author": old_rec['author'],
                                    "depth": old_rec['depth'],
                                    "url": old_rec['url'],},
                              request_timeout=100)
            count += 1
            time_used = time.time() - time_start
            print('{} pages stored in {} seconds  {}'.format(count, time_used, rel['_id']))
import sys
if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    c = Combiner()
    c.merge()