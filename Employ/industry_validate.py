#!/usr/bin/env python
# coding=utf-8
# 单位行业代码验证 industry

from data_resource import employ_conn


def get_industry_dict():
    cursor = employ_conn.cursor()
    select_sql = '''select * from basic where type = 'industry' and status = 1'''
    cursor.execute(select_sql)
    results = cursor.fetchall()
    industry_dict = {}
    for res in results:
        code = res[1]
        name = res[2]
        industry_dict.update({name: code})
    # print(industry_dict)
    return industry_dict


def industry_validate_and_verify(industry_dict):
    select_sql = '''select account, industry, industry_code from employ'''
    update_sql = '''update employ set industry_code = %s where account = %s and industry = %s'''
    cursor = employ_conn.cursor()
    cursor.execute(select_sql)
    results = cursor.fetchall()

    with open("../log/industry", "a") as w:
        for res in results:
            account = res[0]
            industry = res[1]
            industry_code = res[2]
            if industry is not None and industry != '':
                if industry in industry_dict and str(industry_code) == industry_dict[industry]:
                    print(account + '--校验通过！')
                elif industry in industry_dict and str(industry_code) != industry_dict[industry]:
                    print(account + '--代码不匹配！')
                    cursor.execute(update_sql, (industry_dict[industry], account, industry))
                    employ_conn.commit()
                    w.write(account + '修改成功！\n')


if __name__ == '__main__':
    industry_dict = get_industry_dict()
    industry_validate_and_verify(industry_dict)