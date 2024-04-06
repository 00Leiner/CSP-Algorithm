from ortools.sat.python import cp_model

def solve_task_assignment(num_tasks, num_people, task_requirements, people_capabilities):
    # Create the CP-SAT solver
    model = cp_model.CpModel()

    # Create binary decision variables for task assignments
    task_assignments = {}
    
    for i in range(num_tasks):
        for j in range(num_people):
            task_assignments[i, j] = model.NewBoolVar(f'task_{i}_to_person_{j}')

    # Add constraints to ensure each task is assigned to exactly one person
    for i in range(num_tasks):
        model.Add(sum(task_assignments[i, j] for j in range(num_people)) == 1)

    # Add constraints based on task requirements and people capabilities
    for i in range(num_tasks):
        for j in range(num_people):
            if task_requirements[i] > people_capabilities[j]:
                model.Add(task_assignments[i, j] == 0)

    # Add constraints to limit the number of times each person is assigned a task
    for j in range(num_people):
        model.Add(sum(task_assignments[i, j] for i in range(num_tasks)) <= 5)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print("Task Assignments:")
        for i in range(num_tasks):
            for j in range(num_people):
                if solver.Value(task_assignments[i, j]) == 1:
                    print(f"Task_{i} assigned to Person_{j}")
    else:
        print("No solution found.")
        
    # Print the solver's response for debugging
    print("Solver status:", solver.StatusName(status))

if __name__ == '__main__':
    num_tasks = 3  # Number of tasks
    num_people = 2  # Number of people
    
    # Task requirements and people capabilities
    task_requirements = [3, 2, 4]  # Each task's requirement
    people_capabilities = [1, 3]  # Each person's capability
    
    solve_task_assignment(num_tasks, num_people, task_requirements, people_capabilities)
