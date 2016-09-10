import cPickle
def load_outlink_dict():
 print " Loading outlink dict ..."
 file_path = 'chenxi_outlinks_new.cpkl'
 file_open = open(file_path, 'rb')
 outlink_dict=cPickle.load(file_open)
 file_open.close()
 return outlink_dict


def reverse_outlink_into_inlink(outlink_dict):
    print"reversing outlink into inlink... "
    inlink_dict=dict()

    for stored_url in outlink_dict:
        inlink_dict[stored_url]=[]

    for stored_url in outlink_dict:
        outlinks = list(set(outlink_dict[stored_url]))
        for outlink in outlinks:
            inlink_dict[outlink].append(stored_url)




    print " Reverse finished "
    return inlink_dict

import os
def dump_inlink_dict(inlink_dict):
        print 'dumping inlink dict ...'
        output_path = 'chenxi_inlinks_new.cpkl'
        if os.path.exists(output_path):
            os.remove(output_path)
        out_file = open(output_path, 'wb')

        cPickle.dump(inlink_dict, out_file, protocol=cPickle.HIGHEST_PROTOCOL)

        out_file.close()



if __name__ == '__main__':
    outlink_dict=load_outlink_dict()
    inlink_dict=reverse_outlink_into_inlink(outlink_dict)
    dump_inlink_dict(inlink_dict)

