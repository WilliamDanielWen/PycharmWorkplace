import cPickle
import time
from  Util import *
from nltk import PorterStemmer


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


def decode_readable_InvertedFile_from_HDD(catalog, hdd_inverted_file):
    mem_inverted_file=dict()
    for term_id in catalog.keys():
        df, cf, term_inverted_list=decode_readable_TermInvertedList_from_HDD(term_id, catalog, hdd_inverted_file)

        #map to readable
        term_id=Mapping_Num_to_Term[term_id]

        mem_inverted_file[term_id]=term_inverted_list
    return mem_inverted_file


def decode_readable_TermInvertedList_from_HDD(term_id, catalog, hdd_inverted_file):

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

        #map to readable
        doc_id=Mapping_Num_to_Doc_ID[doc_id]

        term_inverted_list[doc_id] = []
        for j in range(1, len(doc_info), 1):
            term_inverted_list[doc_id].append(int(doc_info[j]))

    return df, cf, term_inverted_list


def testTF_DF():
    partyman=Mapping_Term_to_Num["partyman"]
    partyman=decode_readable_TermInvertedList_from_HDD(partyman,Catalog,InvertedFileHDD)

    #imported = Mapping_Term_to_Num["imported"]
    #imported = decode_readable_TermInvertedList_from_HDD(imported, Catalog, InvertedFileHDD)

    waterway = Mapping_Term_to_Num["waterway"]
    waterway = decode_readable_TermInvertedList_from_HDD(waterway, Catalog, InvertedFileHDD)
    breakpoint=1




field = "TEXT"
stopping = True
stemming = True
initialize(field, stopping, stemming)

# h1 = [3]
# h2 = [4,6,8, 99]
# h3 = [5,234234,1345234]
#
# l = [h1, h2 , h3]
# print l
#
# print get_MinimumSpan(l)




