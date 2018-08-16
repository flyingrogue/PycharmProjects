#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import pymongo
from config import *

class MongoDB():
    def __init__(self,host=MONGO_HOST,port=MONGO_PORT,database=MONGO_DB,collection=MONGO_COLLECTION):
        self.host=host
        self.port=port
        self.database=database
        self.collection=collection

        self.client=pymongo.MongoClient(host=self.host,port=self.port)
        self.db=self.client[self.database]
        self.col=self.db[self.collection]

    def insert(self,data):
        self.col.insert_one(data)

