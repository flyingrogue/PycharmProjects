#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import pymysql
from config import *

#MYSQL初始化
class Mysql():
    def __init__(self,host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD,port=MYSQL_PORT,database=MYSQL_DATABASE):
        self.host=host
        self.user=user
        self.password=password
        self.port=port
        self.database=database
        try:
            self.db=pymysql.connect(host,user,password,database,charset='utf8',port=port)
            self.cursor=self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)

    #插入数据
    def insert(self,data):
        keys=','.join(data.keys())
        values=','.join(['%s']*len(data))
        sql='insert into %s(%s) values (%s)' % (MYSQL_TABLE,keys,values)
        try:
            self.cursor.execute(sql,tuple(data.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()


