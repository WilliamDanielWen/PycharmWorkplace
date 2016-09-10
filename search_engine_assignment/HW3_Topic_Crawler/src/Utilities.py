class RequestURLInfo(object):
    def __init__(self, request_url, requestUrl_wave,domain):
        self.request_url = request_url
        self.requestUrl_wave=requestUrl_wave
        self.domain=domain

    def decodeInfo(self):
        return self.request_url, self.requestUrl_wave,self.domain


class OutlinkURLInfo(object):
    def __init__(self, outlink, outlink_wave, score):
        self.outlink=outlink
        self.outlink_wave = outlink_wave
        self.score=score

    def decodeInfo(self):
        return self.outlink, self.outlink_wave, self.score

from elasticsearch import Elasticsearch
daniel_index=Elasticsearch(timeout=100)
daniel_index_name = 'daniel_test'
def create_daniel_index():
    daniel_index.cluster.health(wait_for_status='yellow', request_timeout=5)
    daniel_index.indices.delete(index=daniel_index_name, ignore= 404)
    # create empty index
    daniel_index.indices.create(
        index=daniel_index_name,
        body={
            'settings': {
                "index": {
                    "store": {
                        "type": "default"
                    },
                    "number_of_shards": 1,
                    "number_of_replicas": 1
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

    daniel_index.indices.put_mapping(
        index=daniel_index_name,
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
                    "title": {
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
                        "type": "string",
                        "store": True,
                        "index": "no"
                    },
                    "in_links": {
                        "type": "string",
                        "store": True,
                        "index": "no"
                    },
                    "out_links": {
                        "type": "string",
                        "store": True,
                        "index": "no"
                    },
                    "author": {
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





class ParserTarget(object):

    def __init__(self, base_url):
        self.base_url = base_url

        self.in_body = False
        self.clean_once = False
        self.is_title = False

        self.text_lines = []
        self.title = ''
        self.links = []

    def start(self, tag, attribute):
        if tag == 'body':
            self.in_body = True
        if self.in_body:
            self.clean_once = not (tag == 'link' or tag == 'script' or tag == 'style')
        if tag == 'title':
            self.is_title = True
        if self.in_body and tag == 'a' and attribute.has_key('href') and len(attribute['href']) > 3:
            result=canonicalize_url(self.base_url, attribute['href'])
            if result:
                self.links.append(result)

    def end(self, tag):
        if tag == 'body':
            self.in_body = False

    def data(self, data):
        d = data.strip()
        if self.is_title and d:
            self.title = d
            self.is_title = False
        if self.clean_once and d:
            self.text_lines.append(d)

    def comment(self, text):
        pass

    def close(self):
        pass


from urlparse import urlparse as up
import re
def get_host(url):
    authority_regex = re.compile('^(?:([^\@]+)\@)?([^\:]+)(?:\:(.+))?$')
    authority = up(url).netloc
    host = authority_regex.match(authority).groups()[1]
    host=str(host)
    return host


import urlparse
import urlnorm
def canonicalize_url(inlink, url):
    # deal with relative outlinks
    hostAdded_Links = None

    if url == None:
        return None
    if url.startswith('http://') or url.startswith('https://'):
        hostAdded_Links=url

    if url.startswith('../') or url.startswith('./'):
        hostAdded_Links=inlink.rstrip('/') + '/' + url

    if url.startswith('/') or re.match('([0-9A-Za-z]+\.)+[0-9A-Za-z]+', url) != None:
        hostAdded_Links=urlparse.urljoin(inlink, url)


    if not hostAdded_Links:
        return None

    try:
        hostAdded_Links = hostAdded_Links.encode(encoding='utf-8', errors='replace')
        hostAdded_Links = urlnorm.norm(hostAdded_Links)
        result = hostAdded_Links.split('#')[0]
        return result
    except Exception, e:
        print 'Crawler exception:  canonicalize exception : ', e.message, ' Ignore ', url
        return None




from multiprocessing.managers import BaseManager
from Queue import PriorityQueue
class PriorityQueueManager(BaseManager):
    pass
PriorityQueueManager.register("MultiProcessPriorityQueue", PriorityQueue)



