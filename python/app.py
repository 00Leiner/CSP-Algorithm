from ortools.sat.python import cp_model

class AllSolutionsCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.solutions = []
        
    def on_solution_callback(self):
        solution = [self.Value(var) for var in self.variables]
        self.solutions.append(solution)

def main():
    # Create a new CP-SAT model
    model = cp_model.CpModel()

    # Define the domains of the variables
    A = model.NewIntVar(0, 5, 'A')
    B = model.NewIntVar(0, 5, 'B')
    C = model.NewIntVar(0, 5, 'C')

    # Define a constraint: A + B == C
    model.Add(A + B == C)

    # Create a solver
    solver = cp_model.CpSolver()

    # Create a solution collector
    variables = [A, B, C]
    collector = AllSolutionsCollector(variables)
    solver.SearchForAllSolutions(model, collector)

    print("All solutions:")
    for solution in collector.solutions:
        print(f'A = {solution[0]}, B = {solution[1]}, C = {solution[2]}')

if __name__ == '__main__':
    main()
