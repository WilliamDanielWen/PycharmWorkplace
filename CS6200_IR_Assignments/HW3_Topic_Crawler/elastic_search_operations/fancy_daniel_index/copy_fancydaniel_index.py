from reverse_fancyDaniel_outlinks_into_inlinks import load_outlink_dict
from elasticsearch import Elasticsearch

def copy_index(source_index_name,bakcup_index_name):
    outlink_dict=load_outlink_dict()
    es_client=Elasticsearch()

    counter = 0
    for stored_url in outlink_dict:
        result = es_client.search(
            index=source_index_name,
            body={
                'query': {
                    'filtered': {
                        'query': {
                            "match_all": {}
                        },
                        'filter': {
                            "ids": {
                                "values": [stored_url]
                            }
                        }
                    }
                }
            }
        )

        source = result['hits']['hits'][0]['_source']

        doc = dict(docno=source['docno']
                   , HTTPheader=source['HTTPheader']
                   , title=source['title']
                   , text=source['text']
                   , html_Source=source['html_Source']
                   , in_links=source['in_links']
                   , out_links=source['out_links']
                   , author=source['author']
                   , depth=source['depth']
                   , url=source['url'])

        status = es_client.index(index=bakcup_index_name, doc_type='document', id=stored_url, body=doc)

        if not status['created']:
            print 'backup_error, id: ',stored_url
        else:
            counter += 1

        if counter % 500 == 0:
            print counter, ' pages copied ...'

if __name__=="__main__":

    source_index_name = "fancydanielindex"
    bakcup_index_name = "team_1526"
    copy_index(source_index_name,bakcup_index_name)