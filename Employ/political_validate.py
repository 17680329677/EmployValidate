#!/usr/bin/env python
# coding=utf-8
# 政治面貌代码验证

from data_resource import employ_conn


def get_political_dict():
    cursor = employ_conn.cursor()
    select_sql = '''select * from basic where type = 'political' and status = 1'''
    cursor.execute(select_sql)
    results = cursor.fetchall()
    political_dict = {}
    for res in results:
        code = res[1]
        name = res[2]
        political_dict.update({name: code})
    # print(political_dict)
    return political_dict


def political_validate_and_verify(political_dict):
    select_sql = '''select username, political, political_code from student'''
    update_sql = '''update student set political_code = %s where username = %s and political = %s'''
    cursor = employ_conn.cursor()
    cursor.execute(select_sql)
    results = cursor.fetchall()

    with open("../log/political", "a") as w:
        for res in results:
            username = res[0]
            political = res[1]
            political_code = res[2]
            if political is not None and political != '':
                if political in political_dict and str(political_code) == political_dict[political]:
                    print(username + '--校验通过！')
                elif political in political_dict and str(political_code) != political_dict[political]:
                    print(username + '--代码不匹配！')
                    cursor.execute(update_sql, (political_dict[political], username, political))
                    employ_conn.commit()
                    w.write(username + '修改成功！\n')


if __name__ == '__main__':
    political_dict = get_political_dict()
    political_validate_and_verify(political_dict)