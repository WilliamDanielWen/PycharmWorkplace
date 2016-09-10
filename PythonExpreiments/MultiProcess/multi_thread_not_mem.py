from  multiprocessing import  Process

class MainClass(object):

    def __init__(self):
        self.value = 0

    def thread_1(self):
        while True:
            self.value += 1
            print  self.value,  '  by thread 1'

    def thread_2(self):
        while True:
            self.value += 1
            print  self.value, '  by thread 2'

    def thread_3(self):
        while True:
            self.value += 1
            print  self.value, '  by thread 3'



    def  multiProce(self):
        p1 = Process(target=self.thread_1)
        p2 = Process(target=self.thread_2)
        p3 = Process(target=self.thread_3)
        # p1.daemon=True
        # p2.daemon=True
        # p3.daemon=True

        p1.start()
        p2.start()
        p3.start()






if __name__ == '__main__':
    m=MainClass()
    m.multiProce()

