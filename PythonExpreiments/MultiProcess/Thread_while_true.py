from  multiprocessing import  Process

def  thread_1():
    while True:
        print  '1'


def  thread_2():
    while True:
        print  '2'


def  thread_3():
    while True:
        print  '3'

if __name__ == '__main__':
 p1=Process(target=thread_1)
 p2=Process(target=thread_2)
 p3=Process(target=thread_3)

 p1.start()
 p2.start()
 p3.start()
 p1.join()
 p2.join()
 p3.join()

