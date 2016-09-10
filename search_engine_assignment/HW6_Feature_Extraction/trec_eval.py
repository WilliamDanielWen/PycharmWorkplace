import sys
from collections import defaultdict
from collections import OrderedDict
import math



def read_qrel_file(qrel_lists_path):
    # read qrel file
    qrel_file = open(qrel_lists_path, 'r')
    QREL_Lists = defaultdict(dict)
    Num_Relevant_Docs_inQREL = defaultdict(int)

    while True:
        line = qrel_file.readline().strip()
        if line == '':
            break
        if qrel_lists_path=="sorted_avg_score.txt":
            query_id, author, doc_id, true_score = line.split("\t")
            query_id = query_id.strip()
            doc_id = doc_id.strip()
            true_score = int(float(true_score.strip()))

        else:
            query_id, author, doc_id, true_score = line.split(" ")
            query_id = query_id.strip()
            doc_id = doc_id.strip()
            true_score = int(true_score.strip())



        QREL_Lists[query_id][doc_id] = true_score

        if true_score >0:
            Num_Relevant_Docs_inQREL[query_id] += 1
        else:
            Num_Relevant_Docs_inQREL[query_id] += 0


    return QREL_Lists\
           ,Num_Relevant_Docs_inQREL


def read_top_k_ranked_lists_file(top_k_ranked_lists_path):
    top_k_ranked_lists_file = open(top_k_ranked_lists_path, 'r')
    Top_K_Ranked_Lists = defaultdict(list)
    query_ids = set()
    num_total_docs_retrieved = 0
    while True:

        line = top_k_ranked_lists_file.readline().strip()
        if line == '':
            break


        query_id, author, doc_id, rank_num, ranked_score, exp = line.strip().split()


        query_id=query_id.strip()
        doc_id=doc_id.strip()


        num_total_docs_retrieved += 1
        Top_K_Ranked_Lists[query_id].append(doc_id)
        query_ids.add(query_id)

    return Top_K_Ranked_Lists\
           ,num_total_docs_retrieved


def calculate_evaluation_information(Top_K_Ranked_Lists,QREL_Lists,Num_Relevant_Docs_inQREL):
    # calculate evaluation information
    R_Precision = dict()
    Avg_Precision = dict()
    nDCG = dict()
    DCG=dict()
    DCG_Ideal_List_Scores = dict()
    Precision_at_K = defaultdict(OrderedDict)
    Recall_at_K = defaultdict(OrderedDict)
    F1_at_K = defaultdict(OrderedDict)

    Precision_Recall_Plot = dict()
    Num_Relevant_Docs_Retrieved = dict()

    Ranked_List_with_TrueScore=dict()
    for query_id in Top_K_Ranked_Lists:
        Ranked_List_with_TrueScore[query_id]=dict()

        if not (query_id in QREL_Lists):
            print "Exception! query id\"", query_id, "\" not found in qrel file, ignore this query and continue to process other query..."
            continue

        # initilize
        R_Precision[query_id] = 0
        Avg_Precision[query_id] = 0
        nDCG[query_id] = 0
        DCG[query_id]=0
        Precision_Recall_Plot[query_id] = list()
        Precision_Recall_Plot[query_id].append((0.0, 1.0))
        tp = 0
        k = 0
        for doc_id in Top_K_Ranked_Lists[query_id]:
            k += 1

            if (doc_id in QREL_Lists[query_id]):
                # if doc_id is in Qrel, but it's irrelevant, the true score is  0
                true_score = QREL_Lists[query_id][doc_id]
            else:
                # if doc_id is not in Qrel, the true score is also 0
                true_score = 0

            Ranked_List_with_TrueScore[query_id][doc_id]=true_score


            if true_score > 0:
                # retrived doc id is in Qrel and is relevant
                tp += 1
                Avg_Precision[query_id] += float(tp) / k

            precision_at_k = float(tp) / k
            recall_at_k = float(tp) / Num_Relevant_Docs_inQREL[query_id]

            if precision_at_k == recall_at_k and precision_at_k != 0:
                R_Precision[query_id] = precision_at_k


            if k == 1:
                DCG[query_id] += true_score
            else :
                DCG[query_id]+=true_score / math.log(k, 2)

            if k in K:
                Precision_at_K[query_id][k] = precision_at_k
                Recall_at_K[query_id][k] = recall_at_k

                sum_f1_at_k = 0
                if tp > 0:
                    sum_f1_at_k = float(precision_at_k * recall_at_k * 2) / (precision_at_k + recall_at_k)
                F1_at_K[query_id][k] = sum_f1_at_k

            if precision_at_k != 0:
                Precision_Recall_Plot[query_id].append((recall_at_k, precision_at_k))

        DCG_Ideal_List_Scores[query_id]=1
        count=0
        for doc_id, true_score in sorted( Ranked_List_with_TrueScore[query_id].items(),key=lambda t: t[1], reverse= True):
        #for doc_id, true_score in QREL_Lists[query_id].items():
            count += 1
            if count == 1:
                DCG_Ideal_List_Scores[query_id] += true_score
            else:
                DCG_Ideal_List_Scores[query_id] += true_score / math.log(count, 2)

        nDCG[query_id] = DCG[query_id]/DCG_Ideal_List_Scores[query_id]
        Num_Relevant_Docs_Retrieved[query_id] = tp
        Avg_Precision[query_id] /= Num_Relevant_Docs_inQREL[query_id]


    return Num_Relevant_Docs_Retrieved,Avg_Precision\
    ,Precision_at_K\
    ,R_Precision,nDCG\
    ,Recall_at_K,F1_at_K\
    ,Precision_Recall_Plot\


