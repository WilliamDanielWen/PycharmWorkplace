import os
import cPickle
def dump_dict(dict_name,dict):
    print "dumping ",dict_name," ..."

    output_path = dict_name
    if os.path.exists(output_path):
        os.remove(output_path)
    out_file = open(output_path, 'wb')

    cPickle.dump(dict, out_file, protocol=cPickle.HIGHEST_PROTOCOL)

    out_file.close()

    print "dumping ", dict_name, " finished ..."



from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import time
import sys

def get_team_outlinks_info():

    es_client = Elasticsearch()
    start_time=time.time()
    count=0

    global_id=0
    url_to_id_dict=dict()
    id_to_url_dict=dict()

    team_outlinks_dict=dict()
    for rel in scan(es_client, index="team_1526", doc_type="document", query={"query": {"match_all": {}}}):
        stored_url=rel['_source']['url']
        outlinks=rel['_source']['out_links']

        # get a new id for stored_url
        if not url_to_id_dict.has_key(stored_url):
            global_id += 1
            stored_url_id = global_id
            url_to_id_dict[stored_url] = stored_url_id
            id_to_url_dict[stored_url_id] = stored_url
        else:
            stored_url_id = url_to_id_dict[stored_url]


        team_outlinks_dict[stored_url_id] = []

        for outlink in outlinks:
            # get a new id for a outlink
            if not url_to_id_dict.has_key(outlink):
                global_id += 1
                outlink_id=global_id
                url_to_id_dict[outlink] = outlink_id
                id_to_url_dict[outlink_id] = outlink
            else:
                outlink_id=url_to_id_dict[outlink]

            #write into the team_outlinks_dict
            team_outlinks_dict[stored_url_id].append(outlink_id)


        count+=1
        time_used= time.time()-start_time
        print count, "stored_url processed in ", time_used, " seconds"




    print "getting outlinks finished ...."
    dump_dict("url_to_id_dict_team1526.cpkl", url_to_id_dict)
    dump_dict("id_to_url_dict_team1526.cpkl", id_to_url_dict)
    dump_dict("team1526_outlinks_dict.cpkl",team_outlinks_dict)





if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    get_team_outlinks_info()
