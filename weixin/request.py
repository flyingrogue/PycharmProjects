#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from requests import Request
from config import *

class WeixinRequest(Request):
    def __init__(self,url,callback,method='GET',headers=None,need_proxy=False,fail_time=0,timeout=TIMEOUT):
        #注意此处三个参数顺序不能写错,或者写成url=url的形式
        Request.__init__(self,method,url,headers)
        self.callback=callback
        self.need_proxy=need_proxy
        self.fail_time=fail_time
        self.timeout=timeout




# class Request(RequestHooksMixin):
#     def __init__(self,
#                  method=None,url=None,headers=None,files=None,data=None,
#                  params=None,auth=None,cookies=None,hooks=None,json=None):

        # #Default empty dicts for dict params.
        # data=[] if data is None else data
        # files=[] if files is None else files
        # headers={} if headers is None else headers
        # params={} if params is None else params
        # hooks={} if hooks is None else hooks

        # self.hooks=default_hooks()
        # for (k,v) in list(hooks.items()):
        #     self.register_hook(event=k,hook=v)

        # self.method=method
        # self.url=url
        # self.headers=headers
        # self.files=files
        # self.data=data
        # self.json=json
        # self.params=params
        # self.auth=auth
        # self.cookies=cookies
