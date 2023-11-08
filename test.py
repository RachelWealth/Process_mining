# -*- coding: utf-8 -*-
# @Time : 20/09/2023 09:32
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : test.py
# @Project : pycharm

import pm4py

if __name__ == "__main__":
    log = pm4py.read_xes("extension-log-4.xes")
    net = pm4py.discover_heuristics_net(log, dependency_threshold=0.1)
    print(net)
    pm4py.view_heuristics_net(net)