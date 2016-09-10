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
    # team1526_outlinks_dict=load_dict('team1526_outlinks_dict.cpkl')
    # url_to_id_dict_team1526= load_dict('url_to_id_dict_team1526.cpkl')
    # id_to_url_dict_team1526=load_dict('id_to_url_dict_team1526.cpkl')
    team1526_inlinks_dict=load_dict('team1526_inlinks_dict.cpkl')
    debugbreakpoint=1

