import cPickle

import math
import time
from nltk import PorterStemmer,SnowballStemmer
from Util import *
from collections import OrderedDict

def initialize(field, stopping, stemming):
    s_time = time.time()
    print "Start initialization ..."

    #load basic informations

    global Stemmer
    global Stop_Words
    global IndexType
    Stemmer = PorterStemmer()#SnowballStemmer('english')
    Stop_Words= get_stop_word()
    IndexType = get_index_type(field, stopping, stemming)


    #load catalog file and hdd inverted files
    global Catalog
    global InvertedFileHDD
    inverted_folder="../inverted_files/"+IndexType+"/"
    Catalog=cPickle.load(open(inverted_folder+"round_7_no_1_merged_catalog","r"))
    InvertedFileHDD=open(inverted_folder+"round_7_no_1_merged_inverted_lst","rb")


    # load aux files and informations
    global Mapping_DocID_to_Num  # <Doc_ID, Doc_ID_No>
    global Mapping_Num_to_Doc_ID # <Doc_ID_No, Doc_ID>
    global Mapping_Term_to_Num  # <Term,Term_No>
    global Mapping_Num_to_Term  #<Term_NO,Term>
    global DOC_LENGTH_DICT  # <Doc_ID_No,Length>
    global NON_EMPTY_ID_LIST  # []
    global valid_query_set
    global D
    global TOTAL_DOC_LENGTH
    global AVG_DOC_LENGTH
    global V
    aux_folder = "../aux_files/" + IndexType + "/"

    Mapping_DocID_to_Num = cPickle.load(open(aux_folder + "map_docID_to_num", "r"))
    Mapping_Num_to_Doc_ID = cPickle.load(open(aux_folder + "map_num_to_docID", "r"))
    Mapping_Term_to_Num = cPickle.load(open(aux_folder + "map_term_to_num", "r"))
    Mapping_Num_to_Term = cPickle.load(open(aux_folder + "map_num_to_term", "r"))
    DOC_LENGTH_DICT = cPickle.load(open(aux_folder + "doc_length", "r"))
    NON_EMPTY_ID_LIST = cPickle.load(open(aux_folder + "non_empty_docID_lst", "r"))

    D = len(NON_EMPTY_ID_LIST)
    TOTAL_DOC_LENGTH = get_total_document_length(DOC_LENGTH_DICT, NON_EMPTY_ID_LIST)
    AVG_DOC_LENGTH = (TOTAL_DOC_LENGTH * 1.0) / (D * 1.0)
    V = len(Catalog)  # 160968

    e_time = time.time()
    print "Time usage of loading data : ", e_time - s_time, "seconds"

    return

def Okapi_TF(query):

    score_list = dict()

    for term in query:

        term=str(term)
        # the term is not found in corpus
        if not Mapping_Term_to_Num.has_key(term):
            continue

        term_id = Mapping_Term_to_Num[term]
        df,cf,hits=decode_TermInvertedList_from_HDD(term_id,Catalog,InvertedFileHDD)

        if df>6500:
            continue

        for num_docID in hits.keys():
            tf = len(hits[num_docID])

            str_docID=Mapping_Num_to_Doc_ID[num_docID]
            if score_list.has_key(str_docID):
                score_list[str_docID] += (tf * 1.0) / (tf + 0.5 + (1.5 * DOC_LENGTH_DICT[num_docID] / AVG_DOC_LENGTH))
            else:
                score_list[str_docID] = (tf * 1.0) / (tf + 0.5 + (1.5 * DOC_LENGTH_DICT[num_docID] / AVG_DOC_LENGTH))

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
        term = str(term)



        # the term is not found in corpus
        if not Mapping_Term_to_Num.has_key(term):
            continue

        term_id = Mapping_Term_to_Num[term]
        df, cf, hits = decode_TermInvertedList_from_HDD(term_id, Catalog, InvertedFileHDD)

        for num_docID in hits.keys():

            tf = len(hits[num_docID])

            #get tf_wq
            tf_wq=QUERY_TF_DICT[term]

            #get left part
            base=2
            left_part=math.log((D * 1.0 + 0.5) / (df + 0.5) ,base)

            # get middle part
            middle_part=(tf +  k1*tf )*1.0 / (tf + k1*((1-b) + b*(DOC_LENGTH_DICT[num_docID] / AVG_DOC_LENGTH)))

            # get right part
            right_part=(tf_wq + k2*tf_wq)*1.0 / (tf_wq + k2)

            #get the term score
            term_score = left_part*middle_part*right_part

            str_docID = Mapping_Num_to_Doc_ID[num_docID]
            if score_list.has_key(str_docID):
                score_list[str_docID] += term_score
            else:
                score_list[str_docID] = term_score

    return score_list

