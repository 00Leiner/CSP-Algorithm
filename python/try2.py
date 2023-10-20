from ortools.sat.python import cp_model

def create_programYears_variables(model):
    programs = ["BSCS", "BSIT"]
    years = ["1st", "2nd", "3rd", "4th"]

    programYears = {} # empty dictionary to store the subject variables

    for program in programs:
        for year in years:
            variable_name = f"{program}_{year}"
            programYears[variable_name] = model.NewBoolVar(variable_name) 
        
    return programYears

def create_subjects_variables(model):
    subjects = {
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


def solve_variables():
    model = cp_model.CpModel()
    programYears = create_programYears_variables(model)
    solver = cp_model.CpSolver()

    solver.Solve(model)
    return programYears

if __name__ == "__main__":
    programYears = solve_variables()
    output = list(programYears.keys())
    print(f"{output}")