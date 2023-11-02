from ortools.sat.python import cp_model

def teacher_assignment():
    rooms = [
        {
            'name': "room1",
            'availability': [
                {
                    'day': "Monday",
                    'time': [ '07:00', '07:30', '08:00', '08:30' ],
                },
                {
                    'day': "Tuesday",
                    'time': [ '07:00', '07:30', '08:00', '08:30' ],
                }
                # Add more availability
            ]
        },
        {
            'name': "room2",
            'availability': [
                {
                    'day': "Monday",
                    'time': [ '07:00', '07:30', '08:00', '08:30' ],
                },
                {
                    'day': "Tuesday",
                    'time': [ '07:00', '07:30', '08:00', '08:30' ],
                }
                # Add more availability
            ]
        }
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
        }
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
                    'year': "2",
                    'blocks': "A",
                    'courses': [
                        {
                            'code': "CS 3105",
                            'description': "Operating Systems",
                            'unit': "3",
                        },
                        {
                            'code': "CS 3203",
                            'description': "Software Engineering",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                },
                {
                    'year': "3",
                    'blocks': "A",
                    'courses': [
                        {
                            'code': "CS 4109",
                            'description': "Computer Networks",
                            'unit': "3",
                        },
                        {
                            'code': "CS 4207",
                            'description': "Artificial Intelligence",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                },
                {
                    'year': "4",
                    'blocks': "A",
                    'courses': [
                        {
                            'code': "CS 5102",
                            'description': "Web Development",
                            'unit': "3",
                        },
                        {
                            'code': "CS 5204",
                            'description': "Data Mining",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                }
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
                    'year': "2",
                    'blocks': "A",
                    'courses': [
                        {
                            'code': "IT 2105",
                            'description': "System Analysis and Design",
                            'unit': "3",
                        },
                        {
                            'code': "IT 2207",
                            'description': "Web Development",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                },
                {
                    'year': "3",
                    'blocks': "A",
                    'courses': [
                        {
                            'code': "IT 3109",
                            'description': "Software Engineering",
                            'unit': "3",
                        },
                        {
                            'code': "IT 3201",
                            'description': "Computer Networks",
                            'unit': "3",
                        },
                        # Add more courses
                    ]
                },
                {
                    'year': "4",
                    'blocks': "A",
                    'courses': [
                        {
                            'code': "IT 4102",
                            'description': "Mobile App Development",
                            'unit': "3",
                        },
                        {
                            'code': "IT 4204",
                            'description': "Cloud Computing",
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

    model = cp_model.CpModel()
    
    # Create a variable for each teacher-course combination
    teacher_vars = {}
    for teacher in teachers:
        for course in teacher['preferredCourses']:
            teacher_vars[(teacher['name'], course['code'])] = model.NewBoolVar(f"{teacher['name']}_{course['code']}")
    
    # Create a variable for each course
    course_vars = {}
    for block in program_blocks:
        for year in block['year']:
            for course in year['courses']:
                course_vars[course['code']] = model.NewBoolVar(course['code'])
    
    # Define constraints for teacher preferences
    for (teacher_name, course_code), var in teacher_vars.items():
        for teacher in teachers:
            if teacher['name'] == teacher_name:
                course_codes = [c['code'] for c in teacher['preferredCourses']]
                if course_code not in course_codes:
                    model.Add(var == 0)
    
    # Define constraints to ensure that each course has a teacher
    for course_code, var in course_vars.items():
        teacher_count = sum(teacher_vars[(teacher['name'], course_code)] for teacher in teachers)
        model.Add(teacher_count == 1)
    
    # Define the objective function (optional) to maximize or minimize based on your criteria
    # For example, you can minimize the total number of teachers assigned to undesired courses.
    # model.Minimize(sum(teacher_vars[(teacher['name'], course['code'])] for teacher in teachers for course in teacher['preferredCourses']))
    
    # Create a solver and solve the CSP problem
    solver = cp_model.CpSolver()
    solver.Solve(model)
    
    # Get the teacher assignments
    teacher_assignments = {}
    for (teacher_name, course_code), var in teacher_vars.items():
        if solver.Value(var) == 1:
            teacher_assignments[course_code] = teacher_name
    
    return teacher_assignments

# Run the teacher assignment function
teacher_assignments = teacher_assignment()

# Print the results
for course_code, teacher_name in teacher_assignments.items():
    print(f"Course: {course_code}, Teacher: {teacher_name}")
