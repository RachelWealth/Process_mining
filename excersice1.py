# -*- coding: utf-8 -*-
# @Time : 30/08/2023 10:58
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : excersice1.py
# @Project : pycharm

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
