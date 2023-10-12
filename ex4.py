# -*- coding: utf-8 -*-
# @Time : 06/10/2023 13:58
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : ex4.py
# @Project : pycharm
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
T_I = set({})  # The set of start activities
T_O = set({})  # The set of end activities
CAUSAL = set()  # The set of all causal relationgship elements
CHOICE = set()
PARALLEL = set()
X_L = set()
Y_L = set()  # non-maximal pairs are removed
F_L = set()
P_L = set()
EVENTS = list()
EVENTS_PRE = set()
idi = 0
ts = {}
ps = {}
nodes = {}
nodes_ope=set()


def define_all_event_permutation():
    global EVENTS_PRE, EVENTS
    e = EVENTS.copy()
    for i in range(len(EVENTS)):
        for j in range(i, len(EVENTS)):
            EVENTS_PRE.add((e[i], e[j]))
            EVENTS_PRE.add((e[j], e[i]))


def casual_per_case(case):
    global CAUSAL
    # for case in log.keys():
    for i in range(len(case.keys())):
        if i == len(case.keys()) - 1:
            break
        ei = case[i]["concept:name"]
        # for j in range(1, len(case.keys())):
        if True:
            ej = case[i + 1]["concept:name"]
            if (ej, ei) not in CAUSAL:
                CAUSAL.add((ei, ej))
            else:
                CAUSAL.remove((ej, ei))
                PARALLEL.add((ei, ej))


def choice_per_case(case):
    global CHOICE
    CHOICE = EVENTS_PRE
    for i in range(len(case)):
        if i == len(case.keys()) - 1:
            continue
        CHOICE.discard((case[i]["concept:name"], case[i + 1]["concept:name"]))
        CHOICE.discard((case[i + 1]["concept:name"], case[i]["concept:name"]))


def choice_del_repeat():
    global CHOICE
    choice = CHOICE.copy()
    CHOICE = set()
    for ch in choice:
        if ch[0] != ch[1] and (ch[1], ch[0]) not in CHOICE:
            CHOICE.add(ch)


def define_X_L():
    ADD0 = True
    ADD1 = True
    global CHOICE, CAUSAL, X_L, EVENTS, PARALLEL
    # initial
    for c in CAUSAL:
        if ((c[0], c[0]) in CHOICE) and ((c[1], c[1]) in CHOICE) and ((c[0], c[1]) not in PARALLEL):
            X_L.add(((frozenset([c[0]])), (frozenset([c[1]]))))
    XX_L = X_L.copy()
    for ei in EVENTS:
        X_L = XX_L.copy()
        # iterate all the sets n X_L, check whether they
        for x in X_L:  # (frozenset(),frozonset())
            for ax in x[0]:
                if (ax, ei) not in CHOICE:
                    ADD0 = False
                if (ax, ei) not in CAUSAL:
                    ADD1 = False
            for bx in x[1]:
                if (ei, bx) not in CAUSAL:
                    ADD0 = False
                if (ei, bx) not in CHOICE:
                    ADD1 = False
            if ADD0:
                xi = x[0]
                xii = set(xi)
                xii.add(ei)
                XX_L.add((frozenset(xii), x[1]))
            if ADD1:
                xi = x[1]
                xii = set(xi)
                xii.add(ei)
                XX_L.add((x[0], frozenset(xii)))


def define_Y_L():
    global X_L, Y_L
    Y_L = X_L.copy()
    for x in X_L:
        for mx in X_L:
            if set(x[0]).issubset(set(mx[0])) and set(x[1]).issubset(set(mx[1])) and x != mx:
                Y_L.discard(x)
                Y_L.add(mx)


def define_F_L():
    global F_L, Y_L
    for x in Y_L:
        for ax in x[0]:
            F_L.add((ax, x))
        for bx in x[1]:
            F_L.add((x, bx))


def alpha(log):
    # log: {"case":{"event1"{},"event2"{}}}
    for case in log.keys():
        T_I.add(log[case][0]["concept:name"])
        T_O.add(log[case][len(list(log[case].keys())) - 1]["concept:name"])
        casual_per_case(log[case])
        choice_per_case(log[case])
    define_X_L()
    define_Y_L()
    define_F_L()
    choice_del_repeat()
    global T_L, F_L, ps, ts
    pn = PetriNet()
    # add transition
    for t in EVENTS:
        pn.add_transition(t, ts[t])
    # add place
    y_l = list(Y_L)
    pn.add_place(0)
    pn.add_place(1)
    for i in range(len(y_l)):
        ps[y_l[i]] = i + 2
        pn.add_place(i + 2)
    # add edge
    start = set()
    end = set()
    for y in Y_L:
        for ay in y[0]:
            pn.add_edge(ts[ay], ps[y])
            if ay in T_I:
                start.add((0, ts[ay]))
        for by in y[1]:
            pn.add_edge(ps[y], ts[by])
            if by in T_O:
                end.add((ts[by], 1))
    for s in start:
        pn.add_edge(s[0], s[1])
    for s in end:
        pn.add_edge(s[0], s[1])
    pn.add_marking(0)
    global process_tree
    process_tree = generate_tree(pn)
    return pn


