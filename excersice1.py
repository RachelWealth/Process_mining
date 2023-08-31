# -*- coding: utf-8 -*-
# @Time : 30/08/2023 10:58
# @Author :Rachel Duan
# @Email : rachel_duanyingli@163.com
# @File : excersice1.py
# @Project : pycharm

class PetriNet():

    def __init__(self):
        # code here
        self.tran=[]
        self.pla=[[],[]] # [[places],([place,token]s)]
        self.iedge=[[],[]] # [[source ids],()]
        self.oedge=[[],[]]
        self.enble=[[],[]] # store the transition which can be fired and which place can start the fire

    def add_place(self, name):
        # code here (name, number of token)
        self.pla[0].append(name)
        self.pla[1].append((name,0))

    def add_transition(self, name, id):
        # code here
        self.tran.append((name,id))

    def add_edge(self, source, target):
        # code here
        # two edge sets: input (source, tartgets[])
        #                output (source,targets[])
        if source in self.oedge[0]:
            indexs=self.oedge[0].index(source)
            self.oedge[indexs + 1].append(target)
        else:
            self.oedge[0].append(source)

        if target in self.iedge[0]:
            indext=self.iedge[0].index(target)
            self.iedge[indext + 1].append(source)
        else:
            self.iedge[0].append(target)
        return self


    def get_tokens(self, place):
        # code here
        return self.pla[1][self.pla[0].index[place]+1][1]

    def is_enabled(self, transition):
        # code here
        index = self.iedge[0].index(transition)
        input = self.iedge[index][1:]
        print("Input of transition",transition,"is:",input)
        for i in input:
            if self.pla[1][self.pla[0].index(i)+1][1]!=0:
                print(True)
                return
        print(False)

    def add_marking(self, place):
        # code here
        self.pla[1][self.pla[0].index(place)+1][1]+=1

    def fire_transition(self, transition):
        # code here
        # first find all the useful place
        inputs = self.iedge[1][self.iedge[0].index(transition)][1:]
        # Currently, I choose the first place with token
        for input in inputs:
            if self.pla[1][self.pla[0].index[input]+1][1]!=0:
                self.pla[1][self.pla[0].index[input] + 1][1]-=1
                return


# etc

p = PetriNet()

p.add_place(1)  # add place with id 1
p.add_place(2)
p.add_place(3)
p.add_place(4)
p.add_transition("A", -1)  # add transition "A" with id -1
p.add_transition("B", -2)
p.add_transition("C", -3)
p.add_transition("D", -4)

p.add_edge(1, -1)
p.add_edge(-1, 2)
p.add_edge(2, -2).add_edge(-2, 3)
p.add_edge(2, -3).add_edge(-3, 3)
p.add_edge(3, -4)
p.add_edge(-4, 4)

print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.add_marking(1)  # add one token to place id 1
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-1)  # fire transition A
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-3)  # fire transition C
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-4)  # fire transition D
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.add_marking(2)  # add one token to place id 2
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-2)  # fire transition B
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-4)  # fire transition D
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# by the end of the execution there should be 2 tokens on the final place
print(p.get_tokens(4))