import string
from nltk.stem.snowball import SnowballStemmer
import cPickle
import os
import time
import math
from elasticsearch import Elasticsearch
############################ define helper functions #####################################
def load_doc_length_info():

 print(" Loading doc_length_dict ...")
 path_doc_length_dict = '../runtime_cache/DOCUMENT_LENGTH_DICT.cpkl'
 file_doc_length_dict = open(path_doc_length_dict, 'rb')
 doc_length_dict=cPickle.load(file_doc_length_dict)
 file_doc_length_dict.close()

 return doc_length_dict

def load_whole_doc_id_list():
    whole_doc_id_list = []
    doc_id_list_file = open("../runtime_cache/WHOLE_DOC_ID_LIST", "r")
    doc_id = doc_id_list_file.readline().strip()

    while not doc_id == '':
        whole_doc_id_list.append(doc_id)
        doc_id = doc_id_list_file.readline().strip()

    return whole_doc_id_list

def get_non_empty_doc_id_list(whole_lst,length_dict):
    non_empty_lst=[]
    empty_lst=[]
    for id in whole_lst:
        if length_dict[id]==0:
            empty_lst.append(id)
        else:
            non_empty_lst.append(id)

    return non_empty_lst,empty_lst

def get_total_document_length(doc_length_dict, doc_id_list):
    sum=0
    for doc_id in doc_id_list:
        doc_length=doc_length_dict[doc_id]
        sum +=doc_length
    return sum

def get_stop_word():
    file = open('../../Data/stoplist.txt', 'rb')
    stop_words = set()
    word = ''
    while True:
        word = file.readline().strip()
        if word == '':
            break
        stop_words.add(word)
    file.close()
    return stop_words

# read query from file and preprocess them
def get_valid_queries():

    #step1 read query strings from file and preprocess them
    queries_strings = dict()
    path = "../../Data/query_desc.51-100.short.txt"
    query_file = open(path, 'r')
    query_string = query_file.readline().strip()
    while not query_string == '':
        # if a line is read, preprocess it

        #seperate query id and query string
        query_no=string.split(query_string,". ")[0]
        query_string = string.split(query_string, ". ")[1]

        # to lower case
        query_string = string.lower(query_string)

        #strip the number, dot, and white space
        query_string=string.strip(query_string,". ()")

        #remove the punctuation
        query_string=string.replace(query_string,",","")
        query_string=string.replace(query_string,"(","")
        query_string=string.replace(query_string,")","")
        query_string=string.replace(query_string,"'","")

        #split the dash word
        query_string=string.replace(query_string,"-"," ")


        queries_strings[query_no]=query_string

        #read the next query string
        query_string = query_file.readline().strip()


    # step2 remove stop word and stemming
    stemmer = SnowballStemmer('english')
    STOP_WORDS=get_stop_word()
    REMOVE_WORDS = ['document', 'must', 'will', 'report', 'type'
                        , 'move', 'event', 'ongo', 'method', 'actual'
                        ,'predict', 'include', 'identify', 'describe'
                        , 'discuss','cite']

    valid_queries=dict()
    for query_no in queries_strings:
        query_string=queries_strings[query_no]
        #split the query into array
        terms=query_string.split()
        valid_terms=[]
        for term in terms:
            #remove stop word and no
            if term in STOP_WORDS or term in REMOVE_WORDS:
                continue


            #stem each word
            term = str(stemmer.stem(term))
            valid_terms.append(term)

        #insert the valid query term array
        valid_queries[query_no] = valid_terms

    return valid_queries

def search_term(term):
    es = Elasticsearch()
    result = es.search(
        index='ap_dataset',
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
            },
            "size": 10000,
            "fields": ["stream_id"]
        }

    )



    return result

def get_unique_term_num():
    es=Elasticsearch()
    response=es.search(
        index='ap_dataset',
        doc_type='document',
        body={
            "aggs" : {
                "unique_terms" : {
                    "cardinality" : {
                        "field" : "text"
                    }
                }
            }
        }
    )
    result=response['aggregations']['unique_terms']['value']
    return result

def get_term_statistics(term):
    es = Elasticsearch()
    result = es.search(
        index='ap_dataset',
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
            },
            "size": 10000,
            "fields": ["stream_id"]
        }

    )

    hits = result["hits"]["hits"]
    term_inverted_file = dict()
    ttf = 0

    if not len(hits) == 0:
        for hit in hits:
            doc_id = hit["_id"]
            tf = hit["_score"]
            term_inverted_file[doc_id] = tf
            ttf += tf

    return term_inverted_file, ttf

def get_tf(term,doc_id):
    term_inverted_file,ttf=get_term_statistics(term)

    if term_inverted_file.has_key(doc_id):
         return term_inverted_file[doc_id]
    else:
        return 0

############################### define models #####################################
def Okapi_TF(query):

    score_list = dict()

    for term in query:
        result = search_term(term)
        hits = result["hits"]["hits"]

        #the term is not found in corpus
        if len(hits)==0:
            continue

        for hit in hits:
            doc_id = hit["_id"]
            tf = hit["_score"]
            if score_list.has_key(doc_id):
                score_list[doc_id] += (tf * 1.0) / (tf + 0.5 + (1.5 * DOC_LENGTH_DICT[doc_id] / AVG_DOC_LENGTH))
            else:
                score_list[doc_id] = (tf * 1.0) / (tf + 0.5 + (1.5 * DOC_LENGTH_DICT[doc_id] / AVG_DOC_LENGTH))




    return score_list

