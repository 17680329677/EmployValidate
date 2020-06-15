#!/usr/bin/env python
# coding=utf-8
# 单位性质代码验证 property

from data_resource import employ_conn


def get_property_dict():
    cursor = employ_conn.cursor()
    select_sql = '''select * from basic where type = 'property' and status = 1'''
    cursor.execute(select_sql)
    results = cursor.fetchall()
    property_dict = {}
    for res in results:
        code = res[1]
        name = res[2]
        property_dict.update({name: code})
    print(property_dict)
    return property_dict


def property_validate_and_verify(property_dict):
    select_sql = '''select account, property, property_code from employ'''
    update_sql = '''update employ set property_code = %s where account = %s and property = %s'''
    cursor = employ_conn.cursor()
    cursor.execute(select_sql)
    results = cursor.fetchall()

    with open("../log/property", "a") as w:
        for res in results:
            account = res[0]
            property = res[1]
            property_code = res[2]
            if property is not None and property != '':
                if property in property_dict and str(property_code) == property_dict[property]:
                    print(account + '--校验通过！')
                elif property in property_dict and str(property_code) != property_dict[property]:
                    print(account + '--代码不匹配！')
                    cursor.execute(update_sql, (property_dict[property], account, property))
                    employ_conn.commit()
                    w.write(account + '修改成功！\n')


if __name__ == '__main__':
    property_dict = get_property_dict()
    property_validate_and_verify(property_dict)