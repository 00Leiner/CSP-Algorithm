from ortools.sat.python import cp_model

def create_schedule(teachers, program_blocks, rooms):
    model = cp_model.CpModel()

    # Create Boolean variables to represent the assignment of each class to each room
    teacher_course_vars = {}
    for teacher in teachers:
        for course in teacher['preferredCourses']:
            for program_block in program_blocks:
                for year in program_block['year']:
                    for block in year['blocks']:
                        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"]:
                            for time in rooms[0]['availability'][0]['time']:
                                key = (teacher['name'], course['code'], program_block['program'], year['year'], block, day, time)
                                teacher_course_vars[key] = model.NewBoolVar(f'{key}_assigned')

    # Ensure that each class is assigned to one and only one room
    for teacher in teachers:
        for course in teacher['preferredCourses']:
            for program_block in program_blocks:
                for year in program_block['year']:
                    for block in year['blocks']:
                        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"]:
                            for time in rooms[0]['availability'][0]['time']:
                                key = (teacher['name'], course['code'], program_block['program'], year['year'], block, day, time)
                                model.Add(sum(teacher_course_vars[key] for key in teacher_course_vars) == 1)

    # Rest of your constraints and objectives

    # Solve the model
    solver = cp_model.CpSolver()
    solver.Solve(model)

    # Extract the solution
    assignments = {}
    for key, var in teacher_course_vars.items():
        if solver.Value(var) == 1:
            assignments[key] = var

    return assignments

if __name__ == '__main__':
    rooms = [
        {
            'name': "room1",
            'availability': [
                {
                    'day': "Monday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Tuesday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Wednesday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Thursday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Friday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Sunday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                }
                # Add more availability
            ]
        },
        {
            'name': "room2",
            'availability': [
                {
                    'day': "Monday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Tuesday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Wednesday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Thursday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Friday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                },
                {
                    'day': "Sunday",
                    'time': [ '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                             '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
                             '13:00', '13:30', '14:00', '14:30','15:00', '15:30', 
                             '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', 
                             '19:00', '19:30', '20:00', '12:30' ],
                }
                # Add more availability
            ]
        },
        # Add more rooms
    ]

    teachers = [
        {
            'name': "teacher1",
            'preferredCourses': [
                {
                    'code': "IT 4102",
                    'description': "Mobile App Development",
                    'units': "3" 
                },
                {
                    'code': "IT 1101",
                    'description': "Information Technology Fundamentals",
                    'units': "3" 
                },
                {
                    'code': "CS 5204",
                    'description': "Data Mining",
                    'units': "3" 
                },
                # Add more courses
            ]
        },
        {
            'name': "teacher2",
            'preferredCourses': [
                {
                    'code': "CS 2107", 
                    'description': "Data Structures and Algorithm", 
                    'units': 3
                },
                {
                    'code': "IT 2105", 
                    'description': "System Analysis and Design", 
                    'units': 3
                },
                {
                    'code': "IT 2207", 
                    'description': "Web Development", 
                    'units': 3
                },
                    # Add more subjects here
            ]
        },
        # Add more teachers
    ]

    program_blocks = [
        {
            'program': "BSCS",
            'year': [
                {
                    'year': "1",
                    'blocks': "A",
                    'courses': [
                        {
                            'code': "CS 2107",
                            'description': "Data Structures and Algorithm",
                            'unit': "3",
                        },
                        {
                            'code': "CS 2201",
                            'description': "Database Systems",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                },
                {
                    'year': "1",
                    'blocks': "B",
                    'courses': [
                        {
                            'code': "CS 2107",
                            'description': "Data Structures and Algorithm",
                            'unit': "3",
                        },
                        {
                            'code': "CS 2201",
                            'description': "Database Systems",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                },
                # Add more year
            ]
        },
        {
            'program': "BSIT",
            'year': [
                {
                    'year': "1",
                    'blocks': "A",
                    'courses': [
                        {
                            'code': "IT 1101",
                            'description': "Information Technology Fundamentals",
                            'unit': "3",
                        },
                        {
                            'code': "IT 1203",
                            'description': "Database Management Systems",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                },
                {
                    'year': "1",
                    'blocks': "B",
                    'courses': [
                        {
                            'code': "IT 1101",
                            'description': "Information Technology Fundamentals",
                            'unit': "3",
                        },
                        {
                            'code': "IT 1203",
                            'description': "Database Management Systems",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                },
                # Add more year
            ]
        }
        # Add more programs
    ]

    schedule = create_schedule(teachers, program_blocks, rooms)
    if schedule:
        for (teacher, course, program, year, block, day, time) in schedule:
            print(f'Teacher: {teacher}, Course: {course}, Program: {program}, Year: {year}, Block: {block}, Day: {day}, Time: {time}')
    else:
        print('No feasible solution found.')
