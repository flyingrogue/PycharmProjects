
import requests
from requests import Session
import json
from urllib.parse import urlencode

base_url='https://xueqiu.com/statuses/search.json?'
headers={
    'Host':'xueqiu.com',
    'X-Requested-With':'XMLHttpRequest',
    #'Cookie':'xq_a_token=9c75d6bfbd0112c72b385fd95305e36563da53fb;',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}
cookies={'_gid': 'GA1.2.1519795370.1536762867', '_ga': 'GA1.2.1236204496.1536762867', 'aliyungf_tc': 'AQAAAGwWuRodMQIAUx1R2u7bQU3ychY3', 'xq_r_token.sig': 'usx1_hrblByw-9h0cXk1yLIUlL4', 'xq_a_token': '9c75d6bfbd0112c72b385fd95305e36563da53fb', 'xq_a_token.sig': '-6-bcHntQlhRjsyrvsY2IGwh-B4', 'xq_r_token': '9ad364aac7522791166c59720025e1f8f11bf9eb', 'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1536762865', 'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1536762865', '_gat_gtag_UA_16079156_4': '1', 'u': '501536762874878', 'device_id': '3925aa87d7b127e84e8250e96fc2edab'}

symbols=['SZ000651','SH600276']
for symbol in symbols:
    for page in range(1,6):
        params={
            'symbol':symbol,
            'page':page,
        }
        url=base_url + urlencode(params)
        headers.update({'Referer':'https://xueqiu.com/S/'+symbol})
        res=requests.get(url,headers=headers,cookies=cookies)
        lists=json.loads(res.text).get('list')
        for list in lists:
            dict={}
            dict['description']=list.get('description')
            print(dict)

