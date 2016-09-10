import time
from  Utilities import get_host
from Utilities import RequestURLInfo
import robotparser
from Queue import Queue
from  threading import Thread,Lock

class Frontier(object):


    def __init__(self, politeness_delay, requestQueue, selectionQueue):
        print 'Frontier started ...'
        self.request_queue = requestQueue #https can be request instantly
        self.selection_queue = selectionQueue# store outlinks


        self.domainInfo = dict() # for now stores robot parser files
        self.seenURLs=dict() #used for detect dublicates

        # datas used for politeness delay
        self.politeness_delay = politeness_delay
        self.delayQueues=dict()
        self.delayQueuesLock=Lock()


    def start(self):
        thread_selectURL_fromQueue = Thread(target=self.thread_selectURL_fromSelectionQueue)
        thread_selectURL_fromQueue.daemon = True

        thread_remove_from_domainDelayQueues=Thread(target=self.thread_removeFrom_domainDelayQueues)
        thread_remove_from_domainDelayQueues.daemon = True

        thread_selectURL_fromQueue.start()
        thread_remove_from_domainDelayQueues.start()

        thread_remove_from_domainDelayQueues.join();thread_selectURL_fromQueue.join();

        print"Frontier Error: thread_selectURL_fromQueue , thread_remove_from_domainDelayQueues finished"

    def thread_selectURL_fromSelectionQueue(self):

        while True:

            #get url
            if  self.selection_queue.empty():
                print "Frontier exception : selection_queue is empty"
                continue



            selectionUrl_info=self.selection_queue.get(block=True)
            print "Get one url from selection queue,"," Selection queue length", self.selection_queue.qsize()

            outlink,outlink_wave,inlink_relevanScore=selectionUrl_info.decodeInfo()


            #detect duplicate
            if outlink in self.seenURLs:
                # print 'Frontier: Ignore duplicate url ',url
                continue
            self.seenURLs[outlink] = 1


            try:
                domain=get_host(outlink)
                domain=str(domain)
            except Exception,e:
                print "Frontier exception : domain name unavailable", e.message, " Ignore ",outlink
                continue

            self.update_domain_info(domain)

            if self.is_Rejected_byRobot(domain,outlink):
                 #print 'Frontier: Ignore robot rejected page ', outlink
                 continue


            #put into delay queues
            request_url_info=RequestURLInfo(outlink,outlink_wave)

            self.send_to_delayQueues(domain,request_url_info)


    def thread_removeFrom_domainDelayQueues(self):

        while True:

            #delay a politeness time
            time.sleep(self.politeness_delay * 1.0 / 1000)

            with self.delayQueuesLock:
                # pop one url from each domain
               domains = self.delayQueues.keys()
               if len(domains)==0:
                   print "Frontier exception : delayQueues is empty"
                   continue

               #print "Frontier info: domains to be  released: ",  domains
               for domain in domains:

                   request_url_info = self.delayQueues[domain].get()

                   # put into request queue
                   self.request_queue.put(request_url_info)
                   #print "Frontier info: release url for domain: ", domain


                   if self.delayQueues[domain].empty():
                       self.delayQueues.pop(domain)
                       #print "Frontier info: remove empty queue for domain ", domain


    def update_domain_info(self, domain):
        if not self.domainInfo.has_key(domain):
            # initialize last request time
            self.domainInfo[domain] = dict()

            # initialize robot parser
            rparser = robotparser.RobotFileParser()
            rparser.set_url('http://' + domain + '/robots.txt')
            try:
                rparser.read()
                self.domainInfo[domain]['robotParser'] = rparser
            except Exception, e:
                # print "Frontier: No robot file in this site ", domain, " keep going"
                return


    def is_Rejected_byRobot(self, domain, outlink):
        # check if is robot forbidden page
        if self.domainInfo.has_key(domain):
            if self.domainInfo[domain].has_key('robotParser'):
                if self.domainInfo[domain]['robotParser'].can_fetch('*', outlink):
                    return False


    def send_to_delayQueues(self, domain, request_url_info):
        with self.delayQueuesLock:
            if self.delayQueues.has_key(domain):
                self.delayQueues[domain].put(request_url_info)
            else:
                self.delayQueues[domain] = Queue()
                self.delayQueues[domain].put(request_url_info)
                #print "Frontier info: New domain put in delay queues, domain: ", domain