def output_PrecisionRecallCurve_data_toFile(Precision_Recall_Plot):
    for query_id in Precision_Recall_Plot:

        Non_Increasing_Plot = list()
        out_file = open('precision_recall_original_data/query_' + query_id + '_original_plot.csv', 'w')
        out_file.write('recall,precision\n')
        for  recall,precision in Precision_Recall_Plot[query_id]:
            out_file.write('{},{}\n'.format(recall, precision))
        out_file.close()

def output_PrecisionRecallCurve_data_toFile_bak(Precision_Recall_Plot):
    for query_id in Precision_Recall_Plot:

        Non_Increasing_Plot = OrderedDict()
        min_precision_so_far = 1.0
        for  recall,precision in Precision_Recall_Plot[query_id]:
            min_precision_so_far = min(min_precision_so_far, precision)
            Non_Increasing_Plot[recall]=min_precision_so_far

        out_file = open('precision_recall_plot_data_non_increasing/query_' + query_id + '_plot.csv', 'w')
        out_file.write('recall,precision\n')
        for recall, precision in Non_Increasing_Plot.items():
            out_file.write('{},{}\n'.format(recall, precision))
        out_file.close()


def print_individual_query_information(Top_K_Ranked_Lists
                                       ,Num_Relevant_Docs_inQREL
                                       ,Num_Relevant_Docs_Retrieved
                                       ,Avg_Precision,Precision_at_K
                                       ,R_Precision
                                       ,nDCG
                                       ,Recall_at_K
                                       ,F1_at_K):

    print "#################### Individually Query Information ################## "
    print ""
    for query_id in Top_K_Ranked_Lists:
        print '*******************   Queryid:       {}  ********************'.format(query_id)

        print "Total number of documents over query:"
        print '     Retrieved:          {}'.format(len(Top_K_Ranked_Lists[query_id]))

        print '     Relevant:           {}'.format(Num_Relevant_Docs_inQREL[query_id])
        print '     Relevant_retrieved: {}'.format(Num_Relevant_Docs_Retrieved[query_id])
        print ''

        print 'Average precision : '
        print '     {}'.format(Avg_Precision[query_id])
        print ''

        print 'Precision:'
        for k, v in Precision_at_K[query_id].items():
            print '     At {} docs:     {}'.format(k, v)
        print ''

        print 'R-Precision :'
        print '     {}'.format(R_Precision[query_id])
        print ''

        print 'nDCG:'
        print '     {}'.format(nDCG[query_id])
        print ''

        print 'Recall:'
        for k, v in Recall_at_K[query_id].items():
            print '     At {} docs:     {}'.format(k, v)
        print ''

        print 'F1:'
        for k, v in F1_at_K[query_id].items():
            print '     At {} docs:     {}'.format(k, v)
        print ''
        print ''



