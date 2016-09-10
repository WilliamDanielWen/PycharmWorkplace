import time
from Utilities import RequestURLInfo
from  Utilities import get_host
from Queue import Queue,PriorityQueue
from Utilities import PriorityQueueManager
class Frontier(object):


    def __init__(self
                 ,politeness_delay
                 ,requestQueue
                 ,selectionQueue
                 ,selectionQueueLock):

        self.selection_queue = selectionQueue  # store outlinks, input of frontier
        self.request_queue = requestQueue #https can be request instantly,output of Frontier

        # datas used for politeness delay
        self.politeness_delay = politeness_delay
        self.delayQueues=dict()
        self.selectionQueueLock=selectionQueueLock


        pqmgr = PriorityQueueManager()
        pqmgr.start()
        self.priority_queue=pqmgr.MultiProcessPriorityQueue()

    def start_not_polite(self):
        print 'Frontier started ...'
        while True:
            request_url_info = self.get_oneURL_fromSelectionQueue()

            if request_url_info:
                self.request_queue.put(request_url_info)



    def start(self):

        while True:
            # delay a politeness time
            start_second=time.time()
            receive_url_signal=True
            num_page_retrieved=0

            while receive_url_signal:
                request_url_info=self.get_oneURL_fromSelectionQueue()
                if not request_url_info==None:
                    self.send_to_delayQueues(request_url_info)

                miliSeconds_passed= time.time()*1000*1.0- start_second*1000*1.0


                if miliSeconds_passed>self.politeness_delay:
                #if num_page_retrieved > 100:
                    receive_url_signal=False


            #print "Frontier: Start releasing url to request queue ..."
            self.release_OneWaveUrls_fromDelayQueues()

    def receive_from_selection_queue(self):
        while True:

            try:
                outlink_Url_info=self.selection_queue.get(block=False)
            except Exception,e:
                #print "Frontier: selection queue locked"
                continue

            outlink, outlink_wave, score = outlink_Url_info.decodeInfo()

            try:
                domain = get_host(outlink)
            except Exception, e:
                # print "Frontier outlink get domain exception: {}".format(e)," Ignore outlink ", outlink
                continue

            request_url_info = RequestURLInfo(outlink, outlink_wave, domain)

            self.priority_queue.put(score,request_url_info)



    def send_to_delayQueues(self, request_url_info):
        request_url,requestUrl_wave, domain=request_url_info.decodeInfo()

        if self.delayQueues.has_key(domain):
            self.delayQueues[domain].put(request_url_info)
        else:
            self.delayQueues[domain] = Queue()
            self.delayQueues[domain].put(request_url_info)
            #print "Frontier info: New domain put in delay queues, domain: ", domain



    def release_OneWaveUrls_fromDelayQueues(self):

        # pop one url from each domain
        domains = self.delayQueues.keys()

        size=len(domains)
        print "Frontier: ", size, " urls released with domains: ", domains

        if  size== 0:
            return

        for domain in domains:

            request_url_info = self.delayQueues[domain].get()

            # put into request queue

            self.request_queue.put(request_url_info)
            # print "Frontier info: release url for domain: ", domain

            if self.delayQueues[domain].empty():
                self.delayQueues.pop(domain)
                # print "Frontier info: remove empty queue for domain ", domain



