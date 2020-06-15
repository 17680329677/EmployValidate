#!/usr/bin/env python
# coding=utf-8

from data_resource import employ_conn


def get_area_code_dict():
    print('开始获取地区原始数据')
    cursor = employ_conn.cursor()
    select_province_sql = '''select * from area where type = 1'''
    cursor.execute(select_province_sql)
    province_results = cursor.fetchall()
    area_dict = {}
    for province in province_results:
        province_code = province[1]
        province_name = province[2]
        area_dict.update({province_name: province_code})
        select_city_sql = '''select * from area where type = 2 and citycode = %s'''
        cursor.execute(select_city_sql, (province_code,))
        city_results = cursor.fetchall()
        for city in city_results:
            city_code = city[1]
            city_name = city[2]
            area_dict.update({province_name + city_name: city_code})
    print('加载地区原始数据完毕')
    return area_dict


def addr_update(addr_type, student_code, addr, addr_code):
    cursor = employ_conn.cursor()
    if addr_type == 'enrollment_addr':
        update_sql = '''update student set enrollment_addr = %s, enrollment_code = %s where username = %s'''
        cursor.execute(update_sql, (addr, addr_code, student_code))
        employ_conn.commit()
    # '''select account, implement_comp_addr, implement_comp_code from record'''
    elif addr_type == 'implement_comp_addr':
        update_sql = '''update record set implement_comp_code = %s where account = %s and implement_comp_addr = %s'''
        cursor.execute(update_sql, (addr_code, student_code, addr))
        employ_conn.commit()
    # company_addr, company_addr_code
    elif addr_type == 'company_addr':
        update_sql = '''update employ set company_addr_code = %s where account = %s and company_addr = %s'''
        cursor.execute(update_sql, (addr_code, student_code, addr))
        employ_conn.commit()


def addr_validate_and_verify(addr_type, sql_sentence, area_dict):
    cursor = employ_conn.cursor()
    cursor.execute(sql_sentence)
    results = cursor.fetchall()
    output_file = '../log' + addr_type
    with open(output_file, "a") as w:
        for res in results:
            student_code = res[0]
            addr = res[1]
            addr_code = res[2]
            if addr is None or addr == '':
                print(student_code + '--未填写')
            elif addr in area_dict and addr_code == area_dict[addr]:
                print(student_code + '--校验通过！')
            elif addr + '省' in area_dict and addr_code == area_dict[addr + '省']:
                print(student_code + '--校验通过！')
                addr_update(addr_type, student_code, addr + '省', area_dict[addr + '省'])
                w.write(student_code + '--修改成功！\n')
            elif addr in area_dict and addr_code != area_dict[addr]:
                print(student_code + '--代码不正确')
                # TODO： 更新
                addr_update(addr_type, student_code, addr, area_dict[addr])
                w.write(student_code + '--修改成功！\n')
            elif addr + '省' in area_dict and addr_code != area_dict[addr + '省']:
                # TODO： 更新
                print(student_code + '--代码不正确')
                addr_update(addr_type, student_code, addr + '省', area_dict[addr + '省'])
                w.write(student_code + '--修改成功！\n')


if __name__ == '__main__':
    enrollment_addr = '''select username, enrollment_addr, enrollment_code from student'''
    implement_comp_addr = '''select account, implement_comp_addr, implement_comp_code from record'''
    company_addr = '''select account, company_addr, company_addr_code from employ'''
    area_dict = get_area_code_dict()
    addr_validate_and_verify('enrollment_addr', enrollment_addr, area_dict)
    addr_validate_and_verify('implement_comp_addr', implement_comp_addr, area_dict)
    addr_validate_and_verify('company_addr', company_addr, area_dict)
