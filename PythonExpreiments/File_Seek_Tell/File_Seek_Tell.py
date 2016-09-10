#   [termid][docid][poslist]
cache=dict()


#term 666
cache[666]=dict()

cache[666][22]=dict()
cache[666][99999]=dict()
cache[666][3444]=dict()
cache[666][557]=dict()

cache[666][22]=[1, 2, 3, 4, 5, 6, 7]
cache[666][99999]=[1, 2, 3, 4, 5, 6, 7, 8]
cache[666][3444]=[1]
cache[666][557]=[1, 2, 3]


#term 333
cache[333]=dict()

cache[333][22]=dict()
cache[333][99999]=dict()
cache[333][3444]=dict()
cache[333][557]=dict()

cache[333][22]=[1, 2, 3, 4, 5, 6, 7]
cache[333][99999]=[1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15]
cache[333][3444]=[1]
cache[333][557]=[1, 2, 3]

#  termid,df,cf,docid tf pos1 pos2 pos3 ...posn,docid tf pos1 pos2 pos3 ... posn
def  dump_inverted_list_cache_to_HDD(inverted_list_cache, output_file):
    catalog=dict()
    for term_id in inverted_list_cache:
        output_str=""
        offset_start =output_file.tell()
        term_inverted_list = inverted_list_cache[term_id]
        df = len(term_inverted_list)
        cf = 0

        for doc_id in term_inverted_list:
            output_str += "," + str(doc_id)

            pos_list = term_inverted_list[doc_id]
            tf=len(pos_list)
            output_str += " " + str(tf)

            cf += tf

            for pos in pos_list:
                output_str += " " + str(pos)

        #add the information of term_id,
        output_str=str(term_id)+","+str(df)+","+str(cf)+output_str

        output_file.write(output_str)
        output_file.flush()
        offset_end =output_file.tell()
        offset_size=offset_end - offset_start

           #write into catalog
        catalog[term_id] = (offset_start,offset_size)


    output_file.close()
    return catalog



def  get_term_inverted_list_from_HDD(term_id, catalog, HDD_index_file):
     if  not catalog.has_key(term_id):
          return None

     term_inverted_list = dict()

     offset_start=catalog[term_id][0]
     size=catalog[term_id][1]
     HDD_index_file.seek(offset_start)
     term_info=HDD_index_file.read(size).split(",")

     term_id_read=term_info[0]
     df=term_info[1]
     cf=term_info[2]

     for i in range(3, len(term_info),1):
         doc_info=term_info[i]
         doc_info=doc_info.split(" ")
         doc_id=doc_info[0]
         tf=doc_info[1]
         term_inverted_list[doc_id]=dict()
         term_inverted_list[doc_id]["tf"]=tf
         term_inverted_list[doc_id]["pos_list"] = []
         for j in range (2, len(doc_info),1):
             term_inverted_list[doc_id]["pos_list"].append(doc_info[j])


     return  df,cf,term_inverted_list




output_file=open("index_file.txt", "wb")
catalog=dump_inverted_list_cache_to_HDD(cache, output_file)

index_file=open("index_file.txt", "rb")
# df,cf,dic666=get_term_inverted_list_from_HDD(666, catalog, index_file)
df, cf, dic333 = get_term_inverted_list_from_HDD(333, catalog, index_file)

breakpoint=1

