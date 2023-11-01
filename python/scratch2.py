from ortools.sat.python import cp_model

class Scheduler:
    def __init__(self, rooms):
        self.rooms = rooms