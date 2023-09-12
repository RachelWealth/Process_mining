from excersice1 import PetriNet
# etc

p = PetriNet()

p.add_place(1)

p.add_place(2)

p.add_place(3)

p.add_place(4)

p.add_place(5)

p.add_place(6)

p.add_transition("A", -1)

p.add_transition("B", -2)

p.add_transition("C", -3)

p.add_transition("D", -4)

p.add_edge(1, -1)

p.add_edge(-1, 2).add_edge(2, -2).add_edge(-2, 4).add_edge(4, -4)

p.add_edge(-1, 3).add_edge(3, -3).add_edge(-3, 5).add_edge(5, -4)

p.add_edge(-4, 6)

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