# -*- coding: utf-8 -*-
# @Time : 11/09/2023 23:49
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : exercise2.py
# @Project : pycharm
def log_as_dictionary(log):
    dic_log={}
    events=log.split("\n")
    for event in events:
        fields=event.spil(";")
        if fields[1] not in dic_log.keys():
            dic_log[fiels[1]]=[]
        else: