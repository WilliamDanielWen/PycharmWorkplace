from Crawler  import Crawler
from Frontier import Frontier
from multiprocessing import Process
from Utilities import create_daniel_index
from Utilities import canonicalize_url,get_host,OutlinkURLInfo
from multiprocessing import Queue
from multiprocessing import Manager
import time

def system_monitor(requestQueue
                   , selectionQueue):
    while True:
        print "Monitor System: Selection-Queue size is ", selectionQueue.qsize()
        print "Monitor System: Request-Queue size is :", requestQueue.qsize()
        time.sleep(3)


#seed do not contain duplicate and is canonicalized,which are trated as a new outlink
def loadSeeds():
    # load seeds
    seedurl_list = []
    path="../../Data/HW3_Crawler_Data/seeds.txt"
    file=open(path,"r")
    while True:
        seed_url = file.readline().strip()
        if seed_url=="":
            continue

        if seed_url == 'EOF':
            break
        seedurl_list.append(seed_url)


    seeds = []
    initwave=0
    priority=-1000# this actually is an very high priority in Priority Queue
    seenUrl_dict_init = Manager().dict()

    for url in seedurl_list:

        canonized_url=canonicalize_url("",url)

        if not canonized_url:
            print "Staters ignore seed url: Canonicalize seed exception ",url
            continue

        if  seenUrl_dict_init.has_key(canonized_url):
            print "Staters ignore seed url: Duplicate seed ", canonized_url
            continue

        seenUrl_dict_init[canonized_url]=1

        try:
            domain = get_host(canonized_url)
        except Exception, e:
            print "Staters ignore seed url: Domain parse exception {}",format(e),canonized_url
            continue


        seeds.append(OutlinkURLInfo(canonized_url, initwave, priority))

    print "Seeds loaded, quantity: ", len(seeds)
    return seeds,seenUrl_dict_init


create_daniel_index()
requestQueue=Queue()
selectionQueue=Queue()
selectionQueueLock=Manager().Lock()

seeds,seenUrl_dict_init=loadSeeds()
for seed in seeds:
    selectionQueue.put(seed)


politeness_delay = 1000
num_requestProcess =50
target_num_pages=41000
requestTimeout=5

crawler = Crawler(num_requestProcess
                  ,target_num_pages
                  , requestTimeout
                  ,requestQueue
                  ,selectionQueue
                  ,seenUrl_dict_init
                  ,selectionQueueLock)

frontier = Frontier(politeness_delay
                    ,requestQueue
                    ,selectionQueue
                    ,selectionQueueLock)

frontier_process = Process(target=frontier.start)
crawl_process = Process(target=crawler.process_crawl_requestLinks_byMultiprocess)
system_monitor_process=Process(target=system_monitor, args=(requestQueue
                                                             , selectionQueue
                                                             ,))

system_monitor_process.start()
frontier_process.start()
crawl_process.start()

crawl_process.join()
frontier_process.terminate()
time.sleep(3)
system_monitor_process.terminate()


