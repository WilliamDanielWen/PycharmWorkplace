import os
import sys
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

from threading import Thread

class Crawler(object):


    def __init__(self, num_requestProcess, target_num_pages,requestQueue, requestTimeout,selectionQueue):
        self.request_queue = requestQueue    # type: multiprocess.Queue
        self.selection_queue = selectionQueue # type multiprocess.Queue
        self.author = 'Yu.Wen'
        self.num_page_to_store=target_num_pages
        self.num_requestProcess = num_requestProcess
        self.requestTimeout=requestTimeout

        self.num_stored_page = Manager().Value('l', 0)


        self.keyWords_invalidWebsite = ['video', 'youtube', 'instagram', 'tv',
                                        'amazon', 'ebay', 'photo', 'image', 'game', 'shop', 'foursquare']
                                        #, 'facebook', 'twitter'
        self.startSecond=time.time()

    # keep creating deamon process spider_task, and put it into process_pool
    def start(self):



        crawl_process1 = Process(target=self.process_requestURL_andStore)
        crawl_process1.daemon = True
        crawl_process1.start()

        crawl_process2 = Process(target=self.process_requestURL_andStore)
        crawl_process2.daemon = True
        crawl_process2.start()

        crawl_process3 = Process(target=self.process_requestURL_andStore)
        crawl_process3.daemon = True
        crawl_process3.start()

        crawl_process4 = Process(target=self.process_requestURL_andStore)
        crawl_process4.daemon = True
        crawl_process4.start()

        crawl_process5 = Process(target=self.process_requestURL_andStore)
        crawl_process5.daemon = True
        crawl_process5.start()

        crawl_process6 = Process(target=self.process_requestURL_andStore)
        crawl_process6.daemon = True
        crawl_process6.start()

        crawl_process7 = Process(target=self.process_requestURL_andStore)
        crawl_process7.daemon = True
        crawl_process7.start()

        crawl_process8 = Process(target=self.process_requestURL_andStore)
        crawl_process8.daemon = True
        crawl_process8.start()

        crawl_process9 = Process(target=self.process_requestURL_andStore)
        crawl_process9.daemon = True
        crawl_process9.start()

        crawl_process10 = Process(target=self.process_requestURL_andStore)
        crawl_process10.daemon = True
        crawl_process10.start()


        while True:

            if self.num_stored_page.value > self.num_page_to_store:
                print '################# Crawler Exit Info #############: ', self.num_stored_page, ' page stored, crawl finished, program exits ##########'
                sys.exit()


    def process_requestURL_andStore(self):
        print "Process id ",os.getpid()
        while True:
             if self.request_queue.empty():
                 #print "Crawler exception: Request_Queue is empty"
                 continue

             requestURL_info = self.request_queue.get()
             request_url,request_url_wave=requestURL_info.decodeInfo()

             try:
                 response = urllib2.urlopen(request_url, timeout=self.requestTimeout)
             except Exception, e:
                 print 'Crawler exception :  timeout request ',e.message," Ignore ",request_url
                 continue

             #check status code
             if int(response.getcode()) != 200:
                 #print 'Crawler: Ignore bad request page',  request_url
                 continue

             #check header
             header = response.info()
             if not header:
                 header=dict()

             if 'content-language' in header:
                 if 'en' not in header['content-language']:
                     #print 'Crawler: Ignore non-english page ',request_url
                     continue

             if 'content-type' in header:
                 if 'text' not in header['content-type']:
                     #print 'Crawler: Ignore non-text page ',request_url
                     continue

             header = str(header)


             #check source decode
             response_source = response.read()
             try:
                 response_source = response_source.decode('utf-8', 'ignore')
             except Exception, e:
                 print 'Crawler exception: non utf-8 page source ',e.message," Ignore ",request_url
                 continue

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
                 continue

             #get valid outlinks and send them to self.selection_queue
             valid_outlinks=[]
             for outlink in outLinks:

                 if self.is_valid_outlink(outlink):
                    valid_outlinks.append(outlink)
                    #send related info of outlink
                    outlink_wave=request_url_wave+1
                    inlink_relevanScore=1
                    outlink_url_info=OutlinkURLInfo(outlink, outlink_wave, inlink_relevanScore)

                    self.selection_queue.put(outlink_url_info)

                 # else:
                    # print ' Crawler: Ignore invalid outlink  ',outlink


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
                     timeUsed= (time.time() - self.startSecond) * 1.0 / 60
                     print 'Crawler Store Success : ',self.num_stored_page.value,' page stored in ',timeUsed,' min. ', request_url




             except Exception, e:
                 print 'Crawler exception : Elasticsearch rejected storage : ',e.message," Ignore ",request_url
                 continue

    def is_valid_outlink(self, url):
        for key_word in self.keyWords_invalidWebsite:
            if key_word in url:
                # print 'Crawler: Ignore invalid website page ', url
                return False

        try:
            url.decode('ascii')
        except Exception as e:
            # print 'Crawler: Ignore non english page ', e.message," ", url
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
                print 'Crawler exception:  canonicalize : ', e.message, ' Ignore ', url
                continue
        return results



