from ortools.sat.python import cp_model

# Define rooms, days, and capacities
rooms = ['Room1', 'Room2']
days = ['Monday', 'Tuesday', 'Wednesday']
capacity = {'Room1': 2, 'Room2': 3}

# Create CP-SAT solver
model = cp_model.CpModel()
solver = cp_model.CpSolver()

# Define variables
events = {}
for room in rooms:
    for day in days:
        events[(room, day)] = model.NewIntVar(0, capacity[room], f'events_{room}_{day}')
        
        

# Add capacity constraints
for room in rooms:
    for day in days:
        model.Add(events[(room, day)] <= capacity[room])

# Solve the model
solver.Solve(model)

# Print the solution
for room in rooms:
    for day in days:
        print(f'{room} on {day}: {events[(room, day)].SolutionValue()} events')
