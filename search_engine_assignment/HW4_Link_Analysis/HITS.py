

import os
import time
from Utilities import get_total_document_length,load_dict,Okapi_BM25
from collections import OrderedDict
from nltk import PorterStemmer
from Utilities import stemming_preprocess
# Create a root set: Obtain the root set of about 1000 documents by ranking all pages using BM25
def get_root_set():

    print" getting root set by using okapi bm25 ..."
    query = [
        "maritime", "marine", "ocean"
        , "accident", "disaster", "tragedy"
        , "iceberg","crash"
        , "lampedusa", "migrant", "shipwreck"
        , "cruise", "sail", "cargo", "boat"
        , "sink", "sank", "sunk"
        , "dead", "casualty", "injury"
    ]
    print "query length: ",len(query)
    print "original query: ",query
    stemmer = PorterStemmer()
    query=stemming_preprocess(query,stemmer)
    start_time=time.time()

    DOC_LENGTH_DICT = load_dict('DOCUMENT_LENGTH_DICT.cpkl')
    TOTAL_DOC_LENGTH = get_total_document_length(DOC_LENGTH_DICT)

    AVG_DOC_LENGTH = TOTAL_DOC_LENGTH / len(DOC_LENGTH_DICT)

    # calculate the score list according to retrieval model and store it
    search_results = Okapi_BM25(query,DOC_LENGTH_DICT,AVG_DOC_LENGTH)

    # output the top results
    root_set=OrderedDict()
    count = 1
    for url in sorted(search_results, key=search_results.get, reverse=True):
        root_set[url]=search_results[url]
        count += 1
        if count > 1000:
            break

    end_time=time.time()

    print "time usage of query : ", end_time-start_time, " seconds"
    return root_set

import random
def get_base_set_by_expansion_bak(root_set,d):
    print "expand root set ...."
    team1526_outlinks_dict = load_dict('team1526_outlinks_new.cpkl')
    team1526_inlinks_dict = load_dict('team1526_inlinks_new.cpkl')

    #
    base_set=root_set.keys()

    # Repeat few two or three time this expansion to get a base set of about 10,000 pages
    while len(base_set)<10000:


        for url in base_set:
            # For each page in the set, add all pages that the page points to
            base_set =list(set(base_set+ team1526_outlinks_dict[url]))


            #For each page in the set, obtain a set of pages that pointing to the page
            if len(team1526_inlinks_dict[url])<=d:
                base_set = list(set(base_set + team1526_inlinks_dict[url]))
            else:
                selected_inlinks = random.sample(team1526_inlinks_dict[url],d)
                base_set = list(set(base_set + selected_inlinks))


    print "expansion finished, get sub graph ..."
    base_set_inlink_dict = dict()
    base_set_outlink_dict = dict()

    print "initilizing base set ...."
    for url in base_set:
        base_set_inlink_dict[url]=[]
        base_set_outlink_dict[url]=[]

    print "filtering inlinks and outlinks for base set urls ......."
    count=0
    start_time=time.time()
    for url in base_set:
        outlinks=team1526_outlinks_dict[url]
        for outlink in outlinks:
            if outlink in base_set:
                base_set_outlink_dict[url].append(outlink)

        inlinks = team1526_inlinks_dict[url]
        for inlink in inlinks:
            if inlink in base_set:
                base_set_inlink_dict[url].append(inlink)
        print count,"base set urls processed in",time.time()-start_time,"seconds"

        count +=1

    return base_set,base_set_inlink_dict,base_set_outlink_dict

