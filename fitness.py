# -*- coding: utf-8 -*-
# @Time : 11/10/2023 23:52
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : fitness.py
# @Project : pycharm

import pm4py
import os
from pm4py.objects.log.importer.xes import importer as xes_importer

# Load the log file
log_test = xes_importer.apply('extension-log-noisy-4.xes')

# Define the process model or use a pre-built model
log = pm4py.read_xes("extension-log-4.xes")
process_model, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)

replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log_test, process_model, initial_marking, final_marking)
fitness = pm4py.fitness_token_based_replay(log_test, process_model,initial_marking, final_marking )
print(replayed_traces[565])
print(replayed_traces)
print("Fitness:", fitness )

