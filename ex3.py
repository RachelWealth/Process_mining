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
X_L = set()
Y_L = set() # non-maximal pairs are removed
F_L=set()
P_L=set()
EVENTS=set()
EVENTS_PRE=set()
idi = 0
ts = {}
ps = {}

def define_all_event_permutation():
    global EVENTS_PRE, EVENTS
    e=list(EVENTS)
    for i in range(len(EVENTS)):
        # if i == len(EVENTS):
          #  break
        for j in range(i,len(EVENTS)):
             EVENTS_PRE.add((e[i],e[j]))
             EVENTS_PRE.add((e[j],e[i]))
        
def casual_per_case(case):
    global CAUSAL
    # for case in log.keys():
    for i in range(len(case.keys())):
        if i == len(case.keys()) - 1:
            continue
        ei = case[i]["concept:name"]
        ej = case[i+1]["concept:name"]
        if (ej, ei) not in CAUSAL:
             CAUSAL.add((ei, ej))
        else:
            CAUSAL.remove((ej, ei))
def choice_per_case(case):
    global CHOICE
    CHOICE = EVENTS_PRE
    for i in range(len(case)):
        if i == len(case.keys()) - 1:
            continue
        CHOICE.discard((case[i]["concept:name"],case[i+1]["concept:name"]))
        CHOICE.discard((case[i+1]["concept:name"],case[i]["concept:name"]))

def define_X_L():
    
    global CHOICE,CAUSAL,EVENTS,X_L
    # initial
    for c in CAUSAL:
        X_L.add((frozenset([c[0]]),frozenset([c[1]])))
    print("first X_L is:", X_L)
    for ei in EVENTS:
        ADD0=True
        ADD1=True
        # iterate all the sets n X_L, check whether they 
        for x in X_L: # (frozenset(),frozenset())
            if ei not in x[0]:
                for ax in x[0]:
                    if (ax,ei) not in CHOICE:
                        ADD0=False
                        break
                for bx in x[1]:
                    if (ei,bx) not in CAUSAL:
                        ADD0=False
                        break
            if ei not in x[1]:
                for ax in x[0]:
                    if(ax,ei) not in CAUSAL:
                        ADD1=False
                        break
                for bx in x[1]:
                    if (ei,bx) not in CHOICE:
                        ADD1=False
                        break
            if ADD0:
                 xi=x[0]
                 set(xi).add(ei)
                 X_L.add((frozenset(xi),x[1]))
            if ADD1:
                xi=x[1]
                set(xi).add(ei)
                X_L.add((x[0],frozenset(xi)))
              
def define_Y_L():
    global X_L,Y_L
    Y_L=X_L
    maxSet = set(list(X_L)[0])
    for x in X_L:
        for mx in maxSet:
            if set(x[0]).issubset(set(mx[0])) and set(x[1]).issubset(set(mx[1])) and x!=mx:
                Y_L.remove(x)
 
"""def P_L():
    global P_L
    P_L.add('i_L')
    P_L.add('o_L')
    """
def define_F_L():
    global F_L
    for x in Y_L:
        for ax in x[0]:
           F_L.add((ax,x))     
        for bx in x[1]:
            F_L.add((x,bx))
    
def alpha(log):
    # log: {"case":{"event1"{},"event2"{}}}
    for case in log.keys():
        T_I.add(log[case][0]["concept:name"])
        T_O.add(log[case][len(list(log[case].keys()))-1]["concept:name"])
        casual_per_case(log[case])
        choice_per_case(log[case])
    define_X_L()
    define_Y_L()
    define_F_L()
    global T_L,F_L, ps, ts
    pn=PetriNet()
    # add transition
    for t in EVENTS:
        pn.add_transition(t, ts[t])
    # add place
    for y in Y_L:
        y_l = list(Y_L)
        for i in range(len(y_l)):
            ps[y_l[i]] = i+1
            pn.add_place(i+1)
    # add edge
    for y in Y_L:
        for ay in y[0]:
            pn.add_edge(ay, ps[y])
        for by in y[1]:
            pn.add_edge( ps[y], by)
    return pn

def tran_dic():
    global ts
    events=list(EVENTS)
    for i in range(len(events)):
        ts[events[i]]=0-i-1

def read_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    log = {}  # {"case":{event1:{},event2:{}}
    global EVENTS
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
    define_all_event_permutation()
    tran_dic()
    return log


class PetriNet():

    def __init__(self):
        # code here
        self.tran = []
        self.pla = [[], []]  # [[places],([place,token]s)]
        self.iedge = [[], []]  # [[source ids],()]
        self.oedge = [[], []]

    def add_place(self, name):
        # code here (name, number of token)
        self.pla[0].append(name)
        self.pla[1].append([name, 0])

    def add_transition(self, name, id):
        # code here
        self.tran.append((name, id))

    def add_edge(self, source, target):
        # code here
        # two edge sets: input (source, tartgets[])
        #                output (source,targets[])
        if source in self.oedge[0]:
            indexs = self.oedge[0].index(source)
            self.oedge[1][indexs].append(target)
        else:
            self.oedge[0].append(source)
            self.oedge[1].append([source, target])

        if target in self.iedge[0]:
            indext = self.iedge[0].index(target)
            self.iedge[1][indext].append(source)
        else:
            self.iedge[0].append(target)
            self.iedge[1].append([target, source])
        return self

    def get_tokens(self, place):
        # code here
        return self.pla[1][self.pla[0].index(place)][1]

    def is_enabled(self, transition):
        # code here
        index = self.iedge[0].index(transition)
        input = self.iedge[1][index][1:]
        # print("Input of transition",transition,"is:",input)
        for i in input:
            if self.pla[1][self.pla[0].index(i)][1] != 0:
                return True
        return False

    def add_marking(self, place):
        # code here
        self.pla[1][self.pla[0].index(place)][1] += 1

    def fire_transition(self, transition):
        # code here
        # first find all the useful place
        inputs = self.iedge[1][self.iedge[0].index(transition)][1:]
        next_marking = self.oedge[1][self.oedge[0].index(transition)][1]
        # Currently, I choose the first place with token
        for input in inputs:
            if self.pla[1][self.pla[0].index(input)][1] != 0:
                self.pla[1][self.pla[0].index(input)][1] -= 1
                self.pla[1][self.pla[0].index(next_marking)][1] += 1
                return
    def transition_name_to_id(s):
        return ts[s]