def Unigram_LM_Jelinek_Mercer_Smoothing(query):
    score_list = dict()
    para_lambda=0.6

    #get score
    for term in query:

        # if the corpus didn't contain the term, continue to next term
        # the term is not found in corpus
        if not Mapping_Term_to_Num.has_key(term):
            continue

        term_id = Mapping_Term_to_Num[term]
        df, cf, hits = decode_TermInvertedList_from_HDD(term_id, Catalog, InvertedFileHDD)

        for num_docID in NON_EMPTY_ID_LIST:
            # get tf in doc (default is zero)
            tf = 0
            if hits.has_key(num_docID):
                tf = len(hits[num_docID])

            foreground_prob=para_lambda*tf/DOC_LENGTH_DICT[num_docID]
            background_prob=(1-para_lambda)*cf/TOTAL_DOC_LENGTH
            base=2
            term_score = math.log( (foreground_prob + background_prob)  , base)

            str_docID = Mapping_Num_to_Doc_ID[num_docID]
            if score_list.has_key(str_docID):
                score_list[str_docID] += term_score
            else:
                score_list[str_docID] = term_score

    return score_list

# data structure of entry in the list: (docid, term4Positions, term5positions,.....)
def get_termPositions_list(query):
    termPositions_list=dict()
    for str_term in query:

        if not Mapping_Term_to_Num.has_key(str_term):# skp the term didn't contain in corpus
            continue

        term_id=Mapping_Term_to_Num[str_term]
        df,cf,termILst=decode_TermInvertedList_from_HDD(term_id, Catalog, InvertedFileHDD)
        for doc_id in termILst:
            if not termPositions_list.has_key(doc_id):
                termPositions_list[doc_id]=[termILst[doc_id]]
            else:
                termPositions_list[doc_id].append(termILst[doc_id])

    return termPositions_list




def filt_PoximiSearch_queries(valid_query_set):

    return valid_query_set

import heapq as heapQueue
import sys
def get_MinimumSpan(termPositionsLst):
    minimumSpan = sys.maxint
    smallest_list = [sys.maxint] * len(termPositionsLst)
    stop_search=False

    #create heap queue
    for termPositions in termPositionsLst:
        heapQueue.heapify(termPositions)

    #init smallest_list
    for i in range(0, len(termPositionsLst)):
        smallest_list[i] = heapQueue.heappop(termPositionsLst[i])


    while not stop_search:
        # get max in smallest list
        maximum = -1
        for i in range(0, len(smallest_list)):
            maximum = max(maximum, smallest_list[i])

        # get minimum in smallest list
        minimum = sys.maxint
        minimumIndex = -1
        for i in range(0, len(smallest_list)):
            if  smallest_list[i]<minimum:
                minimum = smallest_list[i]
                minimumIndex = i

        if termPositionsLst[minimumIndex]:

            smallest_list[minimumIndex] = heapQueue.heappop(termPositionsLst[minimumIndex])
        else:
            # minimumIndex=-1, minimum in smallest is not changing
            stop_search = True

        new_span = maximum - minimum
        minimumSpan = min(minimumSpan, new_span)


    return minimumSpan

def Proximity_Search(query):
    score_list = dict()
    termPositions_list=get_termPositions_list(query)
    skip_threshold=3
    skipNum=0
    C=1500
    for num_DocID in termPositions_list:
        if len(termPositions_list[num_DocID]) <skip_threshold:
            # skip the doc contains less than 3 query terms
            #print "Skipped doc id,", Mapping_Num_to_Doc_ID[num_DocID]
            skipNum +=1
            continue

        min_span=get_MinimumSpan(termPositions_list[num_DocID])

        num_ContainTerms=len(termPositions_list[num_DocID])

        doc_score=1.0*(C-min_span)*num_ContainTerms/(DOC_LENGTH_DICT[num_DocID]+V)

        # add score to score list
        str_docID = Mapping_Num_to_Doc_ID[num_DocID]
        score_list[str_docID] = doc_score


    #print skipNum,' hit docs contain less than ',skip_threshold,' query terms in this query, thus are skipped'
    print "######", len(termPositions_list)-skipNum,"/", len(termPositions_list),"#### hit docs returned in score list"
    return score_list

def performe_queries(retrieval_model, output_docNum, model_output_path, valid_query_set):
    print "  Model chosen: ", retrieval_model.func_name
    if os.path.exists(model_output_path):
        os.remove(model_output_path)
    output_file = open(model_output_path, 'w')

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

    return



t1=time.time()
print "Start process of all queries ..."


#Assign index type
field = "TEXT"
stopping = True
stemming = True
initialize(field, stopping, stemming)

# get queries
output_docNum = 1000
valid_query_set = get_valid_queries(stopping, Stop_Words, stemming, Stemmer)


#Assign Model and run
# retrieval_model=Okapi_TF
# model_output_path= "../output/" + IndexType + "/Okapi_TF.txt"
# performe_queries(retrieval_model, output_docNum, model_output_path, valid_query_set)


