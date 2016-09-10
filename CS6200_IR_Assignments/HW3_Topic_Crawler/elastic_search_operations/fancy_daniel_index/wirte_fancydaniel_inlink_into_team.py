from reverse_fancyDaniel_outlinks_into_inlinks import  load_outlink_dict, load_inlink_dict
from elasticsearch import Elasticsearch

import time
def write_inlinks( index_name, inlink_dict, outlink_dict):
  index_client=Elasticsearch()
  start_time=time.time()
  print "Writing inlinks into ", index_name
  count=0
  for stored_url in outlink_dict:
    if inlink_dict.has_key(stored_url):
      index_client.update(index=index_name
                          , doc_type='document'
                          , id=stored_url
                          , body={
                                    'doc':{
                                        'in_links': inlink_dict[stored_url]
                                    }

                            }
                          )

      count += 1
      if count%50==0:
        time_used = time.time() - start_time
        print count, ' pages updated in ', time_used, ' seconds ...'

  print 'Updating finished!'




def print_statistics(inlink_dict,outlink_dict):
    print "Calculating statistics info ...."
    total_valid_inlink_counts=0
    num_nonEmptyInlink_pages=0

    for stored_url in outlink_dict:
        if inlink_dict.has_key(stored_url):
            num_nonEmptyInlink_pages+=1
            total_valid_inlink_counts+=len(inlink_dict[stored_url])


    num_total_pages=len(outlink_dict)
    num_emptyInlink_pages = num_total_pages - num_nonEmptyInlink_pages

    average_inlinks_per_nonEmpty_page=total_valid_inlink_counts*1.0/num_nonEmptyInlink_pages
    average_inlinks_per_page=total_valid_inlink_counts*1.0/num_total_pages

    print "num_total_pages: ",num_total_pages
    print "num_nonEmptyInlink_pages: ",num_nonEmptyInlink_pages
    print "num_emptyInlink_pages: ",num_emptyInlink_pages

    print "",
    print "total_valid_inlink_counts: ",total_valid_inlink_counts
    print "average_inlinks_per_nonEmpty_page: ",average_inlinks_per_nonEmpty_page
    print "average_inlinks_per_page: ",average_inlinks_per_page

if __name__=="__main__":
    inlink_dict=load_inlink_dict()
    outlink_dict=load_outlink_dict()
    print_statistics(inlink_dict,outlink_dict)

