def get_total_document_length(doc_length_dict):
    sum=0
    for doc_id in doc_length_dict:
        doc_length=doc_length_dict[doc_id]
        sum +=doc_length
    return sum


import cPickle
def load_dict(dictname):
 print " Loading ",dictname, " ..."
 file_path = dictname
 file_open = open(file_path, 'rb')
 dict=cPickle.load(file_open)
 file_open.close()
 print " Loading ", dictname, "finished ! "
 return dict

def dump_dict(dict_name,dict):
    print "dumping ",dict_name," ..."

    output_path = dict_name
    if os.path.exists(output_path):
        os.remove(output_path)
    out_file = open(output_path, 'wb')

    cPickle.dump(dict, out_file, protocol=cPickle.HIGHEST_PROTOCOL)

    out_file.close()

    print "dumping ", dict_name, " finished ..."

from elasticsearch.helpers import scan
import time
def get_doc_length_dict():
    print " Getting information of document length ..."

    DOCUMENT_LENGTH_DICT = dict()  # sturcture: {doc id:  doc length}

    es_client=Elasticsearch()
    count=0
    start_time = time.time()
    for rel in scan(es_client, index='team_1526', doc_type="document", query={"query": {"match_all": {}}}):

        doc_id=rel['_id']
        #get termvecotr of document with doc_id
        document = es_client.termvectors(
            index='team_1526',
            doc_type='document',
            id=doc_id,
            fields=['text'],
            body={
                "offsets": False,
                "payloads": False,
                "positions": False,
                "field_statistics": False,
                "term_statistics": True
            }
        )
        #store the term frequency, doc frequency,
        if not len(document['term_vectors']) == 0:
            terms_of_doc = document['term_vectors']['text']['terms']
            words_num_of_doc = 0
            for term in terms_of_doc:
                term_frequency_in_doc = terms_of_doc[term]['term_freq']
                words_num_of_doc += term_frequency_in_doc
            # doc length is sum of term frequency of all terms in this doc
            DOCUMENT_LENGTH_DICT[doc_id] = words_num_of_doc

        else:
            # for empty doc ignore all information,set doc length as zero
            DOCUMENT_LENGTH_DICT[doc_id]=0
            continue
        count +=1
        if(count%50==0):

            print count,' documents has been processed in ',time.time()-start_time,' seconds...'


    print "Getting information of document length finished !"

    return DOCUMENT_LENGTH_DICT

import os
def dump_doc_length_dict(doc_length_dict):
    path_doc_length_dict = 'DOCUMENT_LENGTH_DICT.cpkl'
    if os.path.exists(path_doc_length_dict):
        os.remove(path_doc_length_dict)
    file_doc_length_dict = open(path_doc_length_dict, 'wb')
    cPickle.dump(doc_length_dict, file_doc_length_dict, protocol=cPickle.HIGHEST_PROTOCOL)
    file_doc_length_dict.close()


from collections import OrderedDict
def resize_root_set():
    root1000dict=load_dict("root_set1000.cpkl")
    count=0
    new_root_set=OrderedDict()
    for url in root1000dict:
        new_root_set[url]=root1000dict[url]
        count+=1
        if count>=200:
            break

    dump_dict("root_set.cpkl",new_root_set)


from elasticsearch import Elasticsearch
def search_term(term):
    start_time=time.time()
    print ""
    print "searching term \"",term,"\" ..."
    es = Elasticsearch()
    result = es.search(
        index='team_1526',
        doc_type='document',
        body={
            "query": {
                "function_score": {
                    "query": {
                            "match": {
                                "text": term
                            }
                    },
                    "functions": [
                        {
                            "script_score": {
                                "script_id": "getTF",
                                "lang" : "groovy",
                                "params": {
                                    "term": term,
                                    "field": "text"

                                }
                            }
                        }
                    ],
                    "boost_mode": "replace"
                }
            }
            ,"size": 10000
            , "fields": ["stream_id"]
        },
        request_timeout=500

    )
    end_time=time.time()
    print "finished searching term \"", term, "\" in ",end_time-start_time," seconds."

    return result

