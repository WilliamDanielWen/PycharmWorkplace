from elasticsearch import Elasticsearch
es_client = Elasticsearch()


def create_team_index(index_name):
    # create empty index
    es_client.indices.delete(index=index_name, ignore=404)
    es_client.indices.create(
        index=index_name,
        body={
            'settings': {
                "index": {
                    "store": {
                        "type": "default"
                    },
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                # custom analyzer for analyzing file paths
                'analysis': {
                    "analyzer": {
                        "my_english": {
                            "type": "english",
                            "stopwords_path": "stoplist.txt"
                        }
                    }
                }
            }
        }

    )

    es_client.indices.put_mapping(
        index=index_name,
        doc_type='document',
        body={
          "document": {
            "properties": {
              "docno": {
                "type": "string",
                "store": True,
                "index": "analyzed",
                "term_vector": "with_positions_offsets_payloads"
              },
              "HTTPheader": {
                "type": "string",
                "store": True,
                "index": "not_analyzed"
              },
              "title":{
                "type": "string",
                "store": True,
                "index": "analyzed",
                "term_vector": "with_positions_offsets_payloads"
              },
              "text": {
                "type": "string",
                "store": True,
                "index": "analyzed",
                "term_vector": "with_positions_offsets_payloads"
              },
              "html_Source": {
                "type":"string",
                "store": True,
                "index": "no"
              },
              "in_links":{
                "type": "string",
                "store": True,
                "index": "no"
              },
              "out_links":{
                "type": "string",
                "store": True,
                "index": "no"
              },
              "author":{
                "type": "string",
                "store": True,
                "index": "analyzed"
              },
              "depth": {
                "type": "integer",
                "store": True,
                "index": "not_analyzed"
              },
              "url": {
                "type": "string",
                "store": True,
                "index": "not_analyzed"
              }
            }
          }
        }
    )


if __name__=="__main__":

    index_name = 'daniel_test'
    create_team_index(index_name)