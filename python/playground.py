rooms = [
    {
        'name': "room1",
        'availability': [
            {
                'day': "Monday",
                'time': ['07:00', '07:30', '08:00', '08:30'],
            },
            {
                'day': "Tuesday",
                'time': ['07:00', '07:30', '08:00', '08:30'],
            }
            # Add more availability
        ]
    },
    {
        'name': "room2",
        'availability': [
            {
                'day': "Monday",
                'time': ['07:00', '07:30', '08:00', '08:30'],
            },
            {
                'day': "Tuesday",
                'time': ['07:00', '07:30', '08:00', '08:30'],
            }
            # Add more availability
        ]
        # Add more rooms
    }
    # Add more rooms
]

combined_availability = {}

for room in rooms:
    room_name = room['name']
    availability = room['availability']
    for day_info in availability:
        day = day_info['day']
        time = day_info['time']
        if day in combined_availability:
            combined_availability[day][room_name] = time
        else:
            combined_availability[day] = {room_name: time}

# Convert the combined dictionary back to the desired format
combined_availability_list = [{'day': day, 'availability': availability} for day, availability in combined_availability.items()]

print(combined_availability_list)