# retrieval_model = Okapi_BM25
# model_output_path = "../output/" + IndexType + "/Okapi_BM25.txt"
#performe_queries(retrieval_model, output_docNum, model_output_path, valid_query_set)


# retrieval_model=Unigram_LM_Jelinek_Mercer_Smoothig
# model_output_path= "../output/" + IndexType + "/Unigram_LM_Jelinek_Mercer_Smoothing.txt"
# performe_queries(retrieval_model, output_docNum, model_output_path, valid_query_set)


retrieval_model=Proximity_Search
model_output_path= "../output/" + IndexType + "/Proximity_Search.txt"
# performe_queries(retrieval_model, output_docNum, model_output_path, valid_query_set)

#skipped
# retrieval_model=TF_IDF
# model_output_path= "../output/" + IndexType + "/TF_IDF.txt"


# retrieval_model=Unigram_LM_Laplace_Smoothing
# model_output_path= "../output/" + IndexType + "/Unigram_LM_Laplace_Smoothing.txt"




t2=time.time()
print "Time usage of execution of all queries is : ", (t2-t1), " seconds"



























#test  functions


def produce_TfCfTest_result_file(testInput,testOuput,stemming):
    input_file=open(testInput, "r")

    remove_file(testOuput)
    output_file = open(testOuput, "w")

    #read test set
    outputSet =OrderedDict()
    test_term=input_file.readline().strip()
    while test_term!="":
        outputSet[test_term]=None
        test_term = input_file.readline().strip()


    # get info from index
    # query info

    for testTerm in outputSet.keys():
        queryTerm = testTerm
        if stemming:
            queryTerm = Stemmer.stem(queryTerm)

        if not Mapping_Term_to_Num.has_key(queryTerm):
            print "not found term in term file", queryTerm
            outputSet[testTerm] = (0, 0)
            continue

        query_termID = Mapping_Term_to_Num[queryTerm]

        if not Catalog.has_key(query_termID):
            print "not found term in catalog file", queryTerm
            outputSet[testTerm] = (0, 0)
            continue


        df, cf, ilst = decode_TermInvertedList_from_HDD(query_termID, Catalog, InvertedFileHDD)
        outputSet[testTerm] = (df, cf)


    # output result
    for testTerm in outputSet:
        info_str= testTerm+" "+str(outputSet[testTerm][0])+" "+str(outputSet[testTerm][1])+"\n"
        output_file.write(info_str)

    output_file.close()

    return


# IndexTest_TermFIle = "../output/" + IndexType + "/in.0.50.txt"
# IndexTest_OutFile = "../output/" + IndexType + "/out.50.txt"
IndexTest_TermFIle = "../output/" + IndexType + "/in.1"
IndexTest_OutFile = "../output/" + IndexType + "/out.1"
Stem=True
# produce_TfCfTest_result_file(IndexTest_TermFIle, IndexTest_OutFile,Stem)








def indexToyTest_stopping_stemming(trueResults,stemming):
    print "Toy test stopping stemming begins..."
    # read standard result

    standardResult_file = open(trueResults, "r")
    trueResult = dict()
    result_info = standardResult_file.readline().strip()
    while result_info != "":
        result_info = result_info.split(" ")
        trueResult[result_info[0]] = (int(result_info[1]), int(result_info[2]))
        # read next line
        result_info = standardResult_file.readline().strip()

    #query info
    outputSet=dict()
    testTerms=trueResult.keys()
    for testTerm in testTerms:
        queryTerm=testTerm
        if stemming:
            queryTerm=Stemmer.stem(queryTerm)


        if not Mapping_Term_to_Num.has_key(queryTerm):

                print "not found term in map file", queryTerm
                outputSet[testTerm]=(0,0)
                continue


        query_termID=Mapping_Term_to_Num[queryTerm]

        if not Catalog.has_key(query_termID):
            print "not found term in catalog file", queryTerm
            outputSet[testTerm] = (0, 0)
            continue

        df,cf,ilst=decode_TermInvertedList_from_HDD(query_termID,Catalog,InvertedFileHDD)

        outputSet[testTerm]=(df,cf)


    #print accuracy
    accu_num=0
    for testTerm in testTerms:
        outputTuple=outputSet[testTerm]
        trueTuple=trueResult[testTerm]
        if outputTuple[0]==trueTuple[0] and outputTuple[1]==trueTuple[1]:
            accu_num +=1
        else:
            print "wrong term: ",testTerm
            print "true tuple (df,cf)", trueTuple
            print "output tuple (df,cf)",outputTuple
            print " "

    print "accuracy : ",accu_num*1.0/len(testTerms)


#trueResults = "../output/" + IndexType + "/out.0.stop.stem.txt"
#stemming=True
#indexToyTest_stopping_stemming(trueResults,stemming)



