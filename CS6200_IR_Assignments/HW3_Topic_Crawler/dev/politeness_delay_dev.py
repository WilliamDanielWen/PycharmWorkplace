from multiprocessing.managers import BaseManager
from multiprocessing.managers import DictProxy
from collections import defaultdict
from Queue import PriorityQueue

from pybloom import ScalableBloomFilter
from Queue import Queue

class MemShareManager(BaseManager):
    pass

MemShareManager.register('defaultdict', defaultdict, DictProxy)
MemShareManager.register('dict', dict, DictProxy)
MemShareManager.register("PriorityQueue", PriorityQueue)

MemShareManager.register('ScalableBloomFilter', ScalableBloomFilter)
MemShareManager.register('Queue', Queue)



import time
from Queue import Queue
#from  threading import Thread,Lock
from multiprocessing import Process,Lock,Manager
class DelayTest(object):



    def __init__(self):

        self.politeness_delay = 100
        self.request_queue = Queue()

        self.delayQueuesLock = Lock()

        self.mgr=MemShareManager()

        self.delayQueues = self.mgr.dict()
        #
        # self.delayQueues['facebook'] = Queue()
        # self.delayQueues['linkedin'] = Queue()
        # self.delayQueues['amazon'] = Queue()
        # self.delayQueues['google'] = Queue()
        #
        # self.delayQueues['facebook'].put("fb1")
        # self.delayQueues['facebook'].put("fb2")
        # self.delayQueues['facebook'].put("fb3")
        # self.delayQueues['facebook'].put("fb4")
        # self.delayQueues['facebook'].put("fb5")
        # self.delayQueues['facebook'].put("fb6")
        #
        # self.delayQueues['linkedin'].put("linkin1")
        # self.delayQueues['linkedin'].put("linkin2")
        # self.delayQueues['linkedin'].put("linkin3")
        # self.delayQueues['linkedin'].put("linkin4")
        # self.delayQueues['linkedin'].put("linkin5")
        # self.delayQueues['linkedin'].put("linkin6")
        # self.delayQueues['linkedin'].put("linkin7")
        # self.delayQueues['linkedin'].put("linkin8")
        #
        # self.delayQueues['amazon'].put("ama1")
        # self.delayQueues['amazon'].put("ama2")
        # self.delayQueues['amazon'].put("ama3")
        # self.delayQueues['amazon'].put("ama4")
        # self.delayQueues['amazon'].put("ama5")
        # self.delayQueues['amazon'].put("ama6")
        # self.delayQueues['amazon'].put("ama7")
        # self.delayQueues['amazon'].put("ama8")
        # self.delayQueues['amazon'].put("ama9")
        # self.delayQueues['amazon'].put("ama10")
        #
        # self.delayQueues['google'].put("goog1")
        # self.delayQueues['google'].put("goog2")
        # self.delayQueues['google'].put("goog3")
        # self.delayQueues['google'].put("goog4")
        # self.delayQueues['google'].put("goog5")
        # self.delayQueues['google'].put("goog6")
        # self.delayQueues['google'].put("goog7")
        # self.delayQueues['google'].put("goog8")
        # self.delayQueues['google'].put("goog9")
        # self.delayQueues['google'].put("goog10")
        # self.delayQueues['google'].put("goog11")
        # self.delayQueues['google'].put("goog12")




    def start(self):

        p2 = Process(target=delaytest.remove_from_domainDelayQueues)
        p2.start()

        time.sleep(1)
        p1 = Process(target=delaytest.send_to_delayQueues,args=("apple","apple_request_url_info",))
        p1.start()



    def send_to_delayQueues(self,domain,request_url_info):

        with self.delayQueuesLock:
         if self.delayQueues.has_key(domain):
             self.delayQueues[domain].put(request_url_info)
             #print "put new domain"
         else:
             self.delayQueues[domain] = Queue()
             self.delayQueues[domain].put(request_url_info)
             print "Frontier info: new domain put in delay queues, domain: ",domain


    def remove_from_domainDelayQueues(self):


        while True:


            #delay a politeness time
            time.sleep(self.politeness_delay * 1.0 / 1000)

            with self.delayQueuesLock:
                # pop one url from each domain
               domains = self.delayQueues.keys()
               if len(domains)==0:
                   print "Frontier info: delay queues is empty for now"
                   continue

               print "Frontier info: domains to be  released: ",  domains
               for domain in domains:

                   request_url_info = self.delayQueues[domain].get()

                   # put into request queue
                   self.request_queue.put(request_url_info)
                   print "Frontier info: release url for domain: ", domain


                   if self.delayQueues[domain].empty():
                       self.delayQueues.pop(domain)
                       print "Frontier info: remove empty queue for domain ", domain


#test_queues = dict()

# test_queues['facebook'] = Queue()
# test_queues['linkedin'] = Queue()
# test_queues['amazon'] = Queue()
# test_queues['google'] = Queue()
#
# test_queues['facebook'].put("fb1")
# test_queues['facebook'].put("fb2")
# test_queues['facebook'].put("fb3")
# test_queues['facebook'].put("fb4")
# test_queues['facebook'].put("fb5")
# test_queues['facebook'].put("fb6")
#
# test_queues['linkedin'].put("linkin1")
# test_queues['linkedin'].put("linkin2")
# test_queues['linkedin'].put("linkin3")
# test_queues['linkedin'].put("linkin4")
# test_queues['linkedin'].put("linkin5")
# test_queues['linkedin'].put("linkin6")
# test_queues['linkedin'].put("linkin7")
# test_queues['linkedin'].put("linkin8")
#
# test_queues['amazon'].put("ama1")
# test_queues['amazon'].put("ama2")
# test_queues['amazon'].put("ama3")
# test_queues['amazon'].put("ama4")
# test_queues['amazon'].put("ama5")
# test_queues['amazon'].put("ama6")
# test_queues['amazon'].put("ama7")
# test_queues['amazon'].put("ama8")
# test_queues['amazon'].put("ama9")
# test_queues['amazon'].put("ama10")
#
# test_queues['google'].put("goog1")
# test_queues['google'].put("goog2")
# test_queues['google'].put("goog3")
# test_queues['google'].put("goog4")
# test_queues['google'].put("goog5")
# test_queues['google'].put("goog6")
# test_queues['google'].put("goog7")
# test_queues['google'].put("goog8")
# test_queues['google'].put("goog9")
# test_queues['google'].put("goog10")
# test_queues['google'].put("goog11")
# test_queues['google'].put("goog12")

delaytest=DelayTest()


delaytest.start()




