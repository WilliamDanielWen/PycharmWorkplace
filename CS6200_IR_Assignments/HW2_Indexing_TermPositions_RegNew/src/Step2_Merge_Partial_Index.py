import cPickle
import glob
import Queue
import time
from collections import OrderedDict
from Util import decode_TermInvertedList_from_HDD\
                 ,encode_MemInvertedFile_to_HDDInvertedFile\
                 ,remove_file\
                ,cpkl_dump


def merge_two_partial_index(first_file_path_tuple, second_file_path_tuple, round_no, merge_no):

    #get readable file pointers
    first_inverted_p=first_file_path_tuple[0]
    first_catalog_p=first_file_path_tuple[1]
    second_inverted_p=second_file_path_tuple[0]
    second_catalog_p=second_file_path_tuple[1]
    first_HddInvertedFile=open(first_inverted_p,"rb")
    first_CatalogFile=open(first_catalog_p,"r")
    second_HddInvertedFile=open(second_inverted_p,"rb")
    second_CatalogFile=open(second_catalog_p,"r")

    #get catalog in memory
    first_catalog=cPickle.load(first_CatalogFile)
    second_catalog=cPickle.load(second_CatalogFile)


    # produce output paths of merged file
    folder_path = first_inverted_p.rstrip(first_inverted_p.split("/")[-1])
    prefix = folder_path + "round_" + str(round_no) + "_no_" + str(merge_no)
    merged_inverted_p = prefix + "_merged_inverted_lst"
    merged_catalog_p = prefix + "_merged_catalog"

    #clean previous enviroment and get the writable file pointer
    remove_file(merged_inverted_p)
    remove_file(merged_catalog_p)

    merged_InvertedFile=open(merged_inverted_p,"wb")


    merged_InvertedFileCache=dict()
    merged_Catalog = dict()
    merged_num=0
    for term_id in first_catalog.keys():

        #pull out information in hdd_file1
        df, cf, merged_TermInvertedLst=decode_TermInvertedList_from_HDD(term_id, first_catalog, first_HddInvertedFile)
        first_catalog.pop(term_id)
        # pull out information in hdd_file2 and merge it
        if second_catalog.has_key(term_id):
            df2, cf2, second_TermInvertedLst = decode_TermInvertedList_from_HDD(term_id, second_catalog, second_HddInvertedFile)
            merged_TermInvertedLst.update(second_TermInvertedLst)
            second_catalog.pop(term_id)


        #sort the merged_TermInvertedLst
        merged_InvertedFileCache[term_id]=OrderedDict(sorted(merged_TermInvertedLst.items(),key=lambda t:len(t[1]), reverse= True))
        merged_num+=1


        #keep the usage of memory, write merged_InvertedFileCache to hdd and clear it
        new_catalog = encode_MemInvertedFile_to_HDDInvertedFile(merged_InvertedFileCache,merged_InvertedFile)
        merged_Catalog.update(new_catalog)
        merged_InvertedFileCache.clear()
    print merged_num, "terms have been merged in this merge "

    #get remain terms in second_catalog
    for term_id in second_catalog.keys():
        df, cf, merged_TermInvertedLst = decode_TermInvertedList_from_HDD(term_id, second_catalog, second_HddInvertedFile)
        second_catalog.pop(term_id)
        # sort the merged_TermInvertedLst
        merged_InvertedFileCache[term_id] = OrderedDict(sorted(merged_TermInvertedLst.items(), key=lambda t: len(t[1]), reverse=True))
        merged_num += 1

        # keep the usage of memory, write merged_InvertedFileCache to hdd and clear it
        new_catalog = encode_MemInvertedFile_to_HDDInvertedFile(merged_InvertedFileCache, merged_InvertedFile)
        merged_Catalog.update(new_catalog)
        merged_InvertedFileCache.clear()
    print merged_num, "terms have been merged in this merge "

    #dump the new catalog
    cpkl_dump(merged_Catalog,merged_catalog_p)

    #close files
    first_HddInvertedFile.close()
    first_CatalogFile.close()
    second_HddInvertedFile.close()
    second_CatalogFile.close()
    merged_InvertedFile.close()

    #print merged_inverted_p
    #print merged_catalog_p
    return (merged_inverted_p,merged_catalog_p)