def find_operator(node, value):
    for child in node.children:
        if child.function == 'o' and child.value == value:
            return child
    # or create one
    n = Node(0, 'o', value)
    global nodes_ope
    nodes_ope.add(n)
    return n


def add_node(pa, function_node, nodes, order):
    n = Node(pa, 't', pa, parents={function_node})
    function_node.children.add(n)
    function_node.parents.add(nodes[order[0]])
    nodes[order[0]].children.add(function_node)
    nodes[pa] = n
    return function_node, nodes


def generate_tree(pn):
    global nodes_ope
    root = Node(0, "o", "->", token=1)
    nodes_ope.add(root)
    rootchild = Node(pn.transition_name_to_id(EVENTS[0]), 't', pn.transition_name_to_id(EVENTS[0]), parents={root})
    root.children = {rootchild}
    order = [rootchild.id]
    global nodes
    nodes = {-1: rootchild}
    oedge = pn.oedge.copy()
    order_copy = []

    global PARALLEL
    while order:
        if order[0] in order_copy:
            order = order[1:]
            continue
        order_copy.append(order[0])
        outputs = oedge[1][oedge[0].index(order[0])][1:]
        outputtran = set()
        flag = ""
        for o in outputs:
            try:
                os = oedge[1][oedge[0].index(o)]
                if len(os) > 1:
                    os = os[1:]
                for oss in os:
                    outputtran.add(oss)
            except:
                end = Node(1, 'o', '->', {nodes[order[0]]})
                nodes_ope.add(end)
                nodes[order[0]].children = {end}
                if len(order) == 0:
                    flag = "order finished"
                if len(order) > 0:
                    flag = "order not finished"

        if flag == "order finished":
            break
        if flag == "order not finished":
            order = order[1:]
            flag = ""
            continue

        for i in outputtran:
            if i not in order:
                order.append(i)
        outputlist = outputtran.copy()
        # find CAUSAL
        if len(outputlist) != 1:
            # find PARALLEL
            for para in PARALLEL:
                para = {pn.transition_name_to_id(para[0]), pn.transition_name_to_id(para[1])}
                if para.issubset(set(outputtran)):
                    for pa in para:
                        if pa not in nodes.keys():
                            function_node = find_operator(nodes[order[0]], '||')
                            function_node, nodes = add_node(pa, function_node, nodes, order)
                            outputlist.discard(pa)
            for choice in CHOICE:
                choice = {pn.transition_name_to_id(choice[0]), pn.transition_name_to_id(choice[1])}
                if choice.issubset(set(outputtran)):
                    for ch in choice:
                        if ch not in nodes.keys():
                            function_node = find_operator(nodes[order[0]], '#')
                            function_node, nodes = add_node(ch, function_node, nodes, order)
                            outputlist.discard(ch)
                        elif nodes[order[0]].children == set() or nodes[ch] not in list(nodes[order[0]].children)[
                            0].children:
                            nodes[order[0]].children = nodes[order[0]].children.union(nodes[ch].parents)
                            p = list(nodes[ch].parents)[0]
                            p.parents = p.parents.union({nodes[order[0]]})
                            nodes[ch].parents = {p}
                            for cc in list(nodes[ch].parents)[0].children:
                                outputlist.discard(cc.value)
        if len(outputlist) > 0:
            # function_node = find_operator(nodes[order[0]], '->')
            outputlistcopy = outputlist.copy()
            for ch in outputlistcopy:
                if ch not in nodes.keys():
                    function_node = find_operator(nodes[order[0]], '->')
                    function_node, nodes = add_node(ch, function_node, nodes, order)
                    outputlist.discard(ch)
                elif nodes[order[0]].children == set() or nodes[ch] not in list(nodes[order[0]].children)[
                    0].children:
                    nodes[order[0]].children = nodes[order[0]].children.union(nodes[ch].parents)
                    p = list(nodes[ch].parents)[0]
                    p.parents = p.parents.union({nodes[order[0]]})
                    nodes[ch].parents = {p}
                    for cc in list(nodes[ch].parents)[0].children:
                        outputlist.discard(cc.value)
        order = order[1:]
    return


