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
    team1526_outlinks_dict_old=load_dict('team1526_outlinks_dict.cpkl')
    id_to_url_dict_old=load_dict('id_to_url_dict_team1526.cpkl')


    team1526_outlinks_new = dict()

    #iteration 1: establish keys which stored in elastic search
    count=0
    start_time=time.time()
    for old_url_id in team1526_outlinks_dict_old:
        stored_url=id_to_url_dict_old[old_url_id]
        team1526_outlinks_new[stored_url]=[]
        count += 1
        print count, "stored url established in new dict in ", time.time()-start_time, " seconds"

    #iteration 2,update content for each key. if outlink is not one of the key, remove it
    count = 0
    start_time = time.time()
    for old_url_id in team1526_outlinks_dict_old:
        stored_url=id_to_url_dict_old[old_url_id]
        old_outlink_ids=list(set(team1526_outlinks_dict_old[old_url_id]))

        for old_outlinks_id in old_outlink_ids:
            outlink=id_to_url_dict_old[old_outlinks_id]
            if team1526_outlinks_new.has_key(outlink):
               team1526_outlinks_new[stored_url].append(outlink)

        count+=1
        print count, "stored url updated in new dict in ", time.time() - start_time, " seconds"

    return team1526_outlinks_new

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
    team1526_outlinks_new=filt_outlinks()
    dump_dict('team1526_outlinks_new.cpkl',team1526_outlinks_new)
