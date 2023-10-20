from ortools.sat.python import cp_model

def create_subject_variables(model, programs, years, subjects_per_program):
    subject_vars = {}

    for program in programs:
        for year in years:
            for subject in subjects_per_program[program][year]:
                variable_name = f"{program}_{year}_{subject}"
                var = model.NewBoolVar(variable_name)
                subject_vars[variable_name] = var

    return subject_vars

def solve_subject_variables(programs, years, subjects_per_program):
    model = cp_model.CpModel()
    subject_vars = create_subject_variables(model, programs, years, subjects_per_program)
    solver = cp_model.CpSolver()

    solver.Solve(model)

    return subject_vars

if __name__ == "__main__":
    programs = ["BSCS", "BSIT"]
    years = ["1st", "2nd", "3rd", "4th"]
    
    # Define subjects per program
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

    subject_vars = solve_subject_variables(programs, years, subjects_per_program)
    for variable_name in subject_vars.keys():
        print(f"{variable_name}")
