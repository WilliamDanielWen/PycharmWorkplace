from elasticsearch import  Elasticsearch
es_client=Elasticsearch()
es_client.indices.delete(index="marritiemaccidents", ignore=404)