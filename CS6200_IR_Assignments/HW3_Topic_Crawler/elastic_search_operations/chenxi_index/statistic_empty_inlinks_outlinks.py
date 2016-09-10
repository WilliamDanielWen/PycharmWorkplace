from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import time
import sys
class Statisticer:
    def __init__(self):
        self.read_es = Elasticsearch(["http://104.196.4.140:9200"])
        self.read_index = "maritimeaccidents"

    def find_inlink_outlink_statistics(self):



        empty_inlink_page_count=0
        empty_outlink_page_count = 0

        total_pages = 0
        total_inlinks = 0
        total_outlinks = 0
        time_start = time.time()
        for rel in scan(self.read_es, index=self.read_index, doc_type="document", query={"query": {"match_all": {}}}):

            old_rec = rel['_source']

            if len(old_rec['in_links'])==0:
               empty_inlink_page_count +=1
               print "empty inlink page: ", rel['_id']

            total_inlinks +=len(old_rec['in_links'])


            if len(old_rec['out_links'])==0:
                empty_outlink_page_count+=1
                print "empty outlink page: ", rel['_id']

            total_outlinks+=len(old_rec['out_links'])


            total_pages += 1

            avrage_inlinks_per_page =total_inlinks*1.0/total_pages
            average_outlinks_per_page=total_outlinks*1.0/total_pages

            time_used = time.time() - time_start


            print('{} pages queried in {} seconds'.format(total_pages, time_used))
            print "empty_inlink_page: ", empty_inlink_page_count
            print "avrage_inlinks_per_page: ", avrage_inlinks_per_page
            print "empty_outlink_page: ", empty_outlink_page_count
            print "average_outlinks_per_page",average_outlinks_per_page


            print(" ")
import sys
if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    c = Statisticer()
    c.find_inlink_outlink_statistics()