def TF_IDF(query):
    score_list = dict()
    # total number of Documents

    for term in query:
        result = search_term(term)
        hits = result["hits"]["hits"]

        # the term is not found in corpus
        if len(hits) == 0:
            continue

        df=len(hits)
        for hit in hits:
            doc_id = hit["_id"]
            tf = hit["_score"]
            okapi_tf = (tf * 1.0) / (tf + 0.5 + (1.5 * DOC_LENGTH_DICT[doc_id] / AVG_DOC_LENGTH))
            idf=math.log(D * 1.0 /df, 2)
            term_score=okapi_tf*idf
            if score_list.has_key(doc_id):
                score_list[doc_id] += term_score
            else:
                score_list[doc_id] = term_score

    return score_list

def Okapi_BM25(query):
    k1=2
    k2=500
    b=0

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
        for hit in hits:
            doc_id = hit["_id"]
            tf = hit["_score"]

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

def Unigram_LM_Laplace_Smoothing(query):
    score_list = dict()


    for term in query:
        term_inverted_file,ttf = get_term_statistics(term)

        if ttf==0:
            continue# if the corpus didn't contain the term, continue to next term

        for doc_id in NON_EMPTY_ID_LIST:

            tf=0#default is zero
            if term_inverted_file.has_key(doc_id):
                tf=term_inverted_file[doc_id]

            term_score = math.log((tf + 1) * 1.0 / (DOC_LENGTH_DICT[doc_id] + V), 2)

            if score_list.has_key(doc_id):
                score_list[doc_id] += term_score
            else:
                score_list[doc_id] = term_score

    return score_list

def Unigram_LM_Jelinek_Mercer_Smoothing(query):
    score_list = dict()
    para_lambda=0.6
    total_doc_length=AVG_DOC_LENGTH*len(DOC_LENGTH_DICT)
    #get score
    for term in query:

        term_inverted_file, ttf=get_term_statistics(term)
        if  ttf==0:
            continue
            # if the corpus didn't contain the term, continue to next term

        for doc_id in NON_EMPTY_ID_LIST:
            # get tf in doc (default is zero)
            tf = 0
            if term_inverted_file.has_key(doc_id):
                tf = term_inverted_file[doc_id]

            foreground_prob=para_lambda*tf/DOC_LENGTH_DICT[doc_id]
            background_prob = (1 - para_lambda)*ttf/total_doc_length
            base=2
            term_score = math.log( (foreground_prob + background_prob)  , base)

            if score_list.has_key(doc_id):
                score_list[doc_id] += term_score
            else:
                score_list[doc_id] = term_score

    return score_list

###################### start setp3:calling models to perform queries ############################
def process_valid_query_set(retrieval_model, num_top_docs, path_model_output, valid_query_set):
    print "  Model chosen: ", retrieval_model.func_name
    if os.path.exists(path_model_output):
        os.remove(path_model_output)
    output_file = open(path_model_output, 'w')

    query_count=0
    for query_no in valid_query_set:
        start_time=time.time()
        query = valid_query_set[query_no]

        # calculate the score list according to retrieval model and store it
        score_list = retrieval_model(query)

        # output the top results
        rank = 1
        for doc_id in sorted(score_list, key=score_list.get, reverse=True):
            result = str(query_no) + ' Q0 ' + doc_id + ' ' + str(rank) + ' ' + str(score_list[doc_id]) + ' Exp' + '\n'
            output_file.write(result)
            rank += 1
            if rank > 1000:
                break

        end_time=time.time()
        query_count +=1
        print "  ",query_count," query processed, time usage of query[", query_no ,"] : ", end_time-start_time, " seconds"

############## step3.1  load query info data


s_time=time.time()
print "Start loading data ..."
DOC_LENGTH_DICT= load_doc_length_info()
valid_query_set= get_valid_queries()


WHOLE_DOC_ID_LIST= load_whole_doc_id_list()
NON_EMPTY_ID_LIST ,EMPTY_ID_LIST= get_non_empty_doc_id_list(WHOLE_DOC_ID_LIST,DOC_LENGTH_DICT)
#total number of docs
D = len(NON_EMPTY_ID_LIST)
TOTAL_DOC_LENGTH=get_total_document_length(DOC_LENGTH_DICT, NON_EMPTY_ID_LIST)
AVG_DOC_LENGTH = TOTAL_DOC_LENGTH/D

# number of unique terms
V=get_unique_term_num()#178081

e_time=time.time()
print "Time usage of loading data : ", e_time-s_time,"seconds"


############### step3.2 assign the retrieval model
NUM_TOP_DOCS=1000

#RETRIEVAL_MODEL=Okapi_TF
#PATH_MODEL_OUTPUT= "../output/Okapi_TF.txt"

#RETRIEVAL_MODEL=TF_IDF
#PATH_MODEL_OUTPUT= "../output/TF_IDF.txt"

#RETRIEVAL_MODEL=Okapi_BM25
#PATH_MODEL_OUTPUT= "../output/Okapi_BM25.txt"

#RETRIEVAL_MODEL=Unigram_LM_Laplace_Smoothing
#PATH_MODEL_OUTPUT= "../output/Unigram_LM_Laplace_Smoothing.txt"

retrieval_model=Unigram_LM_Jelinek_Mercer_Smoothing
model_output_path= "../output/Unigram_LM_Jelinek_Mercer_Smoothing.txt"


################### step3.3 execute the query set
t1=time.time()
print "Start process of all queries ..."
process_valid_query_set(retrieval_model, NUM_TOP_DOCS, model_output_path, valid_query_set)
t2=time.time()
print "Time usage of execution of all queries is : ", (t2-t1), " seconds"




##########test index
# print get_tf("cat","AP890302-0045") #18
# print get_tf("cat","AP890427-0023") #24
# print get_tf("corrupt","AP890704-0150") #12
# print get_tf("corrupt","AP890223-0032") #8




