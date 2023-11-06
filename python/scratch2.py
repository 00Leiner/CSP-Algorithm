from ortools.sat.python import cp_model

class Scheduler:
    def __init__(self, rooms, teachers, program_blocks):
        self.rooms = rooms
        self.teachers = teachers
        self.program_blocks = program_blocks

        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        self.course_assignments = self.define_course_assignments()
        self.define_constraints()

    def define_course_assignments(self):
        course_assignments = {}
        for program_block in self.program_blocks:
            program = program_block['program']
            years = program_block['year']

            for year in years:
                year_blocks = year['year']
                year_blocks += year['blocks']
                courses = year['courses']

                for course in courses:
                    course_code = course['code']
                    course_description = course['description']
                    course_unit = course['unit']

                    for room in self.rooms:
                        room_name = room['name']
                        for day in room['availability']:
                            day_name = day['day']

                            for time_slot in day['time']:
                                var_name = f"{course_code}, {course_description}, {course_unit}, {day_name}, {time_slot}, {room_name}"
                                course_assignments[var_name] = self.model.NewBoolVar(var_name)
                                
        return course_assignments

    def define_constraints(self):
        for program_block in self.program_blocks:
            years = program_block['year']

            for year in years:
                courses = year['courses']

                for course in courses:
                    course_code = course['code']
                    teacher = self.get_teacher_for_course(course_code)
                    # Add constraints related to teacher availability, if needed.
                    
        # Add additional constraints as per your requirements, such as room availability, no overlap, etc.

    def get_teacher_for_course(self, course_code):
        # Implement a method to find and return the teacher for a given course code.
        # You can use the 'teachers' data to look up the teacher based on their preferred courses.
        # You may also want to track teacher assignments and ensure that a teacher isn't assigned to conflicting courses.
        pass

    def solve(self):
        status = self.solver.Solve(self.model)
        if status == cp_model.OPTIMAL:
            self.print_solution()
        else:
            print("No feasible solution found.")

    def print_solution(self):
        for var_name, var in self.course_assignments.items():
            if self.solver.Value(var):
                print(f"Assigned: {var_name}")

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

    scheduler = Scheduler(rooms, teachers, program_blocks)
    scheduler.solve()
