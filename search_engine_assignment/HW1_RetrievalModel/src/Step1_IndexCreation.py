from elasticsearch import Elasticsearch
import time
import string
import glob
import re
import os

#index name used in piazza
INDEX_NAME = 'ap89_index'
WHOLE_DOC_ID_LIST=[]


#suggested process from piazza
def initialize_index_in_elasticsearch(instance):
    print "Initializing index ..."

    print "     Cleaning previous environment ..."
    instance.indices.delete(index=INDEX_NAME, ignore=404)

    print "     Creating index ..."
    instance.indices.create(
        index=INDEX_NAME,
        body={
            'settings': {
                "index": {
                    "store": {
                        "type": "default"
                    },
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },

                'analysis': {
                    "analyzer": {
                        "my_english": {
                            "type": "english",
                            "stopwords_path": "stoplist.txt"
                        }
                    }
                }
            }
        }

    )
    print "     Setting properties of type of \'document\' ..."
    instance.indices.put_mapping(
        index= INDEX_NAME,
        doc_type='document',
        body={
            'document': {
                "properties": {
                    "docno": {
                        "type": "string",
                        "store": True,
                        "index": "not_analyzed"
                    },

                    #only analyze the text filed
                    "text": {
                        "type": "string",
                        "store": True,
                        "index": "analyzed",
                        "term_vector": "with_positions_offsets_payloads",
                        "analyzer": "my_english"
                    }
                }
            }
        }
    )

#index documents in files into the index
def index_documents_from_files(es_client,re_file_set):
    #prepare the output file of document list
    output_path_doc_id_list="../runtime_cache/WHOLE_DOC_ID_LIST"
    if os.path.exists(output_path_doc_id_list):
        os.remove(output_path_doc_id_list)
    output_file_doc_id_list = open(output_path_doc_id_list, 'a')


    print "Indexing documents from files ..."
    file_count=0
    doc_count=0
    #loop for all files in the returned list of path names that match re_file_set
    for single_ap_file in glob.glob(re_file_set):

        #get contents in one single file
        fragments_of_single_file = string.split(open(single_ap_file, "r", 1024).read(), "</DOC>")

        #extract documents from contents and index it
        for single_fragment in fragments_of_single_file:

            #skip the empty data
            if len(single_fragment.strip()) < 1  or len(single_fragment) < 1:
                continue

            #extract one document
            # use the non greedy "*?"
            pattern_docno = re.compile(r"<DOCNO>(.*?)</DOCNO>")
            doc_no = "".join(pattern_docno.findall(single_fragment)).strip()
            #output the doc_no as doc_id
            WHOLE_DOC_ID_LIST.append(doc_no)
            output_file_doc_id_list.write(doc_no+"\n")

            pattern_text = re.compile(r"<TEXT>(.*?)</TEXT>", re.MULTILINE| re.DOTALL)
            doc_text = "".join(pattern_text.findall(single_fragment))

            document_extracted=dict(docno=doc_no, text=doc_text)
            doc_count += 1

            #index the doc
            es_client.index(index=INDEX_NAME, doc_type='document', id=doc_no, body=document_extracted)
        #end indexing  one file

        file_count += 1
        print  "    ",file_count," files (",doc_count ,"documents) have been indexed ..."

#start of program
t1 = time.time()
es_client = Elasticsearch()

initialize_index_in_elasticsearch(es_client)

FILE_SET_REGULAR_EXPRESSION = "../../Data/ap89_collection/ap*"
index_documents_from_files(es_client,FILE_SET_REGULAR_EXPRESSION)

print  "Indexing files finished!"

es_client.indices.refresh(index= INDEX_NAME)

t2 = time.time()
print "Time usage of index creation is: ", (t2 - t1) / 60, 'minutes'
