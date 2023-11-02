from ortools.sat.python import cp_model

class Scheduler:
    def __init__(self, rooms, teachers, program_blocks):
        
        self.rooms = rooms
        self.teachers = teachers
        self.program_blocks = program_blocks

        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        # Define variables and domain for teachers, students, rooms, and time slots.
        self.available_teachers = self.define_teacher_variables()
        self.available_courses = self.define_student_variables()
        self.available_rooms = self.define_room_variables()

        # Define constraints based on your scheduling rules.
        self.define_teacher_preferred_courses_constraints()
        self.define_student_constraints()
        self.define_room_constraints()

    def define_teacher_variables(self):
        # Define teacher assignment variables.
        available_teachers = {}

        for teacher in teachers:
            teacher_name = teacher['name']
            teacher_preferredCourses = teacher['preferredCourses']

            for teacher_courses in teacher_preferredCourses:
                t_code = teacher_courses['code']
                t_description = teacher_courses['description']
                t_unit = teacher_courses['units']

                var_name = f"{teacher_name}_{t_code}"
                available_teachers[(teacher_name, t_code)] = self.model.NewBoolVar(var_name)
        
        #for key, value in available_teachers.items():
        #    print(f"Key: {key}, Value: {value}")

        return available_teachers       

    def define_student_variables(self):
        # Define student assignment variables.
        available_courses = {}

        for program_block in program_blocks:
            prgram = program_block['program']
            years = program_block['year']
            
            for year in years:
                programBlock = year['year']
                programBlock += year['blocks']
                courses = year['courses']

                for course in courses:
                    c_code = course['code']
                    c_description = course['description']
                    c_unit = course['unit']

                    var_name = f"{prgram}_{programBlock}_{c_code}"
                    available_courses[(prgram, programBlock, c_code)] = self.model.NewBoolVar(var_name)
        
        #for key, value in available_courses.items():
        #    print(f"Key: {key}, Value: {value}")

        return available_courses  

    def define_room_variables(self):
        # Define room assignment variables.
        available_rooms = {}
        
        for room in rooms:
            room_name = room['name']
            room_availability = room['availability']
            
            for availability in room_availability:
                day = availability['day']
                time_slots = availability['time']
                
                for time in time_slots:
                    var_name = f"{room_name}_{day}_{time}"
                    available_rooms[(room_name, day, time)] = self.model.NewBoolVar(var_name)
        
        #for key, value in available_rooms.items():
        #    print(f"Key: {key}, Value: {value}")

        return available_rooms

    def define_teacher_preferred_courses_constraints(self):
        available_teachers = self.available_teachers
        available_courses = self.available_courses

        for teacher in available_teachers:
            teacher_name = teacher[0]
            t_code = teacher[1]

            for course in available_courses:
                program, year_block, c_code = course

                if t_code == c_code:
                    self.model.Add(available_teachers[(teacher_name, c_code)] == available_courses[course])
                    #print(f"Teacher: {teacher_name}, Course: {c_code}, Program: {program} {year_block}")
                    
    def define_student_constraints(self):
        pass

    def define_room_constraints(self):
        available_rooms = self.available_rooms

        for room in available_rooms:
            room_name, day, time = room
            

    def solve(self):
        # Solve the CSP problem.
        status = self.solver.Solve(self.model)

        if status == cp_model.FEASIBLE:
            # Interpret and output the solution.
            self.interpret_schedule()
        else:
            print("No solution found.")

    def interpret_schedule(self):
        # Interpret the solution to get the schedules for teachers, students, rooms, and time slots.
        pass
 