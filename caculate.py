# -*- coding: utf-8 -*-
# @Time : 11/10/2023 23:13
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : caculate.py
# @Project : pycharm
def f(metrics):
    f_1_1 = sum(m[0] * m[1] for m in metrics)
    f_1_2 = sum(m[0] * m[3] for m in metrics)
    f_2_1 = sum(m[0] * m[2] for m in metrics)
    f_2_2 = sum(m[0] * m[4] for m in metrics)
    print(f_1_1, f_1_2, f_2_1, f_2_2)
    return 0.5 * (2 - f_1_1 / f_1_2 - f_2_1 / f_2_2)


m = [[516, 2, 1, 7, 6],
     [246, 2, 2, 9, 8],
     [235, 2, 2, 8, 8]]

print(round(f(m), 5))
