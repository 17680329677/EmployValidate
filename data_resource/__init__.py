# -*- coding : utf-8 -*-
# coding: utf-8
import pymysql

# 就业信息数据库
employ_conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='employ',
    charset='utf8'
)