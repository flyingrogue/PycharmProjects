#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
from pyquery import PyQuery as pq
import re

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Host':'www.zhihu.com',
    'x-requested-with':'XMLHttpRequest',
}
for i in range(5):
    offest=i*5
    url='https://www.zhihu.com/node/ExploreAnswerListV2?params=%7B%22offset%22%3A'+str(offest)+'%2C%22type%22%3A%22day%22%7D'
    res=requests.get(url,headers=headers)
    #title=re.findall('class="question_link".*?"Title">(.*?)</a>',res.text,re.S)
    #print(title)
    doc=pq(res.text)
    titles=doc('.question_link').items()
    authors=doc('.author-link').items()
    votes=doc('.zm-item-vote-count').items()
    contents=doc('.content').items()
    for title,author,vote,content in zip(titles,authors,votes,contents):
        list=[]
        list.append(title.text().strip())
        list.append(author.text().strip())
        list.append(vote.text())
        list.append(pq(content.html()).text().strip())
        #print(list)
        with open('explore.txt','a',encoding='utf-8') as f:
            f.write('\n'.join([list[0],list[1],list[2],list[3]]))
            f.write('\n'+'-'*50+'\n')





