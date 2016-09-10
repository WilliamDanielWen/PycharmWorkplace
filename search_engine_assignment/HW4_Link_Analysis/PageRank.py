
def get_wt2g_info():
    print "load wt2g_inlinks"
    path = "wt2g_inlinks.txt"
    file=open(path,'r')

    outlink_dict=dict()
    inlink_dict = dict()

    count=0
    while True:
        line = file.readline().strip()
        if line=="":

            break

        line=line.split()

        url=line[0]
        inlinks=line[1:len(line)]

        if not inlink_dict.has_key(url):
            inlink_dict[url]=list(set(inlinks))
        else:
            inlink_dict[url]=list(set(inlink_dict[url]+inlinks))



        count +=1
        if count %10000==0:
            print count ,"  lines loaded "

    for url in inlink_dict:
        inlinks=inlink_dict[url]
        for inlink in inlinks:
            if outlink_dict.has_key(inlink):
                outlink_dict[inlink].append(url)
            else:
                outlink_dict[inlink] = []
                outlink_dict[inlink].append(url)


    print count, "  lines loaded "

    return inlink_dict,outlink_dict
import time
from Utilities import get_L1_error
def comput_pagerank(inlink_dict,outlink_dict,d,precision):
    print "calculating page rank ...."
    print "initialization ...."
    PR = dict()
    N = len(inlink_dict)
    for p in inlink_dict:
        PR[p]=1.0/N

    print "calculating the sink nodes set ..."
    S = dict()
    for p in inlink_dict:
        if not outlink_dict.has_key(p):
            S[p] = 1

    print "calculating page rank score by iteration"

    iteration=1
    start_time=time.time()
    while True:
        newPR = dict()
        sinkPR=0
        for p in S:
            sinkPR +=PR[p]
        for p in inlink_dict:
            newPR[p]=(1-d)/N + d*sinkPR/N
            for q in inlink_dict[p]:
                newPR[p] += d*PR[q]/len(outlink_dict[q])

        #check converge
        error=get_L1_error(newPR, PR)
        print "Iteration ",iteration," L1-error: ",error, " ,time used :", time.time()-start_time, " seconds"
        if error<precision:
            print "Iteration finished !"

            return newPR


        PR=newPR
        iteration+=1

from Utilities import output_top_scored_url
def compute_w2gTop500PageRank():
    inlink_dict, outlink_dict=get_wt2g_info()
    PR=comput_pagerank(inlink_dict, outlink_dict,0.85,10**-15)
    print "Getting sum of all pr..."
    print "Length of PR :", len(PR)
    sum=0
    for url in PR:
        sum+=PR[url]
    print "Sum: ",sum
    output_top_scored_url("PageRank_result_w2g", PR,500)



from Utilities import load_dict
def compute_team1526Top500PageRank():
    team_1526_inlink_dict=load_dict("team1526_inlinks_new.cpkl")
    team_1526_outlink_dict = load_dict("team1526_outlinks_new.cpkl")
    PR=comput_pagerank(team_1526_inlink_dict, team_1526_outlink_dict,0.85,10**-15)


    output_top_scored_url("PageRank_result_team1526", PR, 500)

if __name__=="__main__":
    compute_w2gTop500PageRank()
    # compute_team1526Top500PageRank()