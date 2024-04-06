from ortools.sat.python import cp_model

def limited_assignment(tasks, num_time_slots, lim):
    # Create the CP-SAT solver
    model = cp_model.CpModel()

    # Create the task assignment variables
    task_assignments = {}
    for task in tasks:
        for t in range(num_time_slots):
            task_assignments[task, t] = model.NewBoolVar(f'{task}_at_{t}')

    # Create interval variables for each task
    intervals = {}
    for task in tasks:
        start_var = model.NewIntVar(0, num_time_slots, f'start_{task}')
        end_var = model.NewIntVar(0, num_time_slots, f'end_{task}')
        interval_var = model.NewIntervalVar(start_var, lim[task], end_var, f'interval_{task}')
        intervals[task] = interval_var

    # Add no overlap constraint for intervals of different tasks
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            model.AddNoOverlap([intervals[tasks[i]], intervals[tasks[j]]])

    # Link task assignment variables to interval variables
    for task in tasks:
        for t in range(num_time_slots - lim[task] + 1):
            model.Add(task_assignments[task, t] <= intervals[task].EndExpr() - intervals[task].StartExpr())

    # Each task must be assigned to exactly lim time slots
    for task in tasks:
        model.Add(sum(task_assignments[task, t] for t in range(num_time_slots)) == lim[task])

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Print the assignments
        for task in tasks:
            start = solver.Value(intervals[task].StartExpr())
            assigned_slots = [t for t in range(start, start + lim[task])]
            print(f"{task}: {assigned_slots}")
    else:
        print("No solution found.")

if __name__ == '__main__':
    # Define tasks and number of time slots
    tasks = ['task1', 'task2', 'task3', 'task4']
    num_time_slots = 15
    lim = {'task1': 3, 'task2': 2, 'task3': 3, 'task4': 2}  # Limit of time slots per task

    limited_assignment(tasks, num_time_slots, lim)
