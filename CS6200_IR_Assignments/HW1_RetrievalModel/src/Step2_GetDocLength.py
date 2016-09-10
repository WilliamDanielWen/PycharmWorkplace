from elasticsearch import Elasticsearch
import cPickle
import os
import time

def load_whole_doc_id_list():
    whole_doc_id_list = []
    doc_id_list_file = open("runtime_cache/WHOLE_DOC_ID_LIST", "r")
    doc_id = doc_id_list_file.readline().strip()

    while not doc_id == '':
        whole_doc_id_list.append(doc_id)
        doc_id = doc_id_list_file.readline().strip()

    return whole_doc_id_list


def get_query_info():
    print " Getting information of document length ..."

    DOCUMENT_LENGTH_DICT = dict()  # sturcture: {doc id:  doc length}
    WHOLE_DOC_ID_LIST=load_whole_doc_id_list()
    es_client=Elasticsearch()
    doc_processed=0
    for doc_id in  WHOLE_DOC_ID_LIST:
        #get termvecotr of document with doc_id
        document = es_client.termvectors(
            index='ap89_index',
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
            DOCUMENT_LENGTH_DICT[str(doc_id)] = words_num_of_doc

        else:
            # for empty doc ignore all information,set doc length as zero
            DOCUMENT_LENGTH_DICT[str(doc_id)]=0
            continue
        doc_processed +=1
        if(doc_processed%100==0):
            print'   ',doc_processed,' documents has been processed ...'



    print'   ', doc_processed, ' documents has been processed ...'
    print " Finished getting information of tf, df and document length ..."

    return DOCUMENT_LENGTH_DICT


def output_query_info_to_file( doc_length_dict):
    path_doc_length_dict = '../runtime_cache/DOCUMENT_LENGTH_DICT.cpkl'
    if os.path.exists(path_doc_length_dict):
        os.remove(path_doc_length_dict)
    file_doc_length_dict = open(path_doc_length_dict, 'wb', 1024 * 1024 * 32)
    cPickle.dump(doc_length_dict, file_doc_length_dict, protocol=cPickle.HIGHEST_PROTOCOL)
    file_doc_length_dict.close()


#start step2
t1 = time.time()
print  "Preparaing query information ..."
doc_length_dict=get_query_info()
output_query_info_to_file(doc_length_dict)

t2 = time.time()
print  "Query information preparation finished!"
print "Time usage of Query information preparation is: ", (t2 - t1) / 60, 'minutes'