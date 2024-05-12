from pulp import *

problem = LpProblem('Batteries per Hub Optimization', LpMinimize)

Num_of_batteries = LpVariable("Number of Batteries", lowBound=0)
problem += lpSum(Num_of_batteries), 'Objective Function'

