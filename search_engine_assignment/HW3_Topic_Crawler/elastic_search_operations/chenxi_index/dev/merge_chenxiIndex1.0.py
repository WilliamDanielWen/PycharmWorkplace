# -*- coding: UTF-8 -*-
from elasticsearch.helpers import bulk, scan
from elasticsearch import Elasticsearch, TransportError
import sys
import time

def update_doc(_es_instance, _my_index, _my_type, _docno, change_dict):
	action = {
		'_op_type': 'update',
		'_index': _my_index,
		'_type': _my_type,
		'_id': _docno,
		'doc': change_dict
	}
	try:
		bulk(_es_instance, [action])
	except TransportError as e:
		print(e)
	except:
		pass

def write_new_data(_es_instance, _my_index, _my_type, _source, _docno):
	action = {
		'_index': _my_index,
		'_type': _my_type,
		'_source': _source,
		'_id': _docno
	}
	bulk(_es_instance, [action])


def merge(_es_instance, _my_index, _target_es, _target_index, _my_type):
	count = 0
	time_start=time.time()
	for _m in scan(_es_instance, index=_my_index, doc_type=_my_type,
				   query={"query": {"match_all": {}}}):
		_target = _target_es.search(index=_target_index,
									  doc_type=_my_type,
									  body={"query": {"match": {"_id": _m['_id']}}},
									  request_timeout=30)

		count += 1
		time_used=time.time()-time_start
		print('{} pages stored in {} seconds  {}'.format(count,time_used, _m['_id']))
		if _target['hits']['hits']:
			_target_rec = _target['hits']['hits'][0]
			c = {#"docno": _m['_source']['docno'],
				 #"HTTPheader": _m['_source']['HTTPheader'],
				 #"title": _m['_source']['title'],
				 #"text": _m['_source']['text'],
				 #"html_Source": _m['_source']['html_Source'],
                 #"in_links": list(set(_m['_source']['in_links'].split('\n') + _target_rec['_source']['in_links'])),
				 "out_links": list(set(_m['_source']['out_links'].split('\n') + _target_rec['_source']['out_links'])),
				 "author": _m['_source']['author'] + ' ' + _target_rec['_source']['author']
				 #,"depth": _m['_source']['depth'],
				 #"url": _m['_source']['url']
            }
			update_doc(_target_es, _target_index, _my_type, _m['_id'], c)

		else:
			c = {
				"docno": _m['_source']['docno'],
				"HTTPheader": _m['_source']['HTTPheader'],
				"title": _m['_source']['title'],
				"text": _m['_source']['text'],
				"html_Source": _m['_source']['html_Source'],
				"in_links": list(set(_m['_source']['in_links'].split('\n'))),
				"out_links": list(set(_m['_source']['out_links'].split('\n'))),
				"author": _m['_source']['author'],
				"depth": _m['_source']['depth'],
				"url": _m['_source']['url']
			}
			write_new_data(_target_es, _target_index, _my_type, c, _m['_id'])



if __name__=="__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	es_instance=Elasticsearch(["http://104.196.117.30:9200"])
	my_index="maritimeaccidents"
	target_es = Elasticsearch()
	target_index="marritiemaccidents"
	my_type="document"
	merge(es_instance,my_index,target_es,target_index,my_type)