import os
import cPickle
def dump_chenxi_outlink_dict(dict):

        print 'dumping partial chenxi outlink dict ...'
        output_path = "chenxi_outlink_dict.cpkl"
        if os.path.exists(output_path):
            os.remove(output_path)
        out_file = open(output_path, 'wb')

        cPickle.dump(dict, out_file, protocol=cPickle.HIGHEST_PROTOCOL)

        out_file.close()



from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import time
import sys

def get_chenxi_outlinks():

    reload(sys)
    sys.setdefaultencoding("utf-8")
    chenxi_client = Elasticsearch(["http://104.196.117.30:9200"])
    start_time=time.time()
    count=0

    chenxi_outlinks_dict=dict()
    for rel in scan(chenxi_client, index="maritimeaccidents", doc_type="document", query={"query": {"match_all": {}}}):
        stored_url=rel['_source']['url']
        outlinks=rel['_source']['out_links']
        chenxi_outlinks_dict[stored_url]=list(outlinks)
        count+=1

        time_used= time.time()-start_time
        print count, "stored_url processed in ", time_used, " seconds"

    dump_chenxi_outlink_dict(chenxi_outlinks_dict)
    print "getting outlinks finished ...."







if __name__=="__main__":
    get_chenxi_outlinks()