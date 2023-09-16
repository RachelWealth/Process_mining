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
X_L = set((set(),set()))
Y_L = set((set(),set())) # non-maximal pairs are removed
EVENTS=set()
EVENTS_PRE=set()

def define_all_event_permutation(log):
    for i in range(len(EVENTS)):
        if i == len(case.keys()) - 1:
            continue
        else:
            EVENTS_PRE.add((case[i]["concept:name"],case[i+1]["concept:name"]))
            
        
def casual_per_case(case):
    rt=set()
    # for case in log.keys():
    for i in range(len(case.keys())):
        if i == len(case.keys()) - 1:
            continue
        ei = case[i]["concept:name"]
        for j in range(1, len(case.keys())):
            ej = case[j]["concept:name"]
            if (ej, ei) not in CAUSAL:
                global CAUSAL.add((ei, ej))
            else:
                global CAUSAL.remove((ej, ei))
def choice_per_case(case):
    global CHOICE = EVENTS_PRE
    for i in range(len(case)):
        if i == len(case.keys()) - 1:
            continue
        CHOICE.remove((case[i]["concept:name"],case[j]["concept:name"]))
        CHOICE.remove((case[j]["concept:name"],case[i]["concept:name"]))

def X_L():
    A=set()
    B=set()
    ADD0=True
    ADD1=True
    global CHOICE
    global CAUSAL
    global EVENTS
    # initial
    X_L.add(((list(CHOICE)[0]),(list(CHOICE)[1])))
    print("first X_L is:", X_L)
    for ei in EVENTS:
        # iterate all the sets n X_L, check whether they 
        for x in X_L:# (set(),set())
            if ei not in x[0]:
                for ax in x[0]:
                    if (ax,ei) not in CHOICE:
                        ADD0=False
                    if(ax,ei) not in CAUSAL:
                        ADD1=False
                for bx in x[1]:
                    if (ei,bx) not in CAUSAL:
                        ADD0=False
                    if (ei,bx) not in CHOICE:
                        ADD1=False
                if ADD0:
                    X_L.add((x[0].add(ei),x[1]))
                if ADD:
                    X_L.add((x[0],x[1].add(ei)))
              
def Y_L():
    global X_L
    maxSet =set(list(X_L)[0])
    for x in X_L:
        for mx in maxSET:
            if x[0].issubset(mx[0]) and x[1].issubset(mx[1]) and x!=mx:
                X_L.remove(x)
                                
      
    
    
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
    define_all_event_permutation(log)
    return log

def transition_name_to_id():
    pass