def inlink_team1526_info():
    inlink_dict=load_dict("team1526_inlinks_new.cpkl")
    max=0
    sum=0
    for url in inlink_dict:
        if len(inlink_dict[url])>max:
            max= len(inlink_dict[url])

        sum+=len(inlink_dict[url])

    avg=sum*1.0/len(inlink_dict)
    print "team_1526 inlink dict info:"
    print "avg num inlinks per url:",avg,"max num inlinks per url:",max

def outlink_team1526_info():
    outlink_dict=load_dict("team1526_outlinks_new.cpkl")
    max=0
    sum=0
    for url in outlink_dict:
        if len(outlink_dict[url])>max:
            max= len(outlink_dict[url])

        sum+=len(outlink_dict[url])
    avg=sum*1.0/len(outlink_dict)
    print "team_1526 outlink dict info:"
    print "avg num outlinks per url:",avg,"max num outlinks per url:",max

import math
def Okapi_BM25(query,DOC_LENGTH_DICT,AVG_DOC_LENGTH):
    print 'Start to search query for each term: '
    print 'query length: ',len(query)
    print 'stemmed query: ',query
    k1=2
    k2=500
    b=0
    D=len(DOC_LENGTH_DICT)
    #get term query frequecy dict
    QUERY_TF_DICT=dict()
    for term in query:
        if QUERY_TF_DICT.has_key(term):
            QUERY_TF_DICT[term] +=1
        else:
            QUERY_TF_DICT[term]=1

    #get the score
    score_list = dict()
    for term in query:
        result = search_term(term)
        hits = result["hits"]["hits"]

        # the term is not found in corpus
        if len(hits) == 0:
            continue

        df = len(hits)

        print "term: ", term, " df: ",df
        tf_print_count=0

        for hit in hits:
            doc_id = hit["_id"]
            tf = hit["_score"]
            if tf_print_count<=100:
                tf_print_count += 1
                print "No.",tf_print_count," tf: ",tf," url:",doc_id



            #get tf_wq
            tf_wq=QUERY_TF_DICT[term]

            #get left part
            base=2
            left_part=math.log((D * 1.0 + 0.5) / (df + 0.5) ,base)

            # get middle part
            middle_part=(tf +  k1*tf )*1.0 / (tf + k1*((1-b) + b*(DOC_LENGTH_DICT[doc_id] / AVG_DOC_LENGTH)))

            # get right part
            right_part=(tf_wq + k2*tf_wq)*1.0 / (tf_wq + k2)

            #get the term score
            term_score = left_part*middle_part*right_part
            if score_list.has_key(doc_id):
                score_list[doc_id] += term_score
            else:
                score_list[doc_id] = term_score

    return score_list


def stemming_preprocess(terms,stemmer):

    #Stem
    results = []
    for term in terms:
        term = stemmer.stem(term)
        term =str(term)
        results.append(term)
    return results

def rootset_info():
    print "root set info: "

    root_set = load_dict("root_set.cpkl")
    print " root set length: ", len(root_set)
    num=1
    for url in root_set:
        print "No.",num,", Score: ",root_set[url], ", Url: ",url
        num += 1

def normalize_vector(vector):
    sqaure_sum=0
    for component in vector:
        value=vector[component]
        sqaure_sum+=value*1.0*value

    vector_length=math.sqrt(sqaure_sum)

    for component in vector:
        vector[component]=vector[component]/vector_length

    return vector


def get_L1_error(vector1, vector2):
    l1_error=0
    for component in vector1:
        l1_error +=abs(vector1[component] - vector2[component])
    return l1_error


def output_top_scored_url(file_name, vector, top_num):
    print 'output ',file_name,' to file'
    if os.path.exists(file_name):
        os.remove(file_name)
    file = open(file_name, 'w')
    count=0
    for url in sorted(vector, key=vector.get, reverse=True):
        file.write('score: '+ str(vector[url]) + "  url: "+str(url) + '\n')
        count +=1
        if count>=top_num:
            break

    file.close()

if __name__=="__main__":
    #doc_length_dict=get_doc_length_dict()
    #dump_doc_length_dict(doc_length_dict)
    #dict_test=load_dict("DOCUMENT_LENGTH_DICT.cpkl")

    #inlink_team1526_info()
    #outlink_team1526_info()
    resize_root_set()
    rootset_info()