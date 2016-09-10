
import os
def split_data_set(Data_Set, field_header, train_set_path, test_set_path, test_queries):
    print "Outputing data set to csv ..."

    for i in range(0,len(test_queries),1):
        test_queries[i]=str(test_queries[i])


    if os.path.exists(train_set_path):
        os.remove(train_set_path)
    train_file=open(train_set_path,"w")


    if os.path.exists(test_set_path):
        os.remove(test_set_path)
    test_file=open(test_set_path,"w")

    #write header
    test_file.write("query_id"+",doc_id")
    train_file.write("query_id"+",doc_id")
    for field in field_header:

        test_file.write(","+field)
        train_file.write(","+field)

    test_file.write("\n")
    train_file.write("\n")


    # update static features
    for query_id in Data_Set:

        if query_id  in test_queries:

            for doc_id in Data_Set[query_id]:
                test_file.write(query_id + "," + doc_id)
                for field in field_header:
                    test_file.write("," + str(Data_Set[query_id][doc_id][field]))
                test_file.write("\n")

        else:

            for doc_id in Data_Set[query_id]:
                train_file.write(query_id+","+doc_id)
                for field in field_header:
                    train_file.write(","+str(Data_Set[query_id][doc_id][field]))
                train_file.write("\n")


import Utilities
if __name__=="__main__":

    field_header = ["label", "Okapi_TF", "TF_IDF", "Okapi_BM25", "Unigram_LM_Laplace_Smoothing",
                    "Unigram_LM_Jelinek_Mercer_Smoothing", "doc_length", "query_length"]


    Data_Set=Utilities.load_dict("runtime_cache/Data_Set_dict")

    test_queries = [63, 54, 57, 56, 58]
    train_set_path = "runtime_cache/train_split1.csv"
    test_set_path = "runtime_cache/test_split1.csv"
    split_data_set(Data_Set, field_header, train_set_path, test_set_path, test_queries)

    test_queries = [56, 57, 64, 71, 99]
    train_set_path = "runtime_cache/train_split2.csv"
    test_set_path = "runtime_cache/test_split2.csv"
    split_data_set(Data_Set, field_header, train_set_path, test_set_path, test_queries)

    test_queries = [94,95,97,99,100]
    train_set_path = "runtime_cache/train_split3.csv"
    test_set_path = "runtime_cache/test_split3.csv"
    split_data_set(Data_Set, field_header, train_set_path, test_set_path, test_queries)