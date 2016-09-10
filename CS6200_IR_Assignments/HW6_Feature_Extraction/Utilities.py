
import cPickle
def load_dict(path):
 print " Loading ",path, " ..."
 file_path = path
 file_open = open(file_path, 'rb')
 dict=cPickle.load(file_open)
 file_open.close()
 print " Loading ", path, "finished ! "
 return dict

import os
def dump_dict(path, dict):
    print "dumping ",path, " ..."

    output_path = path
    if os.path.exists(output_path):
        os.remove(output_path)
    out_file = open(output_path, 'wb')

    cPickle.dump(dict, out_file, protocol=cPickle.HIGHEST_PROTOCOL)

    out_file.close()

    print "dumping ", path, " finished ..."

def load_doc_length_info():
 print "Loading doc_length_dict ..."
 path_doc_length_dict = 'runtime_cache/DOCUMENT_LENGTH_DICT.cpkl'
 file_doc_length_dict = open(path_doc_length_dict, 'rb')
 doc_length_dict=cPickle.load(file_doc_length_dict)
 file_doc_length_dict.close()

 return doc_length_dict

def get_avg_doc_length(DOC_LENGTH_DICT):
    sum = 0
    for doc_id in DOC_LENGTH_DICT:
        doc_length = DOC_LENGTH_DICT[doc_id]
        sum += doc_length

    avg=float(sum)/len(DOC_LENGTH_DICT)
    return avg

import string
from nltk import PorterStemmer
# read query from file and preprocess them
def get_valid_queries():

    #step1 read query strings from file and preprocess them
    queries_strings = dict()
    path = "runtime_cache/query_desc.51-100.short.txt"
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
    stemmer = PorterStemmer()
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

def get_stop_word():
    file = open('runtime_cache/stoplist.txt', 'r')
    stop_words = set()
    word = ''
    while True:
        word = file.readline().strip()
        if word == '':
            break
        stop_words.add(word)
    file.close()
    return stop_words


from elasticsearch import Elasticsearch
def search_term(term):
    es = Elasticsearch()
    result = es.search(
        index='ap89_index',
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
def get_term_statistics(term):
    es = Elasticsearch()
    result = es.search(
        index='ap89_index',
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


def get_unique_term_num():
    es=Elasticsearch()
    response=es.search(
        index='ap89_index',
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


def Okapi_TF(query,DOC_LENGTH_DICT,AVG_DOC_LENGTH,D,V):

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

def TF_IDF(query,DOC_LENGTH_DICT,AVG_DOC_LENGTH,D,V):
    D = len(DOC_LENGTH_DICT)
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

def Okapi_BM25(query,DOC_LENGTH_DICT,AVG_DOC_LENGTH,D,V):
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

def Unigram_LM_Laplace_Smoothing(query,DOC_LENGTH_DICT,AVG_DOC_LENGTH,D,V):
    score_list = dict()

    for term in query:
        term_inverted_file,ttf = get_term_statistics(term)

        if ttf==0:
            continue# if the corpus didn't contain the term, continue to next term

        for doc_id in DOC_LENGTH_DICT:

            tf=0#default is zero
            if term_inverted_file.has_key(doc_id):
                tf=term_inverted_file[doc_id]

            term_score = math.log(  float(tf + 1)/ (DOC_LENGTH_DICT[doc_id] + V), 2)

            if score_list.has_key(doc_id):
                score_list[doc_id] += term_score
            else:
                score_list[doc_id] = term_score

    return score_list

import math
def Unigram_LM_Jelinek_Mercer_Smoothing(query,DOC_LENGTH_DICT,AVG_DOC_LENGTH,D,V):
    score_list = dict()
    para_lambda=0.6
    total_doc_length=AVG_DOC_LENGTH*len(DOC_LENGTH_DICT)
    #get score
    for term in query:

        term_inverted_file, ttf=get_term_statistics(term)
        if  ttf==0:
            continue
            # if the corpus didn't contain the term, continue to next term

        for doc_id in DOC_LENGTH_DICT:

            # get tf in doc (default is zero)
            tf = 0
            if term_inverted_file.has_key(doc_id):
                tf = term_inverted_file[doc_id]

            if DOC_LENGTH_DICT[doc_id]!=0:
                foreground_prob=para_lambda*tf/DOC_LENGTH_DICT[doc_id]
            else:
                foreground_prob = 0

            background_prob = (1 - para_lambda)*ttf/total_doc_length
            base=2
            term_score = math.log( (foreground_prob + background_prob)  , base)

            if score_list.has_key(doc_id):
                score_list[doc_id] += term_score
            else:
                score_list[doc_id] = term_score

    return score_list


from collections import defaultdict
def extract_qrel_info(valid_queries):


    true_label_set = defaultdict(dict)
    qrel_file = open("runtime_cache/qrels.adhoc.51-100.AP89.txt","r")

    while True:
        line = qrel_file.readline().strip()
        if line == '':
            break

        query_id, author, doc_id, true_score = line.strip().split()
        query_id = query_id.strip()
        doc_id = doc_id.strip()
        true_score = int(true_score.strip())


        if query_id in valid_queries:
            true_label_set[query_id][doc_id]=true_score



    return  true_label_set


from random import randint
from sklearn.metrics import mean_squared_error , mean_absolute_error
from math import sqrt

# cal the rmse between the actual label and predict label
def getRMSE(yTest, yPredict):
    return sqrt(mean_squared_error(yTest, yPredict))

# get the rand float between start and end
def getRandFloat(start, end):
    return float(randint(start * 100, end * 100 + 1)) / 100

def getMAE(yTest, yPredict):
    return mean_absolute_error(yTest, yPredict)


def outputResult(predicted_dataset, predictedLabels, result_path):
    # output the prediction
    test_qids = predicted_dataset['query_id'].values
    test_docids = predicted_dataset['doc_id'].values

    result_dict = dict()
    i = 0
    for i in range(0, len(predictedLabels), 1):

        query_id = test_qids[i]
        doc_id = test_docids[i]
        label = predictedLabels[i]

        if not result_dict.has_key(query_id):
            result_dict[query_id] = dict()

        result_dict[query_id][doc_id] = label

    import os
    sep = "\t"

    if os.path.exists(result_path):
        os.remove(result_path)
    file = open(result_path, "w")

    for query_id in result_dict:
        score_list = result_dict[query_id]
        rank_num = 1
        for doc_id in sorted(score_list, key=score_list.get, reverse=True):
            file.write(str(query_id))

            file.write(sep + "Yu_Wen")

            file.write(sep + str(doc_id))

            file.write(sep + str(rank_num))

            file.write(sep + str(result_dict[query_id][doc_id]))

            file.write(sep + "Exp")

            file.write("\n")

            rank_num += 1



if __name__=="__main__":
    load_doc_length_info()
