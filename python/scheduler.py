from ortools.sat.python import cp_model

class Scheduler:
    def __init__(self, programs, years, blocks, subjects_per_program):
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.programs = programs
        self.years = years
        self.blocks = blocks
        self.subjects_per_program = subjects_per_program
        self.subject_vars = {}

    def create_programBlock_variables(self):
        for program in self.programs:
            for year in self.years:
                num_blocks = self.blocks.get(program, {}).get(year, 1)
                year_block_names = [chr(ord('a') + i) for i in range(num_blocks)]
                for block in year_block_names:
                    variable_name = f"{program} {year}{block}"
                    var = self.model.NewBoolVar(variable_name)
                    self.subject_vars[variable_name] = var

    def solve_variables(self):
        self.create_programBlock_variables()
        self.solver.Solve(self.model)

    def get_solution(self):
        return self.subject_vars

    def print_programBlocks(self):
        for program in self.programs:
            for year in self.years:
                num_blocks = self.blocks.get(program, {}).get(year, 1)
                year_block_names = [chr(ord('a') + i) for i in range(num_blocks)]
                for block in year_block_names:
                    print(f"{program} {year}{block}")
                    for subject in self.subjects_per_program[program][year]:
                        variable_name = f"{program} {year}{block}"
                        value = self.solver.Value(self.subject_vars[variable_name])
                        print(f"Subject {subject}: {value}")

if __name__ == "__main__":
    programs = ["BSCS", "BSIT"]
    years = ["1st", "2nd", "3rd", "4th"]
    subjects_per_program = {
        "BSCS": {
            "1st": ["Subject1", "Subject2", "Subject3", "Subject4", "Subject5"],
            "2nd": ["Subject6", "Subject7", "Subject8", "Subject9", "Subject10"],
            "3rd": ["Subject11", "Subject12", "Subject13", "Subject14", "Subject15"],
            "4th": ["Subject16", "Subject17", "Subject18", "Subject19", "Subject20"]
        },
        "BSIT": {
            "1st": ["SubjectA", "SubjectB", "SubjectC", "SubjectD", "SubjectE"],
            "2nd": ["SubjectF", "SubjectG", "SubjectH", "SubjectI", "SubjectJ"],
            "3rd": ["SubjectK", "SubjectL", "SubjectM", "SubjectN", "SubjectO"],
            "4th": ["SubjectP", "SubjectQ", "SubjectR", "SubjectS", "SubjectT"]
        }
    }

    # Specify the maximum number of blocks for each program and year
    blocks = {
        "BSCS": {
            "1st": 1,
            "2nd": 2,
            "3rd": 3,
            "4th": 1
        },
        "BSIT": {
            "1st": 2,
            "2nd": 1,
            "3rd": 3,
            "4th": 2
        }
    }

    scheduler = Scheduler(programs, years, blocks, subjects_per_program)
    scheduler.solve_variables()
    subject_vars = scheduler.get_solution()

    # Print the schedule
    scheduler.print_programBlocks()
