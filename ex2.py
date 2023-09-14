# -*- coding: utf-8 -*-
# @Time : 11/09/2023 23:49
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : ex2.py
# @Project : pycharm
import xml.etree.ElementTree as ET
from datetime import datetime

tasks = set([])
link = '{http://www.xes-standard.org/}'


def log_as_dictionary(log):
    dic_log = {}  # {"case":{"event1"{},"event2"{}}}
    events = log.split("\n")
    for event in events:
        if len(event) < 5 or event[0:4] != "Task":
            continue
        fields = event.split(";")
        tasks.add(fields[0])
        # print(event, "\n", fields)
        if fields[1] not in dic_log.keys():
            dic_log[fields[1]] = {}
        task = {}
        task[fields[0]] = {"users": [fields[2]], "times": [fields[3]]}
        dic_log[fields[1]][fields[0]] = task
    return dic_log


def dependency_graph_inline(log):
    dg = {}
    for case in log.keys():
        events = list(log[case].keys())
        for i in range(len(events)):
            ei = events[i]

            if ei not in dg.keys():
                dg[ei] = {}
            if i == len(events) - 1:
                continue
            ej = events[i + 1]
            if ei == ej:
                continue
            if ej not in dg[ei].keys():
                dg[ei][ej] = 1
            else:
                dg[ei][ej] += 1
    return dg


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
                    e[elem.get('key')] = elem.get('value')
            case[event_no] = e
            event_no += 1
        log[key] = case
    # print(log)
    return log


def dependency_graph_file(log):
    dg = {}
    for case in log.keys():
        events_key = list(log[case].keys())
        # for i in range(len(events_key)):
        #     ei = events_key[i]
        #     if ei not in dg.keys():
        #         dg[ei] = {}
        #     if i == len(events_key) - 1:
        #         continue
        #     ej = events_key[i+1]
        #     if ei == ej:
        #         continue
        #     if ej not in dg[ei].keys():
        #         dg[ei][ej] = 1
        #     else:
        #         dg[ei][ej] += 1
        for i in range(len(events_key)):
            ei = log[case][i]["concept:name"]
            if ei not in dg.keys():
                dg[ei] = {}
            if i == len(events_key) - 1:
                continue
            ej = log[case][i + 1]["concept:name"]
            if ej not in dg[ei].keys():
                dg[ei][ej] = 1
            else:
                dg[ei][ej] += 1
    return dg
