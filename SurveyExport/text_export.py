#!/usr/bin/env python
# coding=utf-8
# 简答题导出

from data_resource import employ_conn


def text_export_func(paper_id):
    cursor = employ_conn.cursor()
    questions_query = '''select * from question where paper_id = %s and question_type = 4'''
    answers_query = '''select * from anwser where question_id = %s and student_id in %s'''
    cursor.execute(questions_query, paper_id)
    questions = cursor.fetchall()
    index = 1

    for ques in questions:
        question_id = ques[0]
        question_title = ques[4]
        output_file = 'D:\\jianda\\' + str(index) + '.txt'
        with open(output_file, "a") as w:
            student_list_7 = get_student_list_by_category('7')
            student_list_3 = get_student_list_by_category('3')
            student_list_2 = get_student_list_by_category('2')
            student_list_5 = get_student_list_by_category('5')

            cursor.execute(answers_query, (question_id, student_list_7))
            answers_7 = cursor.fetchall()
            cursor.execute(answers_query, (question_id, student_list_3))
            answers_3 = cursor.fetchall()
            cursor.execute(answers_query, (question_id, student_list_2))
            answers_2 = cursor.fetchall()
            cursor.execute(answers_query, (question_id, student_list_5))
            answers_5 = cursor.fetchall()

            print("===============" + question_title + "===============")
            w.write("\n====================================================================\n")
            w.write("题目：" + question_title + "\n")

            w.write("\n-----------------------专硕答案-------------------------\n")
            for a in answers_7:
                w.write(a[5] + '\n')

            w.write("\n-----------------------学硕答案-------------------------\n")
            for a in answers_3:
                w.write(a[5] + '\n')

            w.write("\n-----------------------博士答案-------------------------\n")
            for a in answers_2:
                w.write(a[5] + '\n')

            w.write("\n-----------------------非全答案-------------------------\n")
            for a in answers_5:
                w.write(a[5] + '\n')
        index = index + 1


def get_student_list_by_category(student_category):
    cursor = employ_conn.cursor()
    select_sql = '''select id from student where category = %s'''
    cursor.execute(select_sql, (student_category, ))
    results = cursor.fetchall()
    student_list = []
    for res in results:
        student_list.append(res[0])
    return student_list


if __name__ == '__main__':
    # get_student_list_by_category('7')
    text_export_func(7)
