# -*- coding: utf-8 -*-
# @Time : 06/10/2023 13:59
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : ex4_main.py
# @Project : pycharm
from ex4 import read_from_file
from ex4 import alpha
from ex4 import fitness_token_replay

log = read_from_file("extension-log-4.xes")
log_noisy = read_from_file("extension-log-noisy-4.xes")

mined_model = alpha(log)
print(round(fitness_token_replay(log, mined_model), 5))
print(round(fitness_token_replay(log_noisy, mined_model), 5))