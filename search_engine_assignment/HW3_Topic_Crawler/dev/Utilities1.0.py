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





class Parser(object):

    def __init__(self, base_url):

        self.in_body = False
        self.clean_once = False
        self.is_title = False
        self.text_lines = []
        self.title = ''
        self.links = []
        self.cano=Canonicalizer(base_url)
    def start(self, tag, attribute):
        if tag == 'body':
            self.in_body = True
        if self.in_body:
            self.clean_once = not (tag == 'link' or tag == 'script' or tag == 'style')
        if tag == 'title':
            self.is_title = True
        if self.in_body and tag == 'a' and attribute.has_key('href') and len(attribute['href']) > 3:
            #self.links.append(self.canon.norms(attribute['href']))
            self.links.append(self.cano.canonicalize_url(attribute['href']))

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



import re
import string
from urlparse import urlparse, urlunparse
from urllib import unquote
from string import *
class Canonicalizer(object):

    _collapse = re.compile('([^/]+/\.\./?|/\./|//|/\.$|/\.\.$)')
    _server_authority = re.compile('^(?:([^\@]+)\@)?([^\:]+)(?:\:(.+))?$')
    _default_port = {'http': '80','https': '443',}

    _relative_schemes = ['http', 'https','']

    _server_authority_schemes = ['http', 'https', 'news', 'snews', 'ftp']

    def __init__(self, url):
        self.parent_url = url

    def canonicalize_url(self, urlstring):

        urlstring = string.strip(urlstring)
        return urlunparse(self.norm(urlparse(urlstring)))

    def norm(self, url_components):

        (scheme, authority, path, parameters, query, fragment) = url_components
        if scheme == '':
            scheme = 'http'
        scheme = lower(scheme)

        if authority:
            userinfo, host, port = self._server_authority.match(authority).groups()
            if host[-1] == '.':
                host = host[:-1]
            authority = lower(host)
            if userinfo:
                authority = "%s@%s" % (userinfo, authority)
            if port and port != self._default_port.get(scheme, None):
                authority = "%s:%s" % (authority, port)

        if scheme in self._relative_schemes:
            last_path = path
            while 1:
                path = self._collapse.sub('/', path, 1)
                if last_path == path:
                    break
                last_path = path

        if authority == '':
            p_tuple = urlparse(self.parent_url)
            if '../' in path:
                tails = split(p_tuple.path, '/')
                try:
                    del tails[-1]
                    del tails[-1]
                except IndexError:
                    print ('absolute path transform failed for parent:{} and {}'.format(p_tuple.path, path))
                path = '/'.join(tails) + path.replace('../', '')
            scheme = p_tuple.scheme
            authority = p_tuple.netloc

        path = unquote(path)
        return scheme, authority, path, parameters, query, ''



from multiprocessing.managers import BaseManager
from Queue import PriorityQueue
class PriorityQueueManager(BaseManager):
    pass
PriorityQueueManager.register("MultiProcessPriorityQueue", PriorityQueue)



