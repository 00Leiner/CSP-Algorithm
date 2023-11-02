from itertools import combinations

time_values = ['07:00', '07:30', '08:00', '08:30']

result = []

# Generate all possible combinations of time values with length <= 3
for r in range(1, 4):  # Generating combinations of length 1, 2, and 3
    for combo in combinations(time_values, r):
        result.append(combo)

# Flatten the results
flat_results = [' '.join(combo) for combo in result]

# Print the combinations
for combo in flat_results:
    print(combo)
