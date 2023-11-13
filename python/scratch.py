from ortools.sat.python import cp_model


class VarArraySolutionCollector(cp_model.CpSolverSolutionCallback):
    """Collect solutions that meet the specified conditions."""

    def __init__(self, variables, assigning_dict):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.assigning_dict = assigning_dict
        self.solutions = []

    def on_solution_callback(self):
        current_solution = {}
        for v in self.variables:
            current_solution[v] = self.Value(v)

        self.solutions.append(current_solution)
        print("Intermediate solution:", current_solution)

    def get_solutions(self):
        return self.solutions



class Scheduler:
    def __init__(self, rooms, program_blocks, teachers):
        self.rooms = rooms
        self.program_blocks = program_blocks
        self.teachers = teachers

        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        self.room_variables = self.define_rooms_variable()
        self.program_block_variables = self.define_program_blocks_variable()
        self.teachers_variables = self.define_teachers_variable()

        assigning = self.assigning()
        self.constraints(assigning)

        self.solve()

    def define_rooms_variable(self):
        room_variables = {}
        for i, room in enumerate(self.rooms):
            room_name = room['name']
            availability = room['availability']
            for day_info in availability:
                day = day_info['day']
                times = day_info['time']
                for time in times:
                    room_variables[(i, day, time)] = self.model.NewBoolVar(f"{room_name}, {day}, {time}")
        return room_variables

    def define_program_blocks_variable(self):
        program_block_variables = {}
        for i, program_block in enumerate(self.program_blocks):
            program = program_block['program']
            years = program_block['year']
            for year in years:
                year_blocks = year['year'] + year['blocks']
                courses = year['courses']
                for course in courses:
                    course_code = course['code']
                    program_block_variables[course_code] = self.model.NewBoolVar(course_code)
        return program_block_variables

    def define_teachers_variable(self):
        teachers_variables = {}
        for i, teacher in enumerate(self.teachers):
            teacher_name = teacher['name']
            teacher_preferred_courses = teacher['preferredCourses']
            for teacher_course in teacher_preferred_courses:
                course_code = teacher_course['code']
                teachers_variables[(i, course_code)] = self.model.NewBoolVar(f"{teacher_name}, {course_code}")
        return teachers_variables

    def assigning(self):
        assigning = {}

        rooms = list(self.room_variables.keys())
        program_blocks = list(self.program_block_variables.keys())
        teachers = list(self.teachers_variables.keys())

        for room_index, room_key in enumerate(rooms):
            for program_block_index, program_block_key in enumerate(program_blocks):
                for teacher_index, teacher_key in enumerate(teachers):
                    assign = (program_block_index, room_index, teacher_index)
                    var = self.model.NewBoolVar(str(assign))
                    assigning[assign] = var

        return assigning

    def constraints(self, assigning):
        # Ensure each room is assigned at most once
        for _, day, time in self.room_variables.keys():
            room_constraints = [assigning[(p, _, t)] for p, _, t in assigning.keys() if _ == day]
            self.model.Add(sum(room_constraints) <= 1)

        # Ensure each program block is assigned at most once
        for p in self.program_block_variables.keys():
            program_block_constraints = [assigning[(p, _, t)] for _, _, t in assigning.keys() if p == _]
            self.model.Add(sum(program_block_constraints) <= 1)

        # Ensure the third item depends on the second item
        for t, course_code in self.teachers_variables.keys():
            for p, _, t1 in assigning.keys():
                self.model.AddImplication(assigning[(p, _, t1)], self.teachers_variables[(t, course_code)])

    def solve(self):
        solution_collector = VarArraySolutionCollector(list(self.assigning().values()), self.assigning())
        status = self.solver.SolveWithSolutionCallback(self.model, solution_collector)

        if status == cp_model.OPTIMAL:
            print("Feasible solutions found. Assignments:")
            for solution in solution_collector.get_solutions():
                valid_solution = True
                for variable, value in solution.items():
                    if value != 1:
                        valid_solution = False
                        break

                if valid_solution:
                    assignment_indices = [i for i, v in enumerate(solution.values()) if v == 1]
                    assignments = [list(self.assigning().keys())[i] for i in assignment_indices]
                    print("Assignment:", assignments)
        else:
            print('No feasible solution found.')


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

  