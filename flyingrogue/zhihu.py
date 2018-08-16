#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
from pyquery import PyQuery as pq


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
res=requests.get('https://www.zhihu.com/explore',headers=headers)
doc=pq(res.text)
items=doc('.explore-feed').items()
for item in items:
    title=item.find('.question_link').text()
    author=item.find('.author-link').text()
    content=pq(item.find('.content').html()).text()
    print([title,author,content])