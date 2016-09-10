import sys
from collections import defaultdict
from collections import OrderedDict
import math

K = [5,10,15,20,30,100,200,500,1000]

# no command mode
slash_q_mode = True
qrel_lists_path = "qrels.adhoc.51-100.AP89.txt"
top_k_ranked_lists_path = "TF_IDF.txt"



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


#read qrel file
qrel_file = open(qrel_lists_path, 'r')
QREL_Lists = defaultdict(dict)
Num_Relevant_Docs_inQREL = defaultdict(int)

while True:
    line = qrel_file.readline().strip()
    if line == '':
        break
    query_id, author, doc_id, true_score = line.split(" ")

    query_id=query_id.strip()
    doc_id=doc_id.strip()
    true_score=int(true_score.strip())

    QREL_Lists[query_id][doc_id] = true_score

    if true_score > 0:
        Num_Relevant_Docs_inQREL[query_id] += 1




#read top kranked lists file
top_k_ranked_lists_file = open(top_k_ranked_lists_path, 'r')
Top_K_Ranked_Lists = defaultdict(list)
query_ids = set()
num_total_docs_retrieved = 0
while True:

    line = top_k_ranked_lists_file.readline().strip()
    if line == '':
        break

    query_id, author, doc_id, rank_num, ranked_score, exp = line.split(" ")
    query_id=query_id.strip()
    doc_id=doc_id.strip()
    num_total_docs_retrieved += 1
    Top_K_Ranked_Lists[query_id].append(doc_id)
    query_ids.add(query_id)



# calculate evaluation information
R_Precision = dict()
Avg_Precision = dict()
nDCG = dict()
Precision_at_K = defaultdict(OrderedDict)
Recall_at_K = defaultdict(OrderedDict)
F1_at_K = defaultdict(OrderedDict)

Precision_Recall_Plot = defaultdict(OrderedDict)
Num_Relevant_Docs_Retrieved = dict()


for query_id in Top_K_Ranked_Lists:

    if not (query_id in QREL_Lists):
        print "Exception! query id\"", query_id,"\" not found in qrel file, ignore this query and continue to process other query..."
        continue

    #initilize
    R_Precision[query_id] = 0
    Avg_Precision[query_id] = 0
    nDCG[query_id] = 0
    Precision_Recall_Plot[query_id][0] = 1
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


        if true_score > 0:
            # retrived doc id is in Qrel and is relevant
            tp += 1
            Avg_Precision[query_id] += float(tp)/ k

        precision_at_k = float(tp) / k
        recall_at_k = float(tp) / Num_Relevant_Docs_inQREL[query_id]

        if precision_at_k == recall_at_k and precision_at_k != 0:
            R_Precision[query_id] = precision_at_k

        nDCG[query_id] += float((pow(2, int(true_score)) - 1)) / math.log(1 + k, 2)



        if k in K:
            Precision_at_K[query_id][k] = precision_at_k
            Recall_at_K[query_id][k] = recall_at_k

            sum_f1_at_k = 0
            if tp > 0:
                sum_f1_at_k = float(precision_at_k * recall_at_k * 2) / (precision_at_k + recall_at_k)
            F1_at_K[query_id][k] = sum_f1_at_k

        if precision_at_k != 0:
            Precision_Recall_Plot[query_id][recall_at_k] = precision_at_k


    Num_Relevant_Docs_Retrieved[query_id] = tp

    Avg_Precision[query_id] /= Num_Relevant_Docs_inQREL[query_id]



# print "-q" mode information
if slash_q_mode:
    print "#################### Individually Query Information ################## "
    print ""
    for query_id in query_ids:
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





#print overall information
print "#################### Overall Queries Information ################## "
print '*******************   Query num:       {}  ********************'.format(len(Top_K_Ranked_Lists))
print "Total number of documents over all queries:"
print '     Retrieved:          {}'.format(num_total_docs_retrieved)
print '     Relevant:           {}'.format(sum(Num_Relevant_Docs_inQREL.values()))
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
    Avg_F1_at_K[k] = float(sum_f1_at_k) / len(F1_at_K)



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



#output precision recall curve
for query_id in Precision_Recall_Plot:
    # print qid
    temp_max_val = 0
    Non_Increasing_Plot = OrderedDict()
    out_file = open('precision_recall_plot_files/query_'+query_id+'plot.csv', 'w')
    Items=Precision_Recall_Plot[query_id].items()
    Reversed_Items=reversed(Items)
    for recall, precision in reversed(Precision_Recall_Plot[query_id].items()):
        temp_max_val = max(temp_max_val, precision)
        Non_Increasing_Plot[recall] = temp_max_val


    out_file.write('recall,precision\n')
    for recall, precision in reversed(Non_Increasing_Plot.items()):
        out_file.write('{},{}\n'.format(recall, precision))
    out_file.close()
