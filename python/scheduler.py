

class Scheduler:
    def __init__(self, programs, years, blocks, subjects_per_program):
        self.programs = programs
        self.years = years
        self.blocks = blocks
        self.subjects_per_program = subjects_per_program

    def create_program_block_variables(self):
        for program in self.programs:
            for year in self.years:
                num_blocks = self.blocks.get(program, {}).get(year, 1)
                year_block_names = [chr(ord('a') + i) for i in range(num_blocks)]
                for block in year_block_names:
                    variable_name = f"{program} {year}{block}"
                    
                    print(variable_name)  # Log variable name
                    for subject in self.subjects_per_program.get(program, {}).get(year, []):
                        print(subject)

if __name__ == "__main__":
    programs = ["BSCS", "BSIT"]
    years = ["1", "2", "3", "4"]
    subjects_per_program = {
        "BSCS": {
            "1": [
                {"name": "Subject1", "code": "CS 2107", "description": "Data Structures and Algorithm", "unit": 3},
                {"name": "Subject2", "code": "CS 2201", "description": "Database Systems", "unit": 3},
                # Add more subjects here
            ],
            "2": [
                {"name": "Subject3", "code": "CS 3105", "description": "Operating Systems", "unit": 3},
                {"name": "Subject4", "code": "CS 3203", "description": "Software Engineering", "unit": 3},
                # Add more subjects here
            ],
            "3": [
                {"name": "Subject5", "code": "CS 4109", "description": "Computer Networks", "unit": 3},
                {"name": "Subject6", "code": "CS 4207", "description": "Artificial Intelligence", "unit": 3},
                # Add more subjects here
            ],
            "4": [
                {"name": "Subject7", "code": "CS 5102", "description": "Web Development", "unit": 3},
                {"name": "Subject8", "code": "CS 5204", "description": "Data Mining", "unit": 3},
                # Add more subjects here
            ]
        },
        "BSIT": {
            "1": [
                {"name": "SubjectA", "code": "IT 1101", "description": "Information Technology Fundamentals", "unit": 3},
                {"name": "SubjectB", "code": "IT 1203", "description": "Database Management Systems", "unit": 3},
                # Add more subjects here
            ],
            "2": [
                {"name": "SubjectC", "code": "IT 2105", "description": "System Analysis and Design", "unit": 3},
                {"name": "SubjectD", "code": "IT 2207", "description": "Web Development", "unit": 3},
                # Add more subjects here
            ],
            "3": [
                {"name": "SubjectE", "code": "IT 3109", "description": "Software Engineering", "unit": 3},
                {"name": "SubjectF", "code": "IT 3201", "description": "Computer Networks", "unit": 3},
                # Add more subjects here
            ],
            "4": [
                {"name": "SubjectG", "code": "IT 4102", "description": "Mobile App Development", "unit": 3},
                {"name": "SubjectH", "code": "IT 4204", "description": "Cloud Computing", "unit": 3},
                # Add more subjects here
            ]
        }
    }

    blocks = {
        "BSCS": {
            "1": 1,
            "2": 1,
            "3": 1,
            "4": 1
        },
        "BSIT": {
            "1": 1,
            "2": 1,
            "3": 1,
            "4": 1
        }
    }

    scheduler = Scheduler(programs, years, blocks, subjects_per_program)

    scheduler.create_program_block_variables()
