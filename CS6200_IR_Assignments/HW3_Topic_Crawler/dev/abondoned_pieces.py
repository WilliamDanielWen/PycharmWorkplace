    #
    # # keep sending one outlink from Spider.url_queue_out to Frontier
    # def send_outLink_toFrontier(self):
    #     address = ('127.0.0.1', Crawler.PUSH_OUT_PORT)
    #     connection = Client(address, authkey=self.authkey)
    #     print ('crawler:  send connection established from {}'.format(address))
    #     while True:
    #         if not self.outlink_queue.empty():
    #             url = self.outlink_queue.get()
    #             try:
    #                 connection.send_bytes(url)
    #             except Exception, e:
    #                 print ('crawler: exception: {}, url : ,{}'.format(e, url))
    #                 continue
    #
    #     connection.close()
    #
    # #keep getting one inlink from Frontier and put it to Spider.url_queue_in
    # def receiveInLink_fromFrontier(self):
    #     address = ('127.0.0.1', Crawler.PULL_IN_PORT)
    #     listener = Listener(address, authkey=self.authkey)
    #     connection = listener.accept()
    #     print ('crawler:  receive connection established from {}'.format(address))
    #
    #     while True:
    #         try:
    #             url = connection.recv_bytes()
    #             self.inlink_queue.put(url)
    #         except Exception, e:
    #             print 'crawler: receive inlink exception {}'.format(e)
    #             continue
    #     connection.close()
    #     listener.close()
    #
    #
    # def start(self):
    #     receiveInlinks_process = Process(target=self.receiveInLink_fromFrontier)
    #     crawl_process = Process(target=self.start)
    #     sendOutlinks_process = Process(target=self.send_outLink_toFrontier)
    #
    #     # receiveInlinks_process.start()
    #     crawl_process.start()
    #     # sendOutlinks_process.start()
    #
    #
    #
    #     # receiveInlinks_process.join()
    #     crawl_process.join()
    #     # sendOutlinks_process.join()
    #
    #
    # # keep sending url from  back_queue to crawler to analysis the url
    # def sendInlinks_toCrawler(self):
    #     address = ('127.0.0.1', Frontier.PUSH_OUT_PORT)
    #     connection = Client(address, authkey=self.authkey)
    #     print ('frontier : send connection established from {}'.format(address))
    #     while True:
    #         url = self.inlink_queue.get(block=True)
    #         try:
    #             connection.send_bytes(url)
    #         except Exception, e:
    #             print ('frontier: send inlinks exception: {}, url : ,{}'.format(e, url))
    #         continue
    #
    #     connection.close()
    #
    #
    # # receive outlinks produced by crawler
    # def receiveOutlinks_fromCrawler(self):
    #     address = ('127.0.0.1', Frontier.PULL_IN_PORT)
    #     listener = Listener(address, authkey=self.authkey)
    #     connection = listener.accept()
    #     print ('Frontier : receive connection accepted from {}'.format(listener.address))
    #     while True:
    #         try:
    #             url = connection.recv_bytes()
    #             self.outlink_queue.put(url)
    #         except Exception,e:
    #             print ('Frontier: receive outlinks exception : {}'.format(e))
    #             continue
    #     connection.close()
    #     listener.close()
    #
    #
    # def start(self):
    #     receiveInlinks_process = Process(target=self.receiveInLink_fromFrontier)
    #     crawl_process = Process(target=self.start)
    #     sendOutlinks_process = Process(target=self.send_outLink_toFrontier)
    #
    #     # receiveInlinks_process.start()
    #     crawl_process.start()
    #     # sendOutlinks_process.start()
    #
    #
    #
    #     # receiveInlinks_process.join()
    #     crawl_process.join()
    #     # sendOutlinks_process.join()
    #
    #
    # PULL_IN_PORT = 9000
    # PUSH_OUT_PORT = 9001
    # BACK_QUEUE_MIN = 20000
    #
    # BACK_FRONT_RATIO = 0.1
    # BACK_QUEUE_DOMAIN_MIN = 14
    #
    #
    # PUSH_OUT_PORT = Frontier.PULL_IN_PORT
    # PULL_IN_PORT = Frontier.PUSH_OUT_PORT