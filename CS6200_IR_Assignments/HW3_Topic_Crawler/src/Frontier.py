import time
from Utilities import RequestURLInfo
from  Utilities import get_host
from Queue import Queue
from Utilities import PriorityQueueManager
from multiprocessing import Process
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


    def start(self):
        monitor_process=Process(target=self.frontier_monitor)
        input_process=Process(target=self.from_Input_to_priorityQueue)
        select_and_output_process=Process(target=self.from_priorityQueue_to_Output)

        monitor_process.start()
        input_process.start()
        select_and_output_process.start()

        monitor_process.join()
        input_process.join()
        select_and_output_process.join()


    def frontier_monitor(self):
        while True:
            print "Monitor Frontier: priority_queue size ",self.priority_queue.qsize()
            time.sleep(3)



    def from_Input_to_priorityQueue(self):
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

            self.priority_queue.put((score,request_url_info))

    def from_priorityQueue_to_Output(self):

        while True:
            # delay a politeness time
            start_second = time.time()
            get_from_priority_queue = True

            while get_from_priority_queue:
                if not self.priority_queue.empty():
                    request_url_info = self.priority_queue.get()[1]
                    self.send_to_delayQueues(request_url_info)

                miliSeconds_passed = time.time() * 1000 * 1.0 - start_second * 1000 * 1.0
                if miliSeconds_passed > self.politeness_delay:
                    get_from_priority_queue = False

            self.release_OneWaveUrls_fromDelayQueues()


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



