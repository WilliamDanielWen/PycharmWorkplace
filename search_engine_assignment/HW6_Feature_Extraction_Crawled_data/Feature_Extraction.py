import Utilities

import time
def compute_IR_Scores(DOC_LENGTH_DICT,valid_queries, true_label_set):


    AVG_DOC_LENGTH = Utilities.get_avg_doc_length(DOC_LENGTH_DICT)
    D = len(DOC_LENGTH_DICT)
    # number of unique terms
    V = Utilities.get_unique_term_num()  # 178081


    IR_Models=[Utilities.Okapi_TF
                ,Utilities.TF_IDF
                ,Utilities.Okapi_BM25
                ,Utilities.Unigram_LM_Laplace_Smoothing
                ,Utilities.Unigram_LM_Jelinek_Mercer_Smoothing]

    IR_Scores = dict()


    for IR_model in IR_Models:

        print "Computing",IR_model.func_name, "score ...."

        query_count=0
        start_time=time.time()
        IR_Scores[IR_model.func_name] =dict()

        for query_id in valid_queries:
            time1=time.time()


            query=valid_queries[query_id]

            IR_Scores[IR_model.func_name][query_id]=IR_model(query,DOC_LENGTH_DICT,AVG_DOC_LENGTH,D,V)


            query_count += 1
            time2 = time.time()
            print "  ", query_count, " query processed, time usage of query[", query_id, "] : ", time2 - time1, " seconds"


        print "Computing",IR_model.func_name, "score finished, time usage:", time.time() - start_time, " seconds"
        print ""

    return  IR_Scores


def extract_static_features(DOC_LENGTH_DICT,valid_queries,true_label_set,avg_length):
    Static_Features=dict()

    feature_name="doc_length"
    Static_Features[feature_name]=dict()
    for query_id in true_label_set:
        Static_Features[feature_name][query_id]=dict()
        for doc_id in true_label_set[query_id]:
            if DOC_LENGTH_DICT.has_key(doc_id):
                Static_Features[feature_name][query_id][doc_id] = DOC_LENGTH_DICT[doc_id]
            else:
                Static_Features[feature_name][query_id][doc_id] = avg_length


    feature_name = "query_length"
    Static_Features[feature_name] = dict()
    for query_id in true_label_set:
        Static_Features[feature_name][query_id] = dict()

        query=valid_queries[query_id]
        query_length=len(query)

        for doc_id in true_label_set[query_id]:
            Static_Features[feature_name][query_id][doc_id] =query_length

    return Static_Features

def extract_static_features_bak(DOC_LENGTH_DICT,valid_queries,true_label_set):
    Static_Features=dict()

    feature_name="doc_length"
    Static_Features[feature_name]=dict()
    for query_id in true_label_set:
        Static_Features[feature_name][query_id]=dict()
        for doc_id in true_label_set[query_id]:
            Static_Features[feature_name][query_id][doc_id] = DOC_LENGTH_DICT[doc_id]




    feature_name = "query_length"
    Static_Features[feature_name] = dict()
    for query_id in true_label_set:
        Static_Features[feature_name][query_id] = dict()

        query=valid_queries[query_id]
        query_length=len(query)

        for doc_id in true_label_set[query_id]:
            Static_Features[feature_name][query_id][doc_id] =query_length

    return Static_Features


def construct_data_set(true_label_set, IR_Scores,Static_Features):
    print "Constructing data matrix ...."
    Data_Set=dict()

    #update true score
    for query_id in true_label_set:
        Data_Set[query_id]=dict()
        for doc_id in true_label_set[query_id]:
            Data_Set[query_id][doc_id]=dict()

            true_label=true_label_set[query_id][doc_id]
            Data_Set[query_id][doc_id]["label"]=true_label



    # update IR features
    for query_id in true_label_set:
        for doc_id in true_label_set[query_id]:

            for model_name in IR_Scores:
                if IR_Scores[model_name].has_key(query_id) and IR_Scores[model_name][query_id].has_key(doc_id):
                    Data_Set[query_id][doc_id][model_name] = IR_Scores[model_name][query_id][doc_id]
                else:
                    Data_Set[query_id][doc_id][model_name] = -1000000000

    # update static features
    for query_id in true_label_set:
        for doc_id in true_label_set[query_id]:
            for static_feature in Static_Features:
                    Data_Set[query_id][doc_id][static_feature] = Static_Features[static_feature][query_id][doc_id]


    return Data_Set


import os
def write_data_set(Data_Set,field_header,file_path):

    if os.path.exists(file_path):
        os.remove(file_path)
    print "Outputing data set to csv ..."
    file=open(file_path,"w")

    #write header
    file.write("query_id"+",doc_id")
    for field in field_header:
        file.write(","+field)
    file.write("\n")


    # update static features
    for query_id in Data_Set:

        for doc_id in Data_Set[query_id]:
            file.write(query_id+","+doc_id)
            for field in field_header:
                file.write(","+str(Data_Set[query_id][doc_id][field]))
            file.write("\n")



if __name__=="__main__":
    # step0
    DOC_LENGTH_DICT = Utilities.load_doc_length_info()
    valid_queries = Utilities.get_valid_queries()
    true_label_set=Utilities.extract_qrel_info(valid_queries)

    # step1
    IR_Scores=compute_IR_Scores(DOC_LENGTH_DICT,valid_queries, true_label_set)
    Utilities.dump_dict("runtime_cache/IR_Scores_dict",IR_Scores)

    # step1 quick alternative
    IR_Scores=Utilities.load_dict("runtime_cache/IR_Scores_dict")


    # step2
    avg_length=Utilities.get_avg_doc_length(DOC_LENGTH_DICT)
    Static_Features=extract_static_features(DOC_LENGTH_DICT,valid_queries,true_label_set,avg_length)
    #Static_Features = extract_static_features(DOC_LENGTH_DICT, valid_queries, true_label_set)


    # step3
    Data_Set=construct_data_set(true_label_set,IR_Scores,Static_Features)
    Utilities.dump_dict("runtime_cache/Data_Set_dict", Data_Set)

    # step3 quick alternative
    Data_Set=Utilities.load_dict("runtime_cache/Data_Set_dict")

    #step4
    field_header=["label","Okapi_TF","TF_IDF","Okapi_BM25","Unigram_LM_Laplace_Smoothing","Unigram_LM_Jelinek_Mercer_Smoothing","doc_length","query_length"]
    file_path="runtime_cache/data_set.csv"
    write_data_set(Data_Set,field_header,file_path)






