

from random import randint
from time import sleep
from queue import Queue
from myThread import MyThread

def writeQ(queue):
    queue.put('xxx',1)
    print('producing object for Q... size now',queue.qsize())

def readQ(queue):
    queue.get(1)
    print('consumed object from Q... size now',queue.qsize())

def writer(queue,loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1,3))

def reader(queue,loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2,5))

funcs=[writer,reader]
nfuncs=range(len(funcs))
pool=range(2)#线程池
def main():
    loops=randint(3,6)
    q=Queue(32)
    threads=[]
    for i in nfuncs:
        for j in pool:
            t=MyThread(funcs[i],(q,loops),funcs[i].__name__)
            threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('all done')

if __name__=='__main__':
    main()