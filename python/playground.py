from ortools.sat.python import cp_model

def solve_class_scheduling(teachers, rooms, students):
    # Create the CP-SAT model
    model = cp_model.CpModel()

    # Define variables
    teacher_subjects = {teacher: model.NewIntVar(1, len(students), f'{teacher}_subject') for teacher in teachers}
    student_rooms = {student: model.NewIntVar(1, len(rooms), f'{student}_room') for student in students}

    # Add constraints: Each teacher is assigned a subject they prefer
    for teacher in teachers:
        model.AddElement(teacher_subjects[teacher], students).in_([teacher_preferences[teacher]])

    # Add constraints: Each student is assigned to an available room
    for student in students:
        model.AddElement(student_rooms[student], rooms).in_([student_preferences[student]])

    # Ensure that subjects, rooms, and students are all assigned uniquely
    model.AddAllDifferent(list(teacher_subjects.values()))
    model.AddAllDifferent(list(student_rooms.values()))

    # Create a solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        # Print the solution
        for teacher in teachers:
            print(f'Teacher {teacher} is assigned subject {solver.Value(teacher_subjects[teacher])}')
        for student in students:
            print(f'Student {student} is assigned to room {solver.Value(student_rooms[student])}')
    else:
        print('No solution found.')

# Example preferences (subject/room indices start from 1)
teacher_preferences = {'Teacher1': 2, 'Teacher2': 1, 'Teacher3': 3}
student_preferences = {'Student1': 2, 'Student2': 1, 'Student3': 3}

# Example resources (subject/room indices start from 1)
available_rooms = ['Room1', 'Room2', 'Room3']
available_students = ['Student1', 'Student2', 'Student3']
available_teachers = ['Teacher1', 'Teacher2', 'Teacher3']

# Solve the class scheduling problem
solve_class_scheduling(available_teachers, available_rooms, available_students)
