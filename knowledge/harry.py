# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 12:47:54 2022

@author: Dell
"""


from logic import *

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

knowledge = And(
    Implication(Not(rain), hagrid),
    Or(hagrid, dumbledore),
    Not(And(hagrid, dumbledore)),
    dumbledore
    )

print(model_check(knowledge, rain))

P = Symbol("It is a Tuesday")
Q = Symbol("It is Raining")
R = Symbol("Harry will go for run")

knowledge1 = And(Implication(And(P, Not(Q)),R),
                 P,
                 Not(Q))

print(knowledge1)