# -*- coding: utf-8 -*-
# @Time : 12/09/2023 13:09
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : ex2_main.py
# @Project : pycharm
from ex2 import log_as_dictionary
from ex2 import dependency_graph_inline
from ex2 import read_from_file
from ex2 import dependency_graph_file

f = """
Task_A;case_1;user_1;2019-09-09 17:36:47
Task_B;case_1;user_3;2019-09-11 09:11:13
Task_D;case_1;user_6;2019-09-12 10:00:12
Task_E;case_1;user_7;2019-09-12 18:21:32
Task_F;case_1;user_8;2019-09-13 13:27:41

Task_A;case_2;user_2;2019-09-14 08:56:09
Task_B;case_2;user_3;2019-09-14 09:36:02
Task_D;case_2;user_5;2019-09-15 10:16:40

Task_G;case_1;user_6;2019-09-18 19:14:14
Task_G;case_2;user_6;2019-09-19 15:39:15
Task_H;case_1;user_2;2019-09-19 16:48:16
Task_E;case_2;user_7;2019-09-20 14:39:45
Task_F;case_2;user_8;2019-09-22 09:16:16

Task_A;case_3;user_2;2019-09-25 08:39:24
Task_H;case_2;user_1;2019-09-26 12:19:46
Task_B;case_3;user_4;2019-09-29 10:56:14
Task_C;case_3;user_1;2019-09-30 15:41:22"""

log = log_as_dictionary(f)
dg = dependency_graph_inline(log)

for ai in sorted(dg.keys()):
   for aj in sorted(dg[ai].keys()):
       print (ai, '->', aj, ':', dg[ai][aj])


log = read_from_file("extension-log.xes")

# general statistics: for each case id the number of events contained
# for case_id in sorted(log):
#     print((case_id, len(log[case_id])))

# details for a specific event of one case
case_id = "case_123"
event_no = 0
print((log[case_id][event_no]["concept:name"], log[case_id][event_no]["org:resource"], log[case_id][event_no]["time:timestamp"],  log[case_id][event_no]["cost"]))

dg = dependency_graph_file(log)

for ai in sorted(dg.keys()):
   for aj in sorted(dg[ai].keys()):
       print (ai, '->', aj, ':', dg[ai][aj])