from ortools.sat.python import cp_model

class Scheduler:
    def __init__(self, rooms, program_blocks, teachers):
        self.rooms = rooms
        self.program_blocks = program_blocks
        self.teachers = teachers

        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        # Create variables for rooms and program blocks
        self.room_variables = self.define_rooms_variable()
        self.program_block_variables = self.define_program_blocks_variable()
        self.teachers_variables = self.define_teachers_variable()

        self.assignment = {}

    def define_rooms_variable(self):
        room_variables = []

        for room in self.rooms:
            room_name = room['name']
            availability = room['availability']
            for day_info in availability:
                day = day_info['day']
                time = day_info['time']
                for t in time:
                    room_variables.append({
                        'room_name': room_name,
                        'day': day,
                        'time': t
                    })

        return room_variables

    def define_program_blocks_variable(self):

        program_block_variables = []

        for program_block in self.program_blocks:
            program = program_block['program']
            years = program_block['year']

            for year in years:
                year_blocks = year['year'] + year['blocks']
                courses = year['courses']
                program_year_blocks = f"{program} {year_blocks}"
                for course in courses:
                    course_code = course['code']

                    program_block_variables.append({
                        'program' : program_year_blocks,
                        'course code' : course_code
                    })

        return program_block_variables
    
    def define_teachers_variable(self):
        teachers_variables = []

        for teachers in self.teachers:
            teacher_name = teachers['name']
            teacher_preferred_courses = teachers['preferredCourses']
            for teacher_courses in teacher_preferred_courses:
                course_code = teacher_courses['code']

                teachers_variables.append({
                    'name' : teacher_name,
                    'course code' : course_code
                })

        return teachers_variables

    def define_assignment(self):
        

        for program_blocks in self.program_block_variables:
            program = program_blocks['program']
            course_code = program_blocks['course code']

            for rooms in self.room_variables:
                room_name = rooms['room_name']
                day = rooms['day']
                time = rooms['time'] 

                for teachers in self.teachers_variables:
                    teacher_name = teachers['name']
                    t_course_code = teachers['course code']

                    if t_course_code == course_code:
                        sched_var = f"{program}, {course_code}, {day}, {time}, {room_name}, {teacher_name} "
                        var = self.model.NewBoolVar(sched_var)
                        self.model.Add(var == 1)  
                        self.assignment[( sched_var )] = var

    def room_constraints(self):
        for rooms in self.room_variables:
            time = rooms['time']
            for program_blocks in self.program_block_variables:
                self.model.Add(sum(self.assignment.get(f"{program_blocks['program']}, {program_blocks['course code']}, {rooms['day']}, {time}, {rooms['room_name']}, {teachers['name']}", 0) for teachers in self.teachers_variables) == 1)

    def solve(self):

        status = self.solver.Solve(self.model)

        if status == cp_model.OPTIMAL:
            self.interpret_schedule()

    def interpret_schedule(self):
        for key, var in self.assignment.items():
            if self.solver.Value(var) == 1:
                print(f"{key}")

if __name__ == "__main__":
    
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
                {
                    'code': "CS 2201",
                    'description': "Database Systems",
                    'unit': "3",
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
                {
                    'code': "CS 3105",
                    'description': "Operating Systems",
                    'unit': "3",
                },
                    # Add more subjects here
            ]
        },
        {
            'name': "teacher3",
            'preferredCourses': [
                {
                    'code': "CS 3203",
                    'description': "Software Engineering",
                    'unit': "3",
                },
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
                {
                    'code': "CS 5102",
                    'description': "Web Development",
                    'unit': "3",
                },
                    # Add more subjects here
            ]
        },
        {
            'name': "teacher4",
            'preferredCourses': [
                {
                    'code': "IT 1203",
                    'description': "Database Management Systems",
                    'unit': "3",
                },
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
                {
                    'code': "IT 4204",
                    'description': "Cloud Computing",
                    'unit': "3",
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

    scheduler = Scheduler(rooms, program_blocks, teachers)
    scheduler.define_assignment()
    scheduler.solve()

