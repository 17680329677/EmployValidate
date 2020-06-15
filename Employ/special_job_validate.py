#!/usr/bin/env python
# coding=utf-8
# 特殊就业类别代码验证 special_job

from data_resource import employ_conn


def get_special_job_dict():
    cursor = employ_conn.cursor()
    select_sql = '''select * from basic where type = 'specialEmployType' and status = 1'''
    cursor.execute(select_sql)
    results = cursor.fetchall()
    special_job_dict = {}
    for res in results:
        code = res[1]
        name = res[2]
        special_job_dict.update({name: code})
    # print(special_job_dict)
    return special_job_dict


def special_job_validate_and_verify(special_job_dict):
    select_sql = '''select account, special_job, special_job_code from employ'''
    update_sql = '''update employ set special_job_code = %s where account = %s and special_job = %s'''
    cursor = employ_conn.cursor()
    cursor.execute(select_sql)
    results = cursor.fetchall()

    with open("../log/special_job", "a") as w:
        for res in results:
            account = res[0]
            special_job = res[1]
            special_job_code = res[2]
            if special_job is not None and special_job != '':
                if special_job in special_job_dict and str(special_job_code) == special_job_dict[special_job]:
                    print(account + '--校验通过！')
                elif special_job in special_job_dict and str(special_job_code) != special_job_dict[special_job]:
                    print(account + '--代码不匹配！')
                    cursor.execute(update_sql, (special_job_dict[special_job], account, special_job))
                    employ_conn.commit()
                    w.write(account + '修改成功！\n')


if __name__ == '__main__':
    special_job_dict = get_special_job_dict()
    special_job_validate_and_verify(special_job_dict)