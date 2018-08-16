

from atexit import register
from random import randrange
from threading import BoundedSemaphore,Lock,Thread
from time import sleep,ctime

lock=Lock()
MAX=5
bs=BoundedSemaphore(MAX)

def refill():
    lock.acquire()
    print('refilling candy...',end='')
    try:
        bs.release()
    except ValueError:
        print('full,skipping')
    else:
        print('ok')
    lock.release()

def buy():
    lock.acquire()
    print('buying candy...',end='')
    if bs.acquire(False):
        print('ok')
    else:
        print('empty,skipping')
    lock.release()

def producer(loops):
    for i in range(loops):
        refill()
        sleep(randrange(3))

def consumer(loops):
    for i in range(loops):
        buy()
        sleep(randrange(3))

def main():
    print('starting at:',ctime())
    nloops=randrange(2,6)
    print('the candy machine (full with %d bars)！' % MAX)
    Thread(target=consumer,args=(randrange(nloops,nloops+MAX+2),)).start()
    Thread(target=producer,args=(nloops,)).start()

@register
def _atexit():
    print('all done at:',ctime())

if __name__=='__main__':
    main()



