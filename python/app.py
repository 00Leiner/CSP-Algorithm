from constraint import *

problem = Problem()

# Define variables and domains
students = ['Y_s1', 'Y_s2', 'Y_s3', 'Y_s4', 'Y_s5']
for student in students:
    problem.addVariable(student, [0, 1])

# Define constraints
def student_constraint(*args):
    return sum(args) <= 5

problem.addConstraint(student_constraint, students)

solutions = problem.getSolutions()
print(solutions)