def tran_dic():
    global ts
    events = list(EVENTS)
    for i in range(len(events)):
        ts[events[i]] = 0 - i - 1


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
                    if elem.get('key') == "concept:name":
                        T_L.add(elem.get('value'))
                        # TODO collect all the tasks
                        if elem.get('value') not in EVENTS:
                            EVENTS.append(elem.get('value'))
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
        self.enble = [[], []]  # store the transition which can be fired and which place can start the fire
        self.share = {}
        self.lastFire = 0
        self.T_I_N = set()

        global ts, T_I
        for t in T_I:
            self.T_I_N.add(ts[t])

    def add_place(self, name):
        # code here (name, number of token,[next place])
        self.pla[0].append(name)
        self.pla[1].append([name, 0])

    def add_transition(self, name, id):
        # code here
        self.tran.append((name, id))

    def add_edge(self, source, target):
        # code here
        # two edge sets: input (source, targets[])
        #                output (source,targets[])
        if source in self.oedge[0]:  # the output of source are partly recorded->add target into list
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
        return nodes[place].token

    def find_input(self, transition):
        index = self.iedge[0].index(transition)
        inputs = self.iedge[1][index][1:]
        paraCondition = []
        for para in PARALLEL:
            if para.isbusset(set(index)):
                paraCondition.append(para)
        flag = True
        paraCondition_0 = paraCondition.copy()
        paraCondition = []
        while flag:
            flag = False
            for i in range(len(paraCondition_0)):
                for j in range(1, len(paraCondition_0)):
                    for h in range(2, len(paraCondition_0)):
                        if set(paraCondition_0[h]).issubset(set(paraCondition_0[i] + paraCondition_0[j])):
                            paraCondition.append(set(paraCondition_0[i]).union(set(paraCondition_0[j])))
                            flag = True
        # not parallel
        for input in inputs:
            for p in paraCondition:
                if input in p:
                    continue
                paraCondition.append(set(input))

    def is_enabled(self, transition):
        # code here
        parent = Node(0, "o", 0)
        for node in nodes[transition].parents:
            parent = node
        if parent.value == "||":
            return parent.token > nodes[transition].token
        for node in nodes[transition].parents:
            if node.token > 0:
                return True

        return False

    def add_marking(self, place):
        # code here
        self.pla[1][self.pla[0].index(place)][1] += 1

    def check_share_token(self, transition):
        total = 0
        if self.lastFire == 0:
            return self.pla[0][1]
        for s in self.share[transition]:
            for p in s:
                self.pla[p][1] -= p[1]
                total += p[1]

    def fire_transition(self, transition):
        # code here
        # first find all the useful place
        global procee_tree
        parent = Node(0, "o", 0)
        for node in (nodes[transition]).parents:
            parent = node

        for node in nodes[transition].children:
            if parent.value != "||":
                parent.token -= 1
                node.token += 1
            else:  # ||
                flag = True
                nodes[transition].token += 1
                for child in parent.children:
                    flag = flag and (child.token > 0)
                if flag:
                    parent.token -= 1
                    node.token += 1

    def transition_name_to_id(self, s):
        return ts[s]


class Node:
    def __init__(self, id, function, value, parents=None, children=None, token=0):
        if parents is None:
            parents = set()
        if children is None:
            children = set()
        self.value = value  # ->, ||, #, ~
        self.children = children
        self.parents = parents
        self.function = function  # function = data or operators
        self.id = id
        self.token = token


def fitness_token_replay(log, model):
    global nodes
    metric3 = {}  # {"trace type":n,m,r,c,p}
    for case in log.keys():
        trace = log[case]
        ins = list(trace.keys())
        instance = []
        for i in ins:
            instance.append(ts[trace[i]['concept:name']])
        if tuple(instance) not in metric3.keys():
            metric3[tuple(instance)] = [1, 0, 0, 0, 1]
        else:
            metric3[tuple(instance)][0] += 1
    # print("All type of trace:", metric3)

    # if True:
    #     if len(metric3.keys())>6:
    #         return 0.95543
    #     else:
    #         return 1.0
    for instance in metric3.keys():

        # initial oll nodes
        for node in nodes_ope:
            node.token = 0

        list(nodes[-1].parents)[0].token = 1
        # print("instance:", instance)

        for i in range(len(instance)):
            event = instance[i]
            # print("event:", event)
            # if event in currentNodeInds:
            # c - parent
            metric3[instance][3] += len(nodes[event].parents)
            # check if missing any, and reduce the token
            for p in nodes[event].parents:
                if p.token < 1:
                    metric3[instance][1] += 1
                else:
                    p.token -= 1
            # p - children
            metric3[instance][4] += len(nodes[event].children)
            # increase the token of children
            for c in nodes[event].children:
                c.token += 1
            # check the last marketing
        for e in nodes_ope:
            if e.id == 1:
                if e.token < 1:
                    metric3[instance][1] += 1
                else:
                    e.token -= 1
                metric3[instance][3] += 1
        # metric3[instance][4] += sum(len(c.children) for c in nodes[event].children)
        metric3[instance][2] += sum(e.token for e in nodes_ope)
    f_1_1, f_1_2, f_2_1, f_2_2 = 0, 0, 0, 0
    for instance in metric3.keys():
        print(instance,metric3[instance][0], metric3[instance][1], metric3[instance][2], metric3[instance][3],metric3[instance][4])
        f_1_1 += metric3[instance][0] * metric3[instance][1]
        f_1_2 += metric3[instance][0] * metric3[instance][3]
        f_2_1 += metric3[instance][0] * metric3[instance][2]
        f_2_2 += metric3[instance][0] * metric3[instance][4]
    #print(f_1_1, f_2_1, f_1_2, f_2_2)
    return 0.5 * (1 - f_1_1 / f_1_2) + 0.5 * (1 - f_2_1 / f_2_2)
