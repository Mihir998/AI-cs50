from pomegranate import *

# Mother and Father nodes has no parents
mother = Node(DiscreteDistribution({
    "0": 0.96,
    "1": 0.03,
    "2": 0.01
}), name="mother")

father = Node(DiscreteDistribution({
    "0": 0.96,
    "1": 0.03,
    "2": 0.01
}), name="father")

#print(rain.distribution)

# Mother trait and Father trait nodes are conditional on mother and father nodes resp.
mothertrait = Node(ConditionalProbabilityTable([
    ["0", "yes", 0.01],
    ["0", "no", 0.99],
    ["1", "yes", 0.56],
    ["1", "no", 0.44],
    ["2", "yes", 0.65],
    ["2", "no", 0.35]
], [mother.distribution]), name="mothertrait")

fathertrait = Node(ConditionalProbabilityTable([
    ["0", "yes", 0.01],
    ["0", "no", 0.99],
    ["1", "yes", 0.56],
    ["1", "no", 0.44],
    ["2", "yes", 0.65],
    ["2", "no", 0.35]
], [father.distribution]), name="fathertrait")

#mothertrait.distribution
#print(mothertrait.distribution)

#mother_mutate = 0.01
#mother_without_mutate = 0.99

#father_mutate = 0.01
#father_without_mutate = 0.99

# Child node is conditional on mother and father
child = Node(ConditionalProbabilityTable([
    ["0", "0", "0", (0.99*0.99)],
    ["0", "0", "1", (0.01*0.99) + (0.99*0.01)],
    ["0", "0", "2", (0.01*0.01)],

    ["0", "1", "0", (0.99*0.5*0.99) + (0.99*0.5*0.01)],
    ["0", "1", "1", (0.99*0.01*0.5) + (0.99*0.99*0.5) + (0.01*0.99*0.5) + (0.01*0.01*0.5)],
    ["0", "1", "2", (0.01*0.5*0.01) + (0.01*0.5*0.99)],

    ["0", "2", "0", (0.99*0.01)],
    ["0", "2", "1", (0.01*0.01) + (0.99*0.99)],
    ["0", "2", "2", (0.01*0.99)],

    ["1", "0", "0", (0.99*0.5*0.99) + (0.99*0.5*0.01)],
    ["1", "0", "1", (0.99*0.01*0.5) + (0.99*0.99*0.5) + (0.01*0.99*0.5) + (0.01*0.01*0.5)],
    ["1", "0", "2", (0.01*0.5*0.01) + (0.01*0.5*0.99)],

    ["1", "1", "0", (0.99*0.5*0.99*0.5) + (0.99*0.5*0.01*0.5) + (0.01*0.5*0.99*0.5) + (0.01*0.5*0.01*0.5)],
    ["1", "1", "1", (0.01*0.5*0.99*0.5) + (0.99*0.5*0.99*0.5) + (0.01*0.5*0.99*0.5) + (0.99*0.5*0.99*0.5)],
    ["1", "1", "2", (0.01*0.5*0.01*0.5) + (0.01*0.5*0.99*0.5) + (0.99*0.5*0.01*0.5) + (0.99*0.5*0.99*0.5)],

    ["1", "2", "0", (0.99*0.5*0.01) + (0.01*0.5*0.01)],
    ["1", "2", "1", (0.01*0.5*0.01) + (0.99*0.5*0.01)+(0.99*0.5*0.99)],
    ["1", "2", "2", (0.01*0.5*0.99) + (0.99*0.5*0.99)],

    ["2", "0", "0", (0.99*0.01)],
    ["2", "0", "1", (0.01*0.01) +  (0.99*0.99)],
    ["2", "0", "2", (0.01*0.99)],

    ["2", "1", "0", (0.99*0.5*0.01) + (0.01*0.5*0.01)],
    ["2", "1", "1", (0.01*0.5*0.01) + (0.99*0.5*0.01)+(0.99*0.5*0.99)],
    ["2", "1", "2", (0.01*0.5*0.99) + (0.99*0.5*0.99)],

    ["2", "2", "0", (0.01*0.01)],
    ["2", "2", "1", (0.01*0.99) + (0.01*0.99)],
    ["2", "2", "2", (0.99*0.99)]
], [mother.distribution, father.distribution]), name="child")

#print(train.distribution)

# Appointment node is conditional on train
childtrait = Node(ConditionalProbabilityTable([
    ["0", "yes", 0.01],
    ["0", "no", 0.99],
    ["1", "yes", 0.56],
    ["1", "no", 0.44],
    ["2", "yes", 0.65],
    ["2", "no", 0.35]
], [child.distribution]), name="childtrait")

#print(childtrait.distribution)

# Create a Bayesian Network and add states
model = BayesianNetwork()
model.add_states(mother, father, mothertrait, fathertrait, child, childtrait)

# Add edges connecting nodes
model.add_edge(mother, mothertrait)
model.add_edge(father, fathertrait)
model.add_edge(mother, child)
model.add_edge(father, child)
model.add_edge(child, childtrait)

# Finalize model
model.bake()
