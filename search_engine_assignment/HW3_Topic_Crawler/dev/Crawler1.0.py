import sys
import string
import time
import re
import urllib2
from lxml import etree
from multiprocessing import Process,Semaphore
from multiprocessing import Manager
from Utilities import daniel_index,daniel_index_name
from Parser import Parser
from Utilities import OutlinkURLInfo
import urlnorm as UrlCleaner
import urlparse
class Crawler(object):


    def __init__(self
                 ,num_requestProcess
                 , target_num_pages
                 , requestTimeout
                 , requestQueue
                 , selectionQueue):
        self.request_queue = requestQueue
        self.selection_queue = selectionQueue
        self.author = 'Yu.Wen'
        self.num_page_to_store=target_num_pages
        self.semaphore_RequestQueue = Semaphore(num_requestProcess)
        self.num_stored_page = Manager().Value('l', 0)
        self.invalidWebsite_keyWords = ['video', 'youtube', 'instagram', 'tv',
                                        'amazon', 'ebay', 'photo', 'image', 'game', 'shop', 'foursquare']
                                        #, 'facebook', 'twitter'
        self.startSeconds=time.time()

    # keep creating deamon process spider_task, and put it into process_pool
    def crawl_requestLinks_byMultiprocess(self):

        while True:

            if self.num_stored_page.value > self.num_page_to_store:
                print '######### Crawler Exit #############: ', self.num_stored_page, ' page stored, crawl finished, program exits ##########'
                sys.exit()

            if not self.semaphore_RequestQueue.acquire(block=False):
                print 'Crawler info: no available semaphore to crawl url acquired, wait other process to release one ...'
                continue

            requestURL_info = self.request_queue.get(block=True)
            p = Process(target=self.crawl_URL, args=(requestURL_info,))
            p.daemon = True
            p.start()



    def is_invalid_outlink(self, url):
        for key_word in self.invalidWebsite_keyWords:
            if key_word in url:
                # print 'Crawler: Ignore invalid website page ', url
                return True

        try:
            url.decode('ascii')
        except Exception as e:
            #print 'Crawler: Ignore non english page ', e.message," ", url
            return True

    def canonicalize_outLinks(self, inlink, original_outlinks):
        # deal with relative outlinks
        hostAdded_Links = []
        for url in original_outlinks:
            if url == None:
                continue
            if url.startswith('http://') or url.startswith('https://'):
                hostAdded_Links.append(url)
                continue
            if url.startswith('../') or url.startswith('./'):
                hostAdded_Links.append(inlink.rstrip('/') + '/' + url)
                continue
            if url.startswith('/') or re.match('([0-9A-Za-z]+\.)+[0-9A-Za-z]+', url) != None:
                hostAdded_Links.append(urlparse.urljoin(inlink, url))
                continue

        results = []
        for url in hostAdded_Links:
            try:
                url = url.encode(encoding='utf-8', errors='replace')
                url = UrlCleaner.norm(url)
                url = url.split('#')[0]
                results.append(url)
            except Exception, e:
                print 'Crawler exception:  canonicalize : ', e.message ,' Ignore ',url
                continue
        return results

    def crawl_URL(self, requestURL_info):
        request_url,request_url_wave=requestURL_info.decodeInfo()

        try:
            response = urllib2.urlopen(request_url, timeout=10)
        except Exception, e:
            print 'Crawler exception :  timeout request ',e.message," Ignore ",request_url
            self.semaphore_RequestQueue.release()
            exit(0)

        #check status code
        if int(response.getcode()) != 200:
            #print 'Crawler: Ignore bad request page',  request_url
            self.semaphore_RequestQueue.release()
            exit(0)

        #check header
        header = response.info()
        if not header:
            header=dict()

        if 'content-language' in header:
            if 'en' not in header['content-language']:
                #print 'Crawler: Ignore non-english page ',request_url
                self.semaphore_RequestQueue.release()
                exit(0)

        if 'content-type' in header:
            if 'text' not in header['content-type']:
                #print 'Crawler: Ignore non-text page ',request_url
                self.semaphore_RequestQueue.release()
                exit(0)

        header = str(header)


        #check source decode
        response_source = response.read()
        try:
            response_source = response_source.decode('utf-8', 'ignore')
        except Exception, e:
            print 'Crawler exception: non utf-8 page source ',e.message," Ignore ",request_url
            self.semaphore_RequestQueue.release()
            exit(0)

        try:
           parser = etree.HTMLParser(target=Parser(request_url), remove_blank_text=True, remove_comments=True)
           etree.HTML(response_source, parser)
           text = ' '.join(parser.target.text_lines)
           title = parser.target.title
           outLinks = parser.target.links
           # canonicalize  the outlink
           outLinks = self.canonicalize_outLinks(request_url,outLinks)
        except Exception,e:
            print 'Crawler exception :  response_source parse ',e.message," Ignore ",request_url
            self.semaphore_RequestQueue.release()
            exit(0)

        #get valid outlinks and send them to self.selection_queue
        valid_outlinks=[]
        for outlink in outLinks:

            if self.is_invalid_outlink(outlink):
                # print ' Crawler: Ignore invalid outlink  ',outlink
                continue

            valid_outlinks.append(outlink)


            #send related info of outlink
            outlink_wave=request_url_wave+1
            inlink_relevanScore=1
            outlink_url_info=OutlinkURLInfo(outlink, outlink_wave, inlink_relevanScore)

            self.selection_queue.put(outlink_url_info)


        # store_content
        try:

            doc = dict(docno=request_url
                       , HTTPheader=header
                       , title=title
                       , text=text
                       , html_Source=response_source
                       , in_links=[]
                       , out_links=valid_outlinks
                       , author='Yu Wen'
                       , depth=0
                       , url=request_url)

            # store in  daniel index
            doc_id=self.num_stored_page.value+1
            status = daniel_index.index(index=daniel_index_name, doc_type='document', id=doc_id, body=doc)
            if status['created']:
                self.num_stored_page.value += 1
                timeUsed=(time.time()-self.startSeconds)*1.0/60
                print '*Crawler*Finish*: ',self.num_stored_page.value,' page stored in ',timeUsed,' min. ', request_url
                self.semaphore_RequestQueue.release()
                exit(0)


        except Exception, e:
            print 'Crawler exception : Elasticsearch rejected storage : ',e.message," Ignore ",request_url
            self.semaphore_RequestQueue.release()
            exit(0)





