#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import pymysql
product={
    'title':'shjs','shop':'dhsk','location':'kyt','price':'khbv','deal':'kje','href':'sdnskdn'
}
db = pymysql.connect(host='localhost', user='root', password='ljb1994917', port=3306, db='taobao')
cursor = db.cursor()
sql='CREATE TABLE IF NOT EXISTS products(id INT AUTO_INCREMENT PRIMARY KEY,title VARCHAR(100) NOT NULL,' \
        'shop VARCHAR(100) NOT NULL,location VARCHAR(100) NOT NULL,price VARCHAR(100) NOT NULL,deal VARCHAR(100) NOT NULL,' \
        'href VARCHAR(100) NOT NULL)'
cursor.execute(sql)
sql='INSERT INTO products(title,shop,location,price,deal,href) values (%s,%s,%s,%s,%s,%s)'
try:
    cursor.execute(sql,tuple(product.values()))
    db.commit()
except:
    db.rollback()
db.close()