def merge_partial_index(IndexType):
    s_time=time.time()
    # get all partial files into merge_queue
    FILE_SET_REGULAR_EXPRESSION="../inverted_files_partial/"+IndexType+"/inverted_lst.*"
    inverted_file_paths=glob.glob(FILE_SET_REGULAR_EXPRESSION)
    merge_queue=Queue.Queue() # the element is tuple of(inverted_file_path, corresponding_catalog_file_path)
    for inverted_file_path in  inverted_file_paths:

        inverted_file_name=inverted_file_path.split("/")[-1]

        catalog_file_name=inverted_file_name.replace("inverted_lst","catalog")
        catalog_file_path=inverted_file_path.rstrip(inverted_file_name)+catalog_file_name

        merge_queue.put((inverted_file_path,catalog_file_path))



    result_queue = Queue.Queue() # data structure to store the paths of the merged files
    round_no = 1
    merge_no = 1
    print "##### Round ", round_no, " merging begins ..."

    if merge_queue.qsize()%2!=0:
        # if the number of files are odd, put the first file to next round to be merged
        first=merge_queue.get()
        result_queue.put(first)

    while True:
        # we make sure the size of merge_queue is even
        first_path_tuple=merge_queue.get()
        second_path_tuple=merge_queue.get()


        merged_file_path_tuple=merge_two_partial_index(first_path_tuple,second_path_tuple,round_no,merge_no)
        print merge_no, " merges have been processed in round ", round_no
        print ""
        merge_no += 1

        #put the merged file tuple in result queue
        result_queue.put(merged_file_path_tuple)

        if merge_queue.qsize()==0:
            if result_queue.qsize()==1:
                #all round finished
                e_time = time.time()
                print "##### Round ", round_no, " merging finished, time usage : ", (e_time - s_time) / 60, " minutes"
                break
            else:
                # one round finished
                e_time=time.time()
                print "##### Round ", round_no, " merging finished, time usage : ", (e_time-s_time)/60," minutes"
                s_time=e_time

                # begin another round
                merge_queue=result_queue
                result_queue=Queue.Queue()
                round_no += 1
                merge_no = 1
                print "##### Round ", round_no, " merging begins ..."
                if merge_queue.qsize() % 2 != 0:
                    first = merge_queue.get()
                    result_queue.put(first)


    print "############# Merging finished #############"




from Step1_Tokenizing_Indexing_Partial \
import   Indexing_TEXT_Stopping_Stemming\
        ,Indexing_TEXT_Without_Stopping_Without_Stemming\
        ,Indexing_TEXT_Without_Stopping_Stemming\
        ,Indexing_TEXT_Stopping_Without_Stemming


print"$$$$$$$$$$$ Indexing_TEXT_Stopping_Stemming"
Indexing_TEXT_Stopping_Stemming()

print"$$$$$$$$$$$ Indexing_TEXT_Without_Stopping_Without_Stemming"
Indexing_TEXT_Without_Stopping_Without_Stemming()

print"$$$$$$$$$$$ Indexing_TEXT_Without_Stopping_Stemming"
Indexing_TEXT_Without_Stopping_Stemming()

print"$$$$$$$$$$$ Indexing_TEXT_Stopping_Without_Stemming"
Indexing_TEXT_Stopping_Without_Stemming()




IndexType="TEXT_Stopping_Stemming"
print "$$$$$$$$$$$$$$ Mergin Index ",IndexType
merge_partial_index(IndexType)

IndexType="TEXT_Without_Stopping_Without_Stemming"
print "$$$$$$$$$$$$$$ Mergin Index ",IndexType
merge_partial_index(IndexType)


IndexType="TEXT_Without_Stopping_Stemming"
print "$$$$$$$$$$$$$$ Mergin Index ",IndexType
merge_partial_index(IndexType)

IndexType="TEXT_Stopping_Without_Stemming"
print "$$$$$$$$$$$$$$ Mergin Index ",IndexType
merge_partial_index(IndexType)