from  multiprocessing import  Process,Manager
import  os

class MainClass(object):

    def __init__(self):
        self.resource =Manager().Value('l', 0)

    def process_1(self):
        while True:
            self.resource.value += 1
            print  ' add one  by process 1',self.resource.value
            if   self.resource.value >1000:
                os.kill (os.getpid(),9)
                print "process 1 kill fail"

    def process_2(self):
        while True:
            self.resource.value += 1
            print  ' add one  by process 2', self.resource.value
            if self.resource.value > 1000:
                os.kill(os.getpid(), 9)
                print "process 2 kill fail"







    def  multiProce(self):
        p1 = Process(target=self.process_1)
        p2 = Process(target=self.process_2)

        # p1.daemon=True
        # p2.daemon=True
        # p3.daemon=True

        p1.start()
        p2.start()

        while True:
            wait=1





if __name__ == '__main__':
    m=MainClass()
    m.multiProce()

