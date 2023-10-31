from ortools.sat.python import cp_model

# Sample data
rooms = ["RoomA", "RoomB", "RoomC"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
times = ["7am", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]

model = cp_model.CpModel()

room_available = {}
for room in rooms:
    room_available[room] = {}
    for day in days:
        room_available[room][day] = {}
        for time in times:
            room_available[room][day][time] = model.NewBoolVar(f"{room}_{day}_{time}")

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    for room in rooms:
        for day in days:
            for time in times:
                if solver.Value(room_available[room][day][time]):
                    print(f"{room} is available on {day} at {time}")
else:
    print("No solution found.")
