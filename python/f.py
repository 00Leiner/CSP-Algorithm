from ortools.sat.python import cp_model

class Scheduler:
    def __init__(self, rooms, program_blocks, teachers):
        self.rooms = rooms
        self.program_blocks = program_blocks
        self.teachers = teachers

        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        # Create variables for rooms, program blocks, and teachers
        self.room_variables = self.define_rooms_variable()
        self.program_block_variables = self.define_program_blocks_variable()
        self.teachers_variables = self.define_teachers_variable()

        # Define schedule as a dictionary to hold variables
        self.schedule = self.define_assignment()

    def define_rooms_variable(self):
        room_variables = []

        for room in self.rooms:
            room_name = room['name']
            availability = room['availability']
            for day_info in availability:
                day = day_info['day']
                times = day_info['time']
                for time in times:
                    room_variables.append((room_name, day, time))

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

                    program_block_variables.append((program_year_blocks, course_code))

        return program_block_variables
    
    def define_teachers_variable(self):
        teachers_variables = []

        for teacher in self.teachers:
            teacher_name = teacher['name']
            teacher_preferred_courses = teacher['preferredCourses']
            for teacher_course in teacher_preferred_courses:
                course_code = teacher_course['code']

                teachers_variables.append((teacher_name, course_code))

        return teachers_variables

    def define_assignment(self):
        schedule = {}

        for program_block in self.program_block_variables:
            program = program_block[0]
            course_code = program_block[1]
            # Unique value of course_code
            course_var = self.model.NewBoolVar(f"course_{course_code}")
            schedule[('course', course_code)] = course_var

        for room in self.room_variables:
            room_name = room[0]
            day = room[1]
            time = room[2]
            # Unique value of room_name
            room_var = self.model.NewBoolVar(f"room_{room_name}")
            schedule[('room', room_name)] = room_var

        for teacher in self.teachers_variables:
            teacher_name = teacher[0]
            teacher_course = teacher[1]
                # Unique value of teacher_name
            teacher_var = self.model.NewBoolVar(f"teacher_{teacher_name}")
            schedule[('teacher', teacher_name)] = teacher_var

        if course_code == teacher_course:
            sched_var = (course_code, day, time, room_name, teacher_name)
            var = self.model.NewBoolVar(str(sched_var))
            schedule[sched_var] = var

        # Add constraint to ensure uniqueness for each variable
        self.model.AddImplication(var, course_var.Not())
        self.model.AddImplication(var, room_var.Not())
        self.model.AddImplication(var, teacher_var.Not())

        return schedule


    def solve(self):
        status = self.solver.Solve(self.model)

        print(f"Solver Status: {status}")

        self.interpret_schedule()

    def interpret_schedule(self):
        for key, var in self.schedule.items():
            print(f"{key}, {self.solver.Value(var)}")


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
    scheduler.solve()


