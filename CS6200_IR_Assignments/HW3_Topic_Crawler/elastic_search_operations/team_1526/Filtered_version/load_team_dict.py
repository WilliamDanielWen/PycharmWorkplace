import cPickle
def load_dict(dictname):
 print " Loading ",dictname, " ..."
 file_path = dictname
 file_open = open(file_path, 'rb')
 dict=cPickle.load(file_open)
 file_open.close()
 print " Loading ", dictname, "finished ! "
 return dict

if __name__=="__main__":

    team1526_outlinks_new=load_dict('team1526_outlinks_new.cpkl')
    team1526_inlinks_new = load_dict('team1526_inlinks_new.cpkl')
    debugbreakpoint=1