import random
def get_base_set(root_set, d):
    print "expand root set ...."
    team1526_outlinks_dict = load_dict('team1526_outlinks_new.cpkl')
    team1526_inlinks_dict = load_dict('team1526_inlinks_new.cpkl')

    base_set=root_set

    iteration=1
    print " Iterate to expand the base set ..."
    print "base set size:", len(base_set)

    augment_outlinks = OrderedDict()
    augment_inlinks = OrderedDict()

    while True:
        print " iteration",iteration,"begins ..."

        for url in base_set:
            # For each page in the set, add all pages that the page points to
            new_outlinks=team1526_outlinks_dict[url]

            for new_outlink in new_outlinks:
                if(not base_set.has_key(new_outlink))\
                    and(not augment_outlinks.has_key(new_outlink))\
                    and(not augment_inlinks.has_key(new_outlink)):
                        augment_outlinks[new_outlink]=0-iteration



            #For each page in the set, obtain a set of pages that pointing to the page
            if len(team1526_inlinks_dict[url])<=d:
                new_inlinks=team1526_inlinks_dict[url]
                for new_inlink in new_inlinks:
                    if(not base_set.has_key(new_inlink))\
                    and(not augment_outlinks.has_key(new_inlink))\
                    and(not augment_inlinks.has_key(new_inlink)):
                            augment_inlinks[new_inlink]=0-iteration
            else:
                selected_inlinks = random.sample(team1526_inlinks_dict[url],d)
                for selected_inlink in selected_inlinks:
                    if(not base_set.has_key(selected_inlink))\
                    and(not augment_outlinks.has_key(selected_inlink))\
                    and(not augment_inlinks.has_key(selected_inlink)):
                            augment_inlinks[selected_inlink] = 0-iteration


        print "base set size:",len(base_set)
        print "augment_outlinks size:",len(augment_outlinks),"augment_inlinks size:",len(augment_inlinks)

        if (len(base_set)+len(augment_outlinks)+len(augment_inlinks))>10000:
            base_set.update(augment_outlinks)
            base_set.update(augment_inlinks)
            break
        else:
            iteration+=1

    print "new base set size: ",len(base_set)
    print "expansion finished !  "
    print ""


    print "getting sub graph (inlink and outlink dict for base set)..."
    base_set_inlink_dict = dict()
    base_set_outlink_dict = dict()



    print "initilizing base set inlink and outlink dict ...."
    for url in base_set:
        base_set_inlink_dict[url]=[]
        base_set_outlink_dict[url]=[]

    print "filtering inlinks and outlinks for base set urls ......."
    count=0
    start_time=time.time()
    for url in base_set:
        outlinks=team1526_outlinks_dict[url]
        for outlink in outlinks:
            if base_set.has_key(outlink):
                base_set_outlink_dict[url].append(outlink)

        inlinks = team1526_inlinks_dict[url]
        for inlink in inlinks:
            if base_set.has_key(inlink):
                base_set_inlink_dict[url].append(inlink)

        #print count,"base set urls processed in",time.time()-start_time,"seconds"

        count +=1

    return base_set,base_set_inlink_dict,base_set_outlink_dict


from Utilities import normalize_vector,get_L1_error,output_top_scored_url
def compute_HITS(base_set,base_set_inlink_dict,base_set_outlink_dict,precision):
    print "compute HITS ..."
    h=dict()
    a=dict()

    print "initialize hub and authority score ...."
    for url in base_set:
        h[url]=1
        a[url]=1

    iteration = 1
    start_time = time.time()
    while True:
        h_new=dict()
        a_new=dict()
        for url in base_set:

            inlinks=base_set_inlink_dict[url]
            # update authority score as  the sum of the hub score of each page that points to it
            hub_sum = 0
            for inlink in inlinks:
                hub_sum+= h[inlink]
            a_new[url]=hub_sum

            # update hub score as the sum of the authority score of each page that it is pointing to
            outlinks=base_set_outlink_dict[url]
            authority_sum=0
            for outlink in outlinks:
                authority_sum+=a[outlink]
            h_new[url] =authority_sum

        #
        a_new = normalize_vector(a_new)
        h_new = normalize_vector(h_new)

        # check converge
        auth_error = get_L1_error(a_new, a)
        hub_error = get_L1_error(h_new,h)
        print "Iteration ", iteration, " hub-L1-error: ", hub_error, " auth-L1-error: ", auth_error, " ,time used :", time.time() - start_time, " seconds"
        if auth_error < precision and hub_error<precision:
            print "Iteration finished !"
            return a,h

        iteration +=1
        h = h_new
        a = a_new


from Utilities import dump_dict
from Utilities import rootset_info
import sys
if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # takes about 10 minutes to run
    #root_set=get_root_set()
    #dump_dict("root_set.cpkl",root_set)

    root_set=load_dict("root_set.cpkl")
    d=50
    base_set, base_set_inlink_dict, base_set_outlink_dict=get_base_set(root_set, d)
    precision=10**-14
    a,h=compute_HITS(base_set, base_set_inlink_dict, base_set_outlink_dict,precision)

    print "Getting sum of all authority score..."
    print "Length of PR :", len(a)
    sum = 0
    for url in a:
        sum += a[url]*a[url]
    print "Sum: ", sum

    print "Getting sum of all hub score..."
    print "Length of PR :", len(h)
    sum = 0
    for url in h:
        sum += h[url]*h[url]
    print "Sum: ", sum


    top_num=500
    output_top_scored_url("HITS_result_top500_authorities", a, top_num)
    output_top_scored_url("HITS_result_top500_hub", h, top_num)




