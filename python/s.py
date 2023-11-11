from ortools.sat.python import cp_model

class ThreeVarStringSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions for a CSP problem with three string variables."""

    def __init__(self, people, fruits, places, preferences):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__people = people
        self.__fruits = fruits
        self.__places = places
        self.__preferences = preferences
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f'Solution {self.__solution_count}:')
        for person in self.__people:
            for fruit in self.__fruits:
                for place in self.__places:
                    if self.Value(self.__preferences[(person, fruit, place)]) == 1:
                        print(f'{person} prefers {fruit} and likes to be at {place}')
        print()

    def solution_count(self):
        return self.__solution_count

def solve_preferences():
    # Create a CP model
    model = cp_model.CpModel()

    # Define people, fruits, and places
    people = ['John', 'Bryan', 'Mark']
    fruits = ['Apple', 'Orange', 'Banana']
    places = ['park', 'house', 'court']

    # Create variables with bounds corresponding to the indices
    preferences = {}
    for person in people:
        for fruit in fruits:
            for place in places:
                preferences[(person, fruit, place)] = model.NewBoolVar(f'{person}_{fruit}_{place}')

    # Add constraints
    for person in people:
        model.Add(sum(preferences[(person, fruit, place)] for fruit in fruits for place in places) == 1)

    # Example constraint: Mark specifically prefers Banana and likes to be at the park
    model.Add(preferences[('Mark', 'Banana', 'park')] == 1)

    # Create a solver
    solver = cp_model.CpSolver()

    # Create a solution printer
    solution_printer = ThreeVarStringSolutionPrinter(people, fruits, places, preferences)

    # Solve the problem and print all solutions
    solver.SearchForAllSolutions(model, solution_printer)

    if solution_printer.solution_count() == 0:
        print('No solutions found.')

# Solve and print all possible solutions for the preferences problem
solve_preferences()
