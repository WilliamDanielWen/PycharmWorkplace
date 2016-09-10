import cPickle
def load_outlink_dict():

 print " Loading outlink dict ..."
 file_path = '../runtime_cache/outlink_dict.cpkl'
 file_open = open(file_path, 'rb')
 outlink_dict=cPickle.load(file_open)
 file_open.close()

 return outlink_dict




def reverse_outlink_into_inlink(outlink_dict):
    print"reversing outlink into inlink... "
    inlink_dict=dict()
    count=0
    for stored_url in outlink_dict:
        outlinks=outlink_dict[stored_url]

        for outlink in outlinks:
            if  inlink_dict.has_key(outlink):
                inlink_dict[outlink].append(stored_url)
            else:
                inlink_dict[outlink]=[]
                inlink_dict[outlink].append(stored_url)

        count +=1
        if count%5000==0:
            print count, " stored urls processed ..."

    print count, " stored urls processed ..."
    print " Reverse finished "

    return inlink_dict

import os
def dump_inlink_dict(inlink_dict):
        print 'dumping inlink dict...'
        output_path = '../runtime_cache/inlink_dict.cpkl'
        if os.path.exists(output_path):
            os.remove(output_path)
        out_file = open(output_path, 'wb')

        cPickle.dump(inlink_dict, out_file, protocol=cPickle.HIGHEST_PROTOCOL)

        out_file.close()


#for test
def load_inlink_dict():

 print " Loading inlink dict ..."
 file_path = '../runtime_cache/inlink_dict.cpkl'
 file_open = open(file_path, 'rb')
 inlink_dict=cPickle.load(file_open)
 file_open.close()

 return inlink_dict

if __name__ == '__main__':
    outlink_dict=load_outlink_dict()
    inlink_dict=reverse_outlink_into_inlink(outlink_dict)
    dump_inlink_dict(inlink_dict)

