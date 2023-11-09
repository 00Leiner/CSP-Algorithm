from ortools.sat.python import cp_model

def solve_task_assignment():
    # Create a CSP model
    model = cp_model.CpModel()

    # Define variables
    num_tasks = 3
    num_workers = 3
    tasks = range(num_tasks)
    workers = range(num_workers)

    # Variable representing the assignment of tasks to workers
    assignment = {}
    for task in tasks:
        for worker in workers:
            assignment[(task, worker)] = model.NewBoolVar(f'Task_{task}_Worker_{worker}')

    # Each task is assigned to exactly one worker
    for task in tasks:
        model.Add(sum(assignment[(task, worker)] for worker in workers) == 1)

    # Each worker is assigned to exactly one task
    for worker in workers:
        model.Add(sum(assignment[(task, worker)] for task in tasks) == 1)

    # Define the solver
    solver = cp_model.CpSolver()

    # Solve the model
    status = solver.Solve(model)

    # Print the solution
    if status == cp_model.OPTIMAL:
        print('Optimal assignment:')
        for task in tasks:
            for worker in workers:
                if solver.Value(assignment[(task, worker)]) == 1:
                    print(f'Task {task} is assigned to Worker {worker}')
    else:
        print('No optimal assignment found.')

# Call the function to solve the task assignment problem
solve_task_assignment()
