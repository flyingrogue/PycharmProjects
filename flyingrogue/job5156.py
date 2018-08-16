import requests
import json
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import time

MAX_PAGE=2
KEYWORD='设计师'
LOCATION=14090000
headers={
    'Host':'www.job5156.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
base_url='http://www.job5156.com/s/result/ajax.json?'
data={'keyword':KEYWORD,'keywordType':0,'locationList':LOCATION,'sortB':0}
for page in range(1,MAX_PAGE+1):
    data['pageNo']=page
    url=base_url+urlencode(data)
    proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'http;//127.0.0.1:1080'
    }
    res=requests.get(url,headers=headers,proxies=proxies)
    result=json.loads(res.text)
    infos = result.get('page').get('items')
    for info in infos:
        href = info.get('posDetailUrl')
        url = 'http://www.job5156.com' + href
        res=requests.get(url,headers=headers)
        doc=pq(res.text)
        item={}
        item['posname'] = doc('.pos_wrap .pos_name').text()
        item['posdesc'] = doc('.pos_describle_content pre').text()
        item['degree'] = doc('.requirements li:first-child p').text()
        item['experience'] = doc('.requirements li:nth-child(2) p').text()
        item['address'] = doc('.requirements li:nth-child(3) p').text()
        print(item)
        with open('result.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(dict(item),ensure_ascii=False)+'\n')
        time.sleep(1)