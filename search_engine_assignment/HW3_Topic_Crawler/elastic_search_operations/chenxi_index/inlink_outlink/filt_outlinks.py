import cPickle
import time
import os
def load_dict(dictname):
 print " Loading ",dictname, " ..."
 file_path = dictname
 file_open = open(file_path, 'rb')
 dict=cPickle.load(file_open)
 file_open.close()
 print " Loading ", dictname, "finished ! "
 return dict

def filt_outlinks():
    chenxi_original_outlinks_dict=load_dict('chenxi_original_outlinks_dict.cpkl')
    id_to_url_dict_old=load_dict('id_to_url_dict_chenxi.cpkl')


    chenxi_outlinks_new = dict()

    #iteration 1: establish keys which stored in elastic search
    count=0
    start_time=time.time()
    for old_url_id in chenxi_original_outlinks_dict:
        stored_url=id_to_url_dict_old[old_url_id]
        chenxi_outlinks_new[stored_url]=[]
        count += 1
        print count, "stored url established in new dict in ", time.time()-start_time, " seconds"

    #iteration 2,update content for each key. if outlink is not one of the key, remove it
    count = 0
    start_time = time.time()
    for old_url_id in chenxi_original_outlinks_dict:
        stored_url=id_to_url_dict_old[old_url_id]
        old_outlink_ids=list(set(chenxi_original_outlinks_dict[old_url_id]))

        for old_outlinks_id in old_outlink_ids:
            outlink=id_to_url_dict_old[old_outlinks_id]
            if chenxi_outlinks_new.has_key(outlink):
               chenxi_outlinks_new[stored_url].append(outlink)

        count+=1
        print count, "stored url updated in new dict in ", time.time() - start_time, " seconds"

    return chenxi_outlinks_new

def dump_dict(dict_name,dict):
    print "dumping ",dict_name," ..."

    output_path = dict_name
    if os.path.exists(output_path):
        os.remove(output_path)
    out_file = open(output_path, 'wb')

    cPickle.dump(dict, out_file, protocol=cPickle.HIGHEST_PROTOCOL)

    out_file.close()

    print "dumping ", dict_name, " finished ..."


if __name__=="__main__":
    chenxi_outlinks_new=filt_outlinks()
    dump_dict('chenxi_outlinks_new.cpkl',chenxi_outlinks_new)
