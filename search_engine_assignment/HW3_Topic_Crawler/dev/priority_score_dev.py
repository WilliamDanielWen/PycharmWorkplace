seedurl_list = []
path="../../Data/HW3_Crawler_Data/seeds.txt"
file=open(path,"r")
while True:
    seed_url = file.readline().strip()
    if seed_url == '':
        break
    seedurl_list.append(seed_url)


from Crawler import Crawler
from multiprocessing import Queue
crawler = Crawler(num_requestProcess=8
                  ,target_num_pages=0
                  , requestTimeout=0
                  ,requestQueue=Queue()
                  ,selectionQueue=Queue()
                  ,seenUrl_dict_init=dict)

tittle=None
print "Lowest priority: ",crawler.lowest_priority
for url in seedurl_list:
    print  crawler.get_url_priority(tittle,url), str(url).lower()


