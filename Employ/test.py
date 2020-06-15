#!/usr/bin/env python
# coding=utf-8

from data_resource import employ_conn

if __name__ == '__main__':
    cursor = employ_conn.cursor()
    select_sql = '''select * from student where username = %s'''
    cursor.execute(select_sql, ('7180278',))
    res = cursor.fetchall()
    print(res[0])