import glob
import string
import re
from nltk import PorterStemmer
import time
from Util import *

def initilize():
    global StopWords
    global Stemmer

    global Doc_ID_No  # 1,2,3,4.....
    global Term_No  # 1,2,3,4.....
    global Mapping_DocID_to_Num  # <Doc_ID, Doc_ID_No>
    global Mapping_Num_to_Doc_ID # <Doc_ID_No, Doc_ID>
    global Mapping_Term_to_Num  # <Term,Term_No>
    global Mapping_Num_to_Term  #<Term_NO,Term>

    global Doc_Length_List  # <Doc_ID_No,Length>
    global NonEmptyDocList #[]

    StopWords= get_stop_word()
    Stemmer = PorterStemmer()

    Doc_ID_No=0
    Term_No = 0

    Mapping_DocID_to_Num=dict()
    Mapping_Num_to_Doc_ID=dict()
    Mapping_Term_to_Num=dict()
    Mapping_Num_to_Term=dict()

    Doc_Length_List=dict()
    NonEmptyDocList=[]

def update_docId_num_mapping(doc_id):
    global Mapping_DocID_to_Num
    global Mapping_Num_to_Doc_ID
    global Doc_ID_No

    # new doc id encountered
    if not Mapping_DocID_to_Num.has_key(doc_id):
        Doc_ID_No += 1
        Mapping_DocID_to_Num[doc_id] = Doc_ID_No
        Mapping_Num_to_Doc_ID[Doc_ID_No]=doc_id

def update_term_num_mapping(term):
    global Mapping_Term_to_Num
    global Mapping_Num_to_Term
    global Term_No
    # new term detected
    if not Mapping_Term_to_Num.has_key(term):
        Term_No += 1
        Mapping_Term_to_Num[term] = Term_No
        Mapping_Num_to_Term[Term_No]=term

def dump_aux_files(field, stopping, stemming):
    index_type=get_index_type(field, stopping, stemming)
    # dump doc length file
    doc_length_path = "../aux_files/"+index_type+"/doc_length"
    cpkl_dump(Doc_Length_List, doc_length_path)
    print "########## doc_length file dumped  ####################"

    # dump non-empty doc id list
    non_empty_docID_lst_path = "../aux_files/" + index_type + "/non_empty_docID_lst"
    cpkl_dump(NonEmptyDocList, non_empty_docID_lst_path)
    print "########## non-empty doc id list  dumped  ####################"


    # dump docID-num mapping files
    docid_to_num_map_path = "../aux_files/"+index_type+"/map_docID_to_num"
    num_to_docid_map_path = "../aux_files/" + index_type + "/map_num_to_docID"
    cpkl_dump(Mapping_DocID_to_Num, docid_to_num_map_path)
    cpkl_dump(Mapping_Num_to_Doc_ID, num_to_docid_map_path)
    print "########## docID-num mapping files  dumped  ####################"


    # dump term-num mapping files
    term_to_num_map_path = "../aux_files/"+index_type+"/map_term_to_num"
    num_to_term_map_path = "../aux_files/" + index_type + "/map_num_to_term"
    cpkl_dump(Mapping_Term_to_Num, term_to_num_map_path)
    cpkl_dump(Mapping_Num_to_Term, num_to_term_map_path)
    print "##########  term-num mapping files   dumped  ####################"

def dump_partial_inverted_file_readable(partial_mem_inverted_file, num_doc_processed, field, stopping, stemming):
    print "Dumping partial inverted file....."
    # get index type
    index_type=get_index_type(field, stopping, stemming)

    # dump inverted list

    inverted_file_path = "../readable_version_inverted_files(stopping,stemming first 1000 docs)/readable_invert_lst"
    remove_file(inverted_file_path)
    inverted_file_output_file = open(inverted_file_path, "wb")
    partial_catalog_file = encode_MemInvertedFile_to_HDDInvertedFile_readble(partial_mem_inverted_file,inverted_file_output_file)
    inverted_file_output_file.close()
    print "########## partial  inverted file dumped  ####################"

    # dump catalog file
    catalog_path="../readable_version_inverted_files(stopping,stemming first 1000 docs)/catalog"
    cpkl_dump(partial_catalog_file,catalog_path)
    print "########## partial catalog file dumped  ####################"

def dump_partial_inverted_file(partial_mem_inverted_file, num_doc_processed, field, stopping, stemming):
    print "Dumping partial inverted file....."
    # get index type
    index_type=get_index_type(field, stopping, stemming)

    # dump inverted list
    inverted_file_path = "../inverted_files_partial/" + index_type + "/"+"inverted_lst."+str(num_doc_processed)+".partial"
    remove_file(inverted_file_path)
    inverted_file_output_file = open(inverted_file_path, "wb")
    partial_catalog_file = encode_MemInvertedFile_to_HDDInvertedFile(partial_mem_inverted_file, inverted_file_output_file)
    inverted_file_output_file.close()
    print "########## partial  inverted file dumped  ####################"

    # dump catalog file
    catalog_path = "../inverted_files_partial/" + index_type +"/"+ "catalog"+"."+str(num_doc_processed)+".partial"
    cpkl_dump(partial_catalog_file,catalog_path)
    print "########## partial catalog file dumped  ####################"

# write terms of doc_id  into  mem_interved_file
def parse_terms_in_one_doc(mem_interved_file, terms, doc_id):

    update_docId_num_mapping(doc_id)
    mapped_doc_id =Mapping_DocID_to_Num[doc_id]
    term_position = 1
    for term in terms:
        update_term_num_mapping(term)
        mapped_token_id = Mapping_Term_to_Num[term]
        if not mem_interved_file.has_key(mapped_token_id):
            mem_interved_file[mapped_token_id] = {mapped_doc_id: [term_position]}

        else:

            if mem_interved_file[mapped_token_id].has_key(mapped_doc_id):
                mem_interved_file[mapped_token_id][mapped_doc_id].append(term_position)
            else:
                mem_interved_file[mapped_token_id][mapped_doc_id] = [term_position]

        term_position += 1

    # store doc length info
    Doc_Length_List[mapped_doc_id] = len(terms)
    if len(terms) != 0:
        NonEmptyDocList.append(mapped_doc_id)

def create_index(field, stopping, stemming):
    FILE_SET_REGULAR_EXPRESSION = "../../Data/ap89_collection/ap*"

    if(field=="TEXT"): RE_FIELD_CONTENT = re.compile(r"<TEXT>(.*?)</TEXT>", re.MULTILINE | re.DOTALL)

    if(field=="HEAD"): RE_FIELD_CONTENT = re.compile(r"<HEAD>(.*?)</HEAD>", re.MULTILINE | re.DOTALL)

    num_file_processed = 0
    num_doc_processed = 0

    #inverted file store in memory
    partial_mem_inverted_file=dict()

    for single_ap_file in glob.glob(FILE_SET_REGULAR_EXPRESSION):#loop all doc set
        # content in one file
        fragments = string.split(open(single_ap_file, "r").read(), "</DOC>")

        # for contant between </DOC>, get tokens from one document
        for fragment in fragments:
            #skip the empty doc
            if len(fragment) < 1 or len(fragment.strip()) < 1:
                continue

            #get id
            re_docid = re.compile(r"<DOCNO>(.*?)</DOCNO>")
            doc_id = "".join(re_docid.findall(fragment)).strip()

            #get string content
            all_filed_content = "".join(RE_FIELD_CONTENT.findall(fragment))

            #get tokens

            # convert to lower case
            all_filed_content=all_filed_content.lower()

            #abort given regular expression
            #tokens_old = re.findall("(\w+(\.?\w+)*)",all_filed_content)
            #already in lower case, just get tokens from tuples
            #tokens_old= convert_to_lower_case(tokens_old)

            tokens = re.findall("(([a-z0-9]+\.)*[a-z0-9]+)", all_filed_content)
            tokens=get_suffix_dot(tokens)

            terms=tokens
            #stemming and stopping
            if stopping==True: terms=stopping_preprocess(terms,StopWords)
            if stemming == True: terms = stemming_preprocess(terms,Stemmer)

            # store all terms in doc id into cache
            parse_terms_in_one_doc(partial_mem_inverted_file, terms, doc_id)

            num_doc_processed += 1

            #print "doc-id: ",doc_id
            if num_doc_processed % 100 == 0:
                print num_doc_processed, " documents, ", num_file_processed, " files have been indexed"

            #dump partial inverted file
            if num_doc_processed%1000==0:
                sort_MemInvertedFile_by_tf(partial_mem_inverted_file)
                dump_partial_inverted_file(partial_mem_inverted_file,num_doc_processed,field,stopping,stemming)
                partial_mem_inverted_file.clear()

        num_file_processed += 1


    print num_doc_processed, " documents, ", num_file_processed, " files have been indexed"
    sort_MemInvertedFile_by_tf(partial_mem_inverted_file)
    dump_partial_inverted_file(partial_mem_inverted_file,num_doc_processed, field, stopping, stemming)

    dump_aux_files(field, stopping, stemming)
    # finished

# runtime calling
def Indexing_TEXT_Stopping_Stemming():
    field="TEXT"
    stopping=True
    stemming=True
    initilize()
    create_index(field, stopping, stemming)

def Indexing_TEXT_Without_Stopping_Stemming():
    field="TEXT"
    stopping=False
    stemming=True
    initilize()
    create_index(field, stopping, stemming)

def Indexing_TEXT_Stopping_Without_Stemming():
    field="TEXT"
    stopping=True
    stemming=False
    initilize()
    create_index(field, stopping, stemming)

def Indexing_TEXT_Without_Stopping_Without_Stemming():
    field="TEXT"
    stopping=False
    stemming=False
    initilize()
    create_index(field, stopping, stemming)

def Indexing_HEAD_Stopping_Stemming():
    field="HEAD"
    stopping=True
    stemming=True
    initilize()
    create_index(field, stopping, stemming)


#s_time=time.time()

#Indexing_TEXT_Stopping_Stemming()
#Indexing_TEXT_Without_Stopping_Without_Stemming()
#Indexing_TEXT_Without_Stopping_Stemming()
#Indexing_TEXT_Stopping_Without_Stemming()

#e_time=time.time()
#print "Indexing finished ,time usage " ,(e_time-s_time)/60 ," minutes"
print"####### This is the new version index with new reg expression"
