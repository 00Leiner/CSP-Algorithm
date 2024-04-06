from ortools.sat.python import cp_model

def consecutive_assignment(tasks, num_time_slots):
    # Create the CP-SAT solver
    model = cp_model.CpModel()
    
    # Create the interval variables for each task
    intervals = {}
    for task in tasks:
        start_var = model.NewIntVar(0, num_time_slots, f'start_{task}')
        end_var = model.NewIntVar(0, num_time_slots, f'end_{task}')
        interval_var = model.NewIntervalVar(start_var, 3, end_var, f'interval_{task}')
        intervals[task] = interval_var
    
    # No overlapping intervals
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            model.AddNoOverlap([intervals[tasks[i]], intervals[tasks[j]]])
    
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        # Print the assignments
        for task in tasks:
            start = solver.Value(intervals[task].StartExpr())
            end = solver.Value(intervals[task].EndExpr())
            print(f"{task}: {[t for t in range(start, start + 3)]}")
    else:
        print("No solution found.")

if __name__ == '__main__':
    # Define tasks
    tasks = ['task1', 'task2', 'task3', 'task4', 'task5']
    num_time_slots = 12  # Ensure that there are enough time slots for all tasks
    
    consecutive_assignment(tasks, num_time_slots)
