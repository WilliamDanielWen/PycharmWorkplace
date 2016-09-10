import os
import sys
import time
import urllib2
from lxml import etree
from reppy.cache import RobotsCache
from multiprocessing import Process,Lock
from multiprocessing import Manager
from Utilities import daniel_index_name,daniel_index
from Utilities import ParserTarget
from Utilities import OutlinkURLInfo
from Utilities import get_host
import cPickle


class Crawler(object):


    def __init__(self
                 ,num_requestProcess
                 ,target_num_pages
                 ,requestTimeout
                 ,requestQueue
                 ,selectionQueue
                 ,seenUrl_dict_init
                 ,selectionQueueLock):

        self.num_requestProcess = num_requestProcess
        self.num_page_to_store = target_num_pages
        self.requestTimeout = requestTimeout

        self.request_queue = requestQueue  # type: multiprocess.Queue
        self.selection_queue = selectionQueue  # type multiprocess.Queue

        self.author = 'Yu.Wen'

        self.robot_rules = Manager().dict()  # for now stores robot parser files
        self.seenURLs = seenUrl_dict_init  # used for detect dublicates,initialized as canonicalized urls

        self.process_pool_lock=Lock
        self.num_stored_page = Manager().Value('l', 0)
        self.num_requested_page = Manager().Value('l', 0)
        self.keyWords_invalidWebsite = ['video', 'youtube', 'instagram', 'tv',
                                        'amazon', 'ebay', 'photo', 'image', 'game', 'shop'
                                        , 'facebook', 'twitter','linkedin']
        self.startSecond=time.time()
        self.semaphore_RequestQueue = Manager().Value('l', num_requestProcess)
        self.outlink_dict=Manager().dict()
        self.relevant_words=[
                              "maritime","marine","ocean"

                              ,"accident","disaster","traged"

                              , "lampedusa", "migrant","shipwreck"

                              ,"cruise","sail","cargo","boat"

                              , "sink","sank", "sunk"

                              ,"crash"

                              ,"iceberg"

                              ,"dead","casualt"

                              ,"injur"
                            ]

        self.lowest_priority=len(self.relevant_words)+1


    def process_crawl_requestLinks_byMultiprocess(self):
        print 'Crawler started ...'
        process_pool=set()
        monitor_start_time = time.time()
        while True:

            timeUsed = (time.time() - self.startSecond)
            if self.num_stored_page.value >= self.num_page_to_store:
                for p in process_pool.copy():
                        p.terminate()
                        process_pool.remove(p)
                print ""


                print '################# Crawler Exit Info #############: '
                print "Dumping outlinks dict ...."
                self.dump_outlink_dict()
                print self.num_stored_page.value, ' page stored ', self.num_requested_page.value, " requests made within ", timeUsed, ' seconds.'
                print '############## Crawling finished, program exits ##############'
                sys.exit()


            if (time.time()-monitor_start_time)>10:
                monitor_start_time=time.time()
                print "Monitor Crawler:",self.num_stored_page.value, ' page stored in ', self.num_requested_page.value, " requests made within ", timeUsed, ' seconds.'

            try:
                requestURL_info = self.request_queue.get(block=False)
            except Exception, e:
                #print "Crawler: Request Queue locked"
                continue


            if self.semaphore_RequestQueue.value<=0:

                #print 'Crawler info: no available semaphore to crawl url acquired, wait other process to release one ...'

                #clean exited process
                for p in process_pool.copy():
                    if not p.is_alive():
                        #print "Crawl Process ",p.pid, " is dead, create a new one...."
                        p.terminate()
                        process_pool.remove(p)
                        self.semaphore_RequestQueue.value +=1
                continue

            self.semaphore_RequestQueue.value -=1
            new_process = Process(target=self.process_requestURL_andStore, args=(requestURL_info,))
            new_process.daemon = True
            process_pool.add(new_process)

            new_process.start()

    def process_requestURL_andStore(self,requestURL_info):

        request_url,request_url_wave,domain=requestURL_info.decodeInfo()


        self.update_robote_rules(domain)

        # 1. check whether is rejected by robot
        if self.is_rejected_byRobot(domain, request_url):
            print 'Cralwer Ignore request: Robot file rejected page exception: ', request_url
            return

        # 2. make http request
        try:
            self.num_requested_page.value += 1
            response = urllib2.urlopen(request_url, timeout=self.requestTimeout)
        except Exception, e:
            print 'Crawler Ignore request: Timeout request exception: {}'.format(e),"  ",request_url
            return

        # 3. check status code
        response_code=response.getcode()
        if response_code:
            if int(response_code) != 200:
                print 'Crawler Ignore request : Bad status response code exception : ',  request_url
                return

        #4. check header
        header = response.info()
        if not header:
            header=dict()


        if 'content-language' in header:
            if 'en' not in header['content-language']:
                print 'Crawler Ignore request: Non-english page exception : ', request_url
                return

        if 'content-type' in header:
            if 'text' not in header['content-type']:
                print 'Crawler Ignore request: Not text - html, json, or xml  page exception: ',request_url
                return


        header = str(header)

        #5. check response encoding
        try:
            response_source = response.read()
        except Exception, e:
            print 'Crawler Ignore request : Response Read exception {}'.format(e), " ", request_url
            return

        try:
            response_source = response_source.decode('utf-8', 'ignore')
        except Exception, e:
            print 'Crawler Ignore request: Response Decode in utf-8  exception:   {}'.format(e)," ",request_url
            return

        text=''
        title=''
        outLinks=[]
        #6. parse the response
        if 'html'  in header:
            result=self.parse_HTML(request_url, response_source)
            if result==None:
                return
            else:
                (text,title,outLinks)=result
        else:
            result = self.parse_XML(request_url, response_source)
            if result == None:
                return
            else:
                (text, title, outLinks) = result



        #7.get valid outlinks
        valid_outlinks = []
        for outlink in outLinks:

            if  not self.is_valid_outlink(outlink):
                # print ' Crawler info : ignore invalid outlink  ',outlink
                continue

            valid_outlinks.append(outlink)


        #8.store request_url content
        try:
            doc = dict(docno=request_url
                       , HTTPheader=header
                       , title=title
                       , text=text
                       , html_Source=response_source
                       , in_links=[]
                       , out_links=valid_outlinks
                       , author='Yu Wen'
                       , depth=request_url_wave
                       , url=request_url)

            status = daniel_index.index(index=daniel_index_name, doc_type='document', id=request_url, body=doc)

            if status['created']:
                self.num_stored_page.value += 1
                timeUsed= (time.time() - self.startSecond)
                print '###_Crawler_Store_Success_###',self.num_stored_page.value, ' page stored ', self.num_requested_page.value, " requests made within ", timeUsed, ' seconds. '#,request_url

                # 9.update inlink dict
                self.update_outlink_dict(request_url, valid_outlinks)

                # 10. send valid outlinks to self.selection_queue

                outlink_wave = request_url_wave + 1
                for valid_outlink in valid_outlinks:
                # send valid outlink and its related information
                    score=self.get_url_priority(request_url,valid_outlink)
                    outlink_url_info = OutlinkURLInfo(valid_outlink, outlink_wave, score)
                    self.selection_queue.put(outlink_url_info)
                return

            else:
                print "Crawler Ignore request: Elasticsearch store status exception!  ",request_url
                return

        except Exception, e:
            print "CrawlerIgnore request: Elasticsearch store page failure exception!  ",request_url, " Exception message: {}".format(e)
            return

    def update_robote_rules(self, domain):
        if not self.robot_rules.has_key(domain):

            try:
                robots = RobotsCache()
                site_robot_rules = robots.fetch("http://" + domain)
            except Exception, e:
                #print "Crawler: site don't have robot file, keep going ", domain
                return

            # initialize robot parser
            self.robot_rules[domain] = site_robot_rules

    def is_rejected_byRobot(self, domain, outlink):
        # check if is robot forbidden page
        if not self.robot_rules.has_key(domain):
            return False

        if self.robot_rules[domain].allowed(outlink, "*"):
            return False
        else:
            return True

    def is_valid_outlink(self,outlink):

        # detect duplicate
        if  self.seenURLs.has_key(outlink):
             #print 'Crawler ignore outlink: Duplicate outlink found: ',outlink
             return False
        self.seenURLs[outlink] = 1

        try:
            get_host(outlink)
        except Exception, e:
            print "Crawler ignore outlink: Domain parse exception {}".format(e), outlink
            return False

        #filt non english outlink
        try:
            outlink.decode('ascii')
        except Exception as e:
            #print 'Crawler ignore outlink":  Outlink url decode ascii exception,  {}'.format(e), outlink
            return False

        for key_word in self.keyWords_invalidWebsite:
            if key_word in outlink:
                #print 'Crawler ignore outlink: Outlink is page from invalid website  ',key_word, outlink
                return False

        return True

    def update_outlink_dict(self, stored_requested_url, valid_outlinks):
        #store outlink dict
        self.outlink_dict[stored_requested_url]=list(valid_outlinks)

    def dump_outlink_dict(self):

        path_inlink = '../runtime_cache/outlink_dict.cpkl'
        if os.path.exists(path_inlink):
            os.remove(path_inlink)
        out_file = open(path_inlink, 'wb')
        dict_values=self.outlink_dict._getvalue()
        cPickle.dump(dict_values, out_file, protocol=cPickle.HIGHEST_PROTOCOL)
        out_file.close()

    def get_url_priority(self, request_url, outlink):
        request_url=str(request_url).lower()
        outlink=str(outlink).lower()

        priority=self.lowest_priority

        for r_word in self.relevant_words:
            if r_word in outlink :
                priority-=1
            if r_word in request_url:
                priority -= 1

        return priority

    def parse_HTML(self,request_url,response_source):
        try:
            parser = etree.HTMLParser(target=ParserTarget(request_url), remove_blank_text=True, remove_comments=True)
            etree.HTML(response_source, parser)
            text = ' '.join(parser.target.text_lines)
            title = parser.target.title
            outLinks = parser.target.links
            return text,title,outLinks
        except Exception, e:
            print 'Crawler Ignore request: Parse html response exception :  {}'.format(e), "  ", request_url
            return None

    def parse_XML(self, request_url, response_source):
        try:
            parser = etree.XMLParser(target=ParserTarget(request_url), remove_blank_text=True, remove_comments=True)
            etree.XML(response_source, parser)
            text = ' '.join(parser.target.text_lines)
            title = parser.target.title
            outLinks = parser.target.links
            return text, title, outLinks
        except Exception, e:
            print 'Crawler Ignore request: Parse xml response exception :  {}'.format(e), "  ", request_url
            return None

    def parse_XML(self, request_url, response_source):
        try:
            parser = etree.XMLParser(target=ParserTarget(request_url), remove_blank_text=True, remove_comments=True)
            etree.XML(response_source, parser)
            text = ' '.join(parser.target.text_lines)
            title = parser.target.title
            outLinks = parser.target.links
            return text, title, outLinks
        except Exception, e:
            print 'Crawler Ignore request: Parse xml response exception :  {}'.format(e), "  ", request_url
            return None

