

# Define variables
task_vars = ['task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7', 'task8', 'task9', 'task10', 'task11', 'task12', 'task13', 'task14', 'task15', 'task16', 'task17', 'task18', 'task19', 'task20']
interval_size = 3
rooms = 2
days = 2
times = 15


# Global storage of variables
room_list = {}
for room in range(1, rooms + 1):
    room_list[room] = {}
    for day in range(1, days + 1):
        room_list[room][day] = list(range(times))


# Add constraints to schedule tasks
for task_id, task in enumerate(task_vars):
    scheduled = False
    for room in range(1, rooms + 1):
        if scheduled:
            break
        for day in range(1, days + 1):
            if scheduled:
                break
            for time in room_list[room][day]:
                if time + interval_size <= times:
                    # Check if the time slot is available
                    available = True
                    for t in range(time, time + interval_size):
                        if t not in room_list[room][day]:
                            available = False
                            break
                    if available:
                        # Schedule the task
                        for t in range(time, time + interval_size):
                            room_list[room][day].remove(t)
                        start = time + (day - 1) * times
                        end = start + interval_size
                        scheduled = True
                        print(f"Scheduled {task} in room {room} on day {day} at time {time} - {time + 3}")
                        break
                else:
                    # If the time slot is not available, move to the next room
                    break


