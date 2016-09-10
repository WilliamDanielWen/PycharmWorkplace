import glob
import cPickle
import os
import string
from collections import OrderedDict

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def clean_folder(folder_path):
    file_paths = os.path.join(folder_path, '*')
    for file_path in glob.glob(file_paths):
        remove_file(file_path)

def convert_to_lower_case(term_tuples):
    results = []
    for term_tuple in term_tuples:
        term = term_tuple[0].strip().lower()
        results.append(term)
    return results

def stemming_preprocess(terms, stemmer):
    #Stem
    results = []
    for term in terms:
        term = stemmer.stem(term)
        term =str(term)
        results.append(term)
    return results


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

def stopping_preprocess(terms,stop_words):
    #remove stop words in tokens
    results = []
    for term in terms:
        if  not term in stop_words:
            results.append(term)
    return results


def get_index_type(field, stopping, stemming):
    # get index type
    index_type = str(field)

    if not stopping:
        index_type += "_Without"
    index_type += "_Stopping"

    if not stemming:
        index_type += "_Without"
    index_type += "_Stemming"
    return index_type


def print_inverted_file(inverted_file):
    count=0
    for term in inverted_file:
        print term
        for docid in inverted_file[term].keys():
            print " ", docid, " ", inverted_file[term][docid]
        count +=1
        if count>20:
            break

def get_total_document_length(doc_length_dict, doc_id_list):
    sum=0
    for doc_id in doc_id_list:
        doc_length=doc_length_dict[doc_id]
        sum +=doc_length
    return sum


def get_total_cf(catalog, hdd_inverted_file):

    result=0
    for term_id in catalog:
        df,cf,termInvertedFile=decode_TermInvertedList_from_HDD(term_id,catalog,hdd_inverted_file)
        result+=cf

    return result

# read query from file and preprocess them
def get_valid_queries(stopping,stop_words,stemming,stemmer):

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


    # step2 remove remove words and stopping  and stemming process

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

        # remove the RMOVEWORDS
        for term in terms:
            if  term in REMOVE_WORDS:
                continue

            valid_terms.append(term)

        # stemming
        if stemming:
            valid_terms=stemming_preprocess(valid_terms,stemmer)

        # stopping
        if stopping:
            valid_terms = stopping_preprocess(valid_terms, stop_words)


        #insert the valid query term array
        valid_queries[query_no] = valid_terms

    return valid_queries

def cpkl_dump(dump_obj, output_file_path):
    remove_file(output_file_path)
    dump_file=open(output_file_path, "w")
    cPickle.dump(dump_obj, dump_file, protocol=cPickle.HIGHEST_PROTOCOL)
    dump_file.close()

#  termid,df,cf,docid tf pos1 pos2 pos3 ...posn,docid tf pos1 pos2 pos3 ... posn
def encode_MemInvertedFile_to_HDDInvertedFile_readble(mem_inverted_file, output_file):
    catalog=dict()
    for term_id in mem_inverted_file:
        output_str=""
        offset_start =output_file.tell()
        term_inverted_list = mem_inverted_file[term_id]
        df = len(term_inverted_list)
        cf = 0

        for doc_id in term_inverted_list:
            output_str += "," + str(doc_id)
            pos_list = term_inverted_list[doc_id]
            tf=len(pos_list)
            output_str += " " + "tf="+str(tf)
            cf += tf

            output_str +=" term_pos:["
            for pos in pos_list:
                output_str += str(pos)+","
            output_str=output_str.rstrip(",")
            output_str += "] "

        #add the information of term_id,
        output_str=str(term_id)+",df="+str(df)+",cf="+str(cf)+output_str+"\n"

        output_file.write(output_str)
        output_file.flush()
        offset_end =output_file.tell()
        offset_size=offset_end - offset_start

           #write into catalog
        catalog[term_id] = (offset_start,offset_size)

    return catalog

#  "termid",df,cf,docid "tf" pos1 pos2 pos3 ...posn,docid tf pos1 pos2 pos3 ... posn
def encode_MemInvertedFile_to_HDDInvertedFile(mem_inverted_file, hdd_inverted_file):
    catalog=dict()
    for term_id in mem_inverted_file:
        output_str=""
        offset_start =hdd_inverted_file.tell()
        term_inverted_list = mem_inverted_file[term_id]
        df = len(term_inverted_list)
        cf = 0

        for doc_id in term_inverted_list:
            output_str += "," + str(doc_id)
            pos_list = term_inverted_list[doc_id]
            tf=len(pos_list)
            #output_str += " " + str(tf)
            cf += tf

            for pos in pos_list:
                output_str += " " + str(pos)

        #add the information of term_id,
        #output_str=str(term_id)+","+str(df)+","+str(cf)+output_str
        output_str = str(df) + "," + str(cf) + output_str

        hdd_inverted_file.write(output_str)
        hdd_inverted_file.flush()
        offset_end =hdd_inverted_file.tell()
        offset_size=offset_end - offset_start

           #write into catalog
        catalog[term_id] = (offset_start,offset_size)

    return catalog


def decode_InvertedFile_from_HDD(catalog, hdd_inverted_file):
    mem_inverted_file=dict()
    for term_id in catalog.keys():
        df, cf, term_inverted_list=decode_TermInvertedList_from_HDD(term_id, catalog, hdd_inverted_file)
        mem_inverted_file[term_id]=term_inverted_list
    return mem_inverted_file


def decode_TermInvertedList_from_HDD(term_id, catalog, hdd_inverted_file):

    term_inverted_list = dict()
    offset_start = catalog[term_id][0]
    size = catalog[term_id][1]
    hdd_inverted_file.seek(offset_start)
    term_info = hdd_inverted_file.read(size).split(",")

    df = int(term_info[0])
    cf = int(term_info[1])

    for i in range(2, len(term_info), 1):
        doc_info = term_info[i].split(" ")
        doc_id = int(doc_info[0])

        term_inverted_list[doc_id] = []
        for j in range(1, len(doc_info), 1):
            term_inverted_list[doc_id].append(int(doc_info[j]))

    return df, cf, term_inverted_list


def sort_MemInvertedFile_by_tf(mem_inverted_file):
    for term_id in mem_inverted_file.keys():
        termInvertedList=mem_inverted_file[term_id]
        sorted_lst = sorted(termInvertedList.items(), key=lambda t: len(t[1]), reverse=True)
        ordered_termInvertedList = OrderedDict(sorted_lst)
        mem_inverted_file[term_id]=ordered_termInvertedList




