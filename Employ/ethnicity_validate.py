#!/usr/bin/env python
# coding=utf-8
# 民族代码验证

from data_resource import employ_conn


def get_ethnicity_dict():
    cursor = employ_conn.cursor()
    select_sql = '''select * from basic where type = 'ethnicity' and status = 1'''
    cursor.execute(select_sql)
    results = cursor.fetchall()
    ethnicity_dict = {}
    for res in results:
        code = res[1]
        name = res[2]
        ethnicity_dict.update({name: code})

    return ethnicity_dict


def ethnicity_validate_and_verify(ethnicity_dict):
    select_sql = '''select username, ethnicity, ethnicity_code from student'''
    update_sql = '''update student set ethnicity_code = %s where username = %s and ethnicity = %s'''
    cursor = employ_conn.cursor()
    cursor.execute(select_sql)
    results = cursor.fetchall()
    # output_file = r"G:\ethnicity.txt"
    with open("../log/ethnicity", "a") as w:
        for res in results:
            username = res[0]
            ethnicity = res[1]
            ethnicity_code = res[2]
            if ethnicity is not None and ethnicity != '':
                if ethnicity in ethnicity_dict and str(ethnicity_code) == ethnicity_dict[ethnicity]:
                    print(username + '--校验通过！')
                    w.write(username + '--校验通过！\n')
                elif ethnicity in ethnicity_dict and str(ethnicity_code) != ethnicity_dict[ethnicity]:
                    print(username + '--代码不匹配！')
                    cursor.execute(update_sql, (ethnicity_dict[ethnicity], username, ethnicity))
                    employ_conn.commit()
                    w.write(username + '修改成功！\n')


if __name__ == '__main__':
    ethnicity_dict = get_ethnicity_dict()
    ethnicity_validate_and_verify(ethnicity_dict)