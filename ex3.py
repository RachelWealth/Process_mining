# -*- coding: utf-8 -*-
# @Time : 13/09/2023 12:39
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : ex3.py
# @Project : pycharm
import xml.etree.ElementTree as ET
from datetime import datetime

link = '{http://www.xes-standard.org/}'
T_L = set({})  # The set of all the activities
T_I = set({})   # The set of start activities
T_O = set({})   # The set of end activities
CAUSAL=set() # The set of all causal relationgship elements
CHOICE=set()
X_L = set({})
EVENTS=set()
EVENTS_PER=set()

def define_all_event_permutation():
    for i in range(len(EVENTS)):
        if i == len(case.keys()) - 1:
            continue
        else:
            
        
def casual_per_case(case):
    rt=set()
    # for case in log.keys():
    for i in range(len(case.keys())):
        if i == len(case.keys()) - 1:
            continue
        ei = case[i]
        for j in range(1, len(case.keys())):
            ej = case[j]
            if (ej, ei) not in CAUSAL:
                global CAUSAL.add((ei, ej))
            else:
                global CAUSAL.remove((ej, ei))
def choice_per_case(case):
    for i in range(len(case)):
        if i == len(case.keys()) - 1:
            continue

def alpha(log):
    # log: {"case":{"event1"{},"event2"{}}}
    for case in log.keys():
        T_I.add(case[0]["concept:name"])
        T_O.add(case[len(list(case.keys()))-1]["concept:name"])
        casual_per_case(log)

    pass


def read_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    log = {}  # {"case":{event1:{},event2:{}}
    for trace in root.findall(link + 'trace'):
        event_no = 0
        keys = trace.findall(link + 'string')[0]
        key = keys.get('value')
        if key not in log.keys():
            log[key] = {}
        case = {}
        for event in trace.findall(link + 'event'):
            e = {}
            for elem in event:
                key_event = elem.tag.split('}')[1].split("'")[0]
                if key_event == 'date':
                    input_format = "%Y-%m-%dT%H:%M:%S%z"
                    e[elem.get('key')] = datetime.strptime(elem.get('value'), input_format).replace(tzinfo=None)
                    continue
                if key_event == 'int':
                    e[elem.get('key')] = int(elem.get('value'))
                else:
                    if elem.get('key')=="concept:name":
                        T_L.add(elem.get('value'))
                        # TODO collect all the tasks
                        EVENTS.add(elem.get('value'))

                    e[elem.get('key')] = elem.get('value')
            case[event_no] = e
            event_no += 1
        log[key] = case
    return log

def transition_name_to_id():
    pass