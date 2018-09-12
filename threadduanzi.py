

import requests
import json
from threading import Thread,Lock,BoundedSemaphore
from queue import Queue
from lxml import etree
import time

headers={
    'Host':'www.qiushibaike.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

class CrawlThread(Thread):
    def __init__(self,threadName,pageQueue,dataQueue):
        super(CrawlThread,self).__init__()
        self.threadName=threadName
        self.pageQueue=pageQueue
        self.dataQueue=dataQueue

    def run(self):
        print(self.threadName,'启动')
        while not CRAWL_EXIT:
            try:
                page=self.pageQueue.get(False)
                url='https://www.qiushibaike.com/8hr/page/'+str(page)
                res=requests.get(url,headers=headers)
                self.dataQueue.put(res.text)
            except:
                pass
        print(self.threadName,'结束')

class ParseThread(Thread):
    def __init__(self,threadName,dataQueue,filename):
        super(ParseThread,self).__init__()
        self.threadName=threadName
        self.dataQueue=dataQueue
        self.filename=filename

    def parse(self,html):
        html=etree.HTML(html)
        node_list=html.xpath('//*[@id="content-left"]/div')
        print(len(node_list))
        for node in node_list:
            username=node.xpath('.//h2/text()')[0].strip()
            image=node.xpath('./div[@class="thumb"]//@src')
            content=node.xpath('.//div[@class="content"]/span/text()')[0].strip()
            zan=node.xpath('.//div[@class="stats"]/span[1]/i/text()')[0]
            comments=node.xpath('.//div[@class="stats"]/span[2]//i/text()')[0]
            yield {
                'uesrname':username,
                'image':image,
                'content':content,
                'zan':zan,
                'comments':comments
            }

    def run(self):
        print(self.threadName,'启动')
        while not PARSE_EXIT:
            try:
                html=self.dataQueue.get(False)
                for item in self.parse(html):

                    self.filename.write(json.dumps(item,ensure_ascii=False)+'\n')
            except:
                pass
        print(self.threadName,'结束')


CRAWL_EXIT=False
PARSE_EXIT=False

def main():
    lock=Lock()
    bs=BoundedSemaphore(1)
    pageQueue=Queue(10)
    for i in range(1,6):
        pageQueue.put(i)
    dataQueue=Queue()
    filename=open('段子.txt','a',encoding='utf-8')


    crawllist=['采集线程1号','采集线程2号','采集线程3号']
    crawlthread=[]
    for threadName in crawllist:
        thread=CrawlThread(threadName,pageQueue,dataQueue)
        thread.start()
        crawlthread.append(thread)

    while not pageQueue.empty():
        pass
    global CRAWL_EXIT
    CRAWL_EXIT=True
    print('pageQueue为空')
    for thread in crawlthread:
        thread.join()



    parselist = ['解析线程1号','解析线程2号','解析线程3号']
    parsethread = []
    for threadName in parselist:
        thread = ParseThread(threadName, dataQueue, filename)
        thread.start()
        parsethread.append(thread)
    while not dataQueue.empty():
        pass

    global PARSE_EXIT
    PARSE_EXIT=True
    print('dataQueue为空')

    for thread in parsethread:
        thread.join()


if __name__=='__main__':
    main()



