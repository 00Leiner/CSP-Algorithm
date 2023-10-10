from constraint import *

problem = Problem()
n = 4  # Size of the magic square (4x4)

# Add variables with values from 1 to 16
problem.addVariables(range(n * n), range(1, n * n + 1))

# Add constraints
problem.addConstraint(AllDifferentConstraint(), range(n * n))
problem.addConstraint(ExactSumConstraint(34), [0, 5, 10, 15])
problem.addConstraint(ExactSumConstraint(34), [3, 6, 9, 12])

# Add row and column constraints
for row in range(n):
    problem.addConstraint(ExactSumConstraint(34), [row * n + i for i in range(n)])

for col in range(n):
    problem.addConstraint(ExactSumConstraint(34), [col + n * i for i in range(n)])

solutions = problem.getSolutions()
print(solutions)