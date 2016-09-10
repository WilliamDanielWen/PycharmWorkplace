import re
import string
from urlparse import urlparse, urlunparse
from urllib import unquote
from string import *
class Canonicalizer(object):

    _collapse = re.compile('([^/]+/\.\./?|/\./|//|/\.$|/\.\.$)')
    _server_authority = re.compile('^(?:([^\@]+)\@)?([^\:]+)(?:\:(.+))?$')
    _default_port = {'http': '80',
                     'https': '443',
                     'gopher': '70',
                     'news': '119',
                     'snews': '563',
                     'nntp': '119',
                     'snntp': '563',
                     'ftp': '21',
                     'telnet': '23',
                     'prospero': '191',
                     }
    _relative_schemes = ['http', 'https', 'news', 'snews', 'nntp', 'snntp', 'ftp', 'file', '']

    _server_authority_schemes = ['http', 'https', 'news', 'snews', 'ftp']

    def __init__(self, url):
        self.parent_url = url

    def norms(self, urlstring):
        """
        given a string URL, return its normalised form
        """
        urlstring = string.strip(urlstring)
        return urlunparse(self.norm(urlparse(urlstring)))

    def norm(self, urltuple):
        """
        given a six-tuple URL, return its normalised form
        """
        (scheme, authority, path, parameters, query, fragment) = urltuple
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

def canoicalizer__test1():

    url1 = 'HTTP://www.Example.com/SomeFile.html'

    url2 = 'http://www.example.com:80/SomeFile.html'

    url3 = '../c.html'

    url4 = 'http://www.example.com/a.html#anything'

    url5 = 'http://www.example.com//a.html'

    url6 = 'http://www.example.com/a/b/../c.html'

    url7 = '/topic/history.html'

    url8 = '/h2'

    url9 = '#'

    url10 = ''

    can = Canonicalizer('http://www.example.com/a/b.html')
    print "test1"
    print url1,'url1 ',can.norms(url1)
    print url2,'url2 ',can.norms(url2)
    print url3,'url3 ',can.norms(url3)
    print url4,'url4 ',can.norms(url4)
    print url5,'url5 ',can.norms(url5)
    print url6,'url6 ',can.norms(url6)
    print url7,'url7 ',can.norms(url7)
    print url8,'url8 ',can.norms(url8)
    print url9,'url9 ',can.norms(url9)
    print url10,'url10 ',can.norms(url10)


#from Utilities import canonicalize_url
def canco_test():
    url1 = 'HTTTP://www.Example.com/SomeFile.html'

    url2 = 'http://www.example.com:80/SomeFile.html'

    url3 = '../c.html'

    url4 = 'http://www.example.com/a.html#anything'

    url5 = 'http://www.example.com//a.html'

    url6 = 'http://www.example.com/a/b/../c.html'

    url7 = '/topic/history.html'

    url8 = '/h2'

    url9 = '#'

    url10 = ''

    base="http://www.example.com"
    print "test2"
    print url1,' to ', canonicalize_url(url1,url1)
    print url2,' to ', canonicalize_url(url1,url2)
    print url3,' to ', canonicalize_url(url1,url3)
    print url4,' to ', canonicalize_url(url1,url4)
    print url5,' to ', canonicalize_url(url1,url5)
    print url6,' to ', canonicalize_url(url1,url6)
    print url7,' to ', canonicalize_url(url1,url7)
    print url8,' to ', canonicalize_url(url1,url8)
    print url9,' to ', canonicalize_url(url1,url9)
    print url10,' to ', canonicalize_url(url1,url10)
    print "rstrip",url3.strip('/')

canoicalizer__test1()
