from logic import *

color = ['Red', 'Blue', 'Green', 'Yellow']

symbols = []

knowledge = And()

for c in color:
    for i in range(4):
        symbols.append(Symbol(f"{c}{i}"))

# Only one position per color
for c in color:
    for i in range(4):
        for j in range(4):
            if i != j:
                knowledge.add(Implication(Symbol(f"{color}{i}"),Not(Symbol(f"{color}{i}"))))

#Only one color per color
for i in range(4):
    for c1 in color:
        for c2 in color:
            if c1 != c2:
                knowledge.add(Implication(Symbol(f"{c1}{i}"),Not(Symbol(f"{c2}{i}"))))


# Condition 1: Two are correct two are not
knowledge.add(Or(
    And(Symbol('Red0'), Symbol('Blue1'), Not(Symbol('Green2')), Not(Symbol('Yellow3'))),
    And(Symbol('Red0'), Symbol('Green2'), Not(Symbol('Blue1')), Not(Symbol('Yellow3'))),
    And(Symbol('Red0'), Symbol('Yellow3'), Not(Symbol('Blue1')), Not(Symbol('Green2'))),
    And(Symbol('Blue1'), Symbol('Green2'), Not(Symbol('Red0')), Not(Symbol('Yellow3'))),
    And(Symbol('Blue1'), Symbol('Yellow3'), Not(Symbol('Red0')), Not(Symbol('Green2'))),
    And(Symbol('Green2'), Symbol('Yellow3'), Not(Symbol('Red0')), Not(Symbol('Blue1'))),
))

# Condition 2: None are correct
knowledge.add(And(
    Not(Symbol('Blue2')),Not(Symbol('Red1')),Not(Symbol('Green2')),Not(Symbol('Yellow3'))
))

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)

