#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import pymysql
#id='2013003430'
#user='Steven'
#age=21
#table='students'
#condition='age>22'
db=pymysql.connect(host='localhost',user='root',password='ljb1994917',port=3306,db='spiders')
cursor=db.cursor()
sql='SELECT * FROM students WHERE age>19 '
#sql='DELETE FROM {table} WHERE {condition}'.format(table=table,condition=condition)
#sql='UPDATE students SET age=%s WHERE name=%s'
#sql='INSERT INTO students(id ,name,age) values(%s,%s,%s)'
#sql='CREATE TABLE IF NOT EXISTS students (id VARCHAR(100) NOT NULL, name VARCHAR(100) NOT NULL, age INT NOT NULL,PRIMARY KEY (id))'
cursor.execute(sql)
#db.commit()
results=cursor.fetchall()
for result in results:
    print(result)
#db.close()