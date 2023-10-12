# -*- coding: utf-8 -*-
# @Time : 20/09/2023 09:32
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : test.py
# @Project : pycharm

import pm4py

if __name__ == "__main__":
    log = pm4py.read_xes('extension-log-4.xes')
    process_model = pm4py.discover_bpmn_inductive(log)
    pm4py.view_bpmn(process_model)