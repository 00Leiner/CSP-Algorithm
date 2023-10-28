from ortools.sat.python import cp_model

def send_more_money():
    model = cp_model.CpModel()

    # Create variables for each letter (S, E, N, D, M, O, R, Y).
    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
    digit_vars = {letter: model.NewIntVar(0, 9, letter) for letter in letters}

    # Create the constraints for the problem.
    model.Add(digit_vars['S'] > 0)  # S must be nonzero.
    model.Add(digit_vars['M'] > 0)  # M must be nonzero.
    model.Add(digit_vars['S'] * 1000 + digit_vars['E'] * 100 + digit_vars['N'] * 10 + digit_vars['D'] +
              digit_vars['M'] * 1000 + digit_vars['O'] * 100 + digit_vars['R'] * 10 + digit_vars['E'] ==
              digit_vars['M'] * 10000 + digit_vars['O'] * 1000 + digit_vars['N'] * 100 + digit_vars['E'] * 10 + digit_vars['Y'])

    # Create the solver and solve the problem.
    solver = cp_model.CpSolver()
    solution_printer = cp_model.VarArrayAndObjectiveSolutionPrinter(list(digit_vars.values()))
    
    status = solver.SearchForAllSolutions(model, solution_printer)
    
    if status == cp_model.OPTIMAL:
        print("Solution found:")
        for letter in letters:
            print(f"{letter}: {digit_vars[letter].Value()}")

send_more_money()