def print_overall_queries_information(num_total_docs_retrieved
                                      ,num_total_relevant_docs
                                      ,Num_Relevant_Docs_Retrieved
                                      ,Avg_Precision
                                      ,nDCG
                                      ,R_Precision
                                      ,Precision_at_K
                                      ,Recall_at_K
                                      ,F1_at_K):
    print "#################### Overall Queries Information ################## "
    print '*******************   Query num:       {}  ********************'.format(len(Top_K_Ranked_Lists))
    print "Total number of documents over all queries:"
    print '     Retrieved:          {}'.format(num_total_docs_retrieved)
    print '     Relevant:           {}'.format(num_total_relevant_docs)
    print '     Relevant_retrieved: {}'.format(sum(Num_Relevant_Docs_Retrieved.values()))
    print ''

    avg_avg_precision = float(sum(Avg_Precision.values())) / len(Avg_Precision)
    avg_nDCG = float(sum(nDCG.values())) / len(nDCG)
    avg_r_precision = float(sum(R_Precision.values())) / len(R_Precision)


    Avg_Precision_at_K = dict()
    Avg_Recall_at_K = dict()
    Avg_F1_at_K = dict()

    for k in K:
        precision_at_k = 0
        recall_at_k = 0
        sum_f1_at_k = 0
        count =0
        for query_id in Precision_at_K:
            if Precision_at_K[query_id].has_key(k):
                precision_at_k += Precision_at_K[query_id][k]
                count +=1
        Avg_Precision_at_K[k] = float(precision_at_k) / count

        count = 0
        for query_id in Recall_at_K:
            if Recall_at_K[query_id].has_key(k):
                recall_at_k += Recall_at_K[query_id][k]
                count +=1
        Avg_Recall_at_K[k] = float(recall_at_k) / count

        count=0
        for query_id in F1_at_K:
            if F1_at_K[query_id].has_key(k):
                sum_f1_at_k += F1_at_K[query_id][k]
                count +=1
        Avg_F1_at_K[k] = float(sum_f1_at_k) / count



    print 'Average precision (average of Average_Precision of all queries): '
    print '     {}'.format(avg_avg_precision)
    print ''


    print 'Precision at K :'
    for k in K:
            print'     At {} docs (average of all queries):     {}'.format(k, Avg_Precision_at_K[k])
    print ''

    print 'R-Precision (average of all queries):'
    print '     {}'.format(avg_r_precision)
    print ''

    print 'nDCG (average of all queries):'
    print '     {}'.format(avg_nDCG)
    print ''



    print 'Recall at K :'
    for k in K:
        print '     At {} docs (average of all queries):     {}'.format(k, Avg_Recall_at_K[k])
    print ''


    print 'F1 at K :'
    for k in K: print '     At {} docs (average of all queries):     {}'.format(k, Avg_F1_at_K[k])
    print ''



if __name__=="__main__":


    K =[5,10,15,30,50,100,150,200]

    slash_q_mode = True

    qrel_lists_path = "runtime_cache/qrels.adhoc.51-100.AP89.txt"

    #Random Forest for test queries 1
    #top_k_ranked_lists_path = "runtime_cache/test_performance_random_forest_split1.txt"
    #top_k_ranked_lists_path = "runtime_cache/train_performance_random_forest_split1.txt"

    #SVM for test queries 3
    #top_k_ranked_lists_path = "runtime_cache/test_performance_SVM_split3.txt"
    #top_k_ranked_lists_path = "runtime_cache/train_performance_SVM_split3.txt"

    #SVM RANK  for test queries 3
    #top_k_ranked_lists_path = "runtime_cache/test_performance_SVM_Rank_split3.txt"

    top_k_ranked_lists_path = "runtime_cache/train_performance_SVM_Rank_split3.txt"


    # command mode
    # if len(sys.argv)!=3 and  len(sys.argv)!=4:
    #     print "usage: python trec_eval.py [-q] QREL_file_name  ranked_list_file_name"
    #     exit(0)
    #
    #
    # slash_q_mode=False
    # if len(sys.argv)==3:
    #     #read files
    #     qrel_lists_path = sys.argv[1]
    #     top_k_ranked_lists_path = sys.argv[2]
    # else:
    #     slash_q_mode = True
    #     qrel_lists_path = sys.argv[2]
    #     top_k_ranked_lists_path = sys.argv[3]



    print '#################### QREL file(true labels): {},       Ranked list file: {} #############'.format(qrel_lists_path, top_k_ranked_lists_path)
    print ''

    QREL_Lists\
    ,Num_Relevant_Docs_inQREL\
    =read_qrel_file(qrel_lists_path)

    Top_K_Ranked_Lists\
    ,num_total_docs_retrieved\
    =read_top_k_ranked_lists_file(top_k_ranked_lists_path)

    Num_Relevant_Docs_Retrieved,Avg_Precision\
    ,Precision_at_K\
    ,R_Precision,nDCG\
    ,Recall_at_K,F1_at_K\
    ,Precision_Recall_Plot\
    =calculate_evaluation_information(Top_K_Ranked_Lists, QREL_Lists, Num_Relevant_Docs_inQREL)

    #output_PrecisionRecallCurve_data_toFile(Precision_Recall_Plot)

    # print "-q" mode information
    if slash_q_mode:
        print_individual_query_information(Top_K_Ranked_Lists
                                           , Num_Relevant_Docs_inQREL
                                           , Num_Relevant_Docs_Retrieved
                                           , Avg_Precision, Precision_at_K
                                           , R_Precision
                                           , nDCG
                                           , Recall_at_K
                                           , F1_at_K)

    num_total_relevant_docs=0
    for query_id in  Top_K_Ranked_Lists:
            num_total_relevant_docs +=Num_Relevant_Docs_inQREL[query_id]

    print_overall_queries_information(num_total_docs_retrieved
                                      , num_total_relevant_docs
                                      , Num_Relevant_Docs_Retrieved
                                      , Avg_Precision
                                      , nDCG
                                      , R_Precision
                                      , Precision_at_K
                                      , Recall_at_K
                                      , F1_at_K)










