# Task : Implement the Water Jug Problem using Depth-First Search 
# (DFS) and print the rules applied at each step.
# Ishmal Nadeem (101) BSAI-4B

def dfs(state, visited, path):
    x, y = state
    
    if x == 2 or y == 2:
        for step in path:
            print(step)
        print("Goal Reached at state:", state)
        return True

    visited.append(state)

    next_states = []

    next_states.append(((4, y), "Fill 4L Jug"))
    next_states.append(((x, 3), "Fill 3L Jug"))
    next_states.append(((0, y), "Empty 4L Jug"))
    next_states.append(((x, 0), "Empty 3L Jug"))

    transfer = min(x, 3 - y)
    next_states.append(((x - transfer, y + transfer), "Pour 4L -> 3L"))

    transfer = min(y, 4 - x)
    next_states.append(((x + transfer, y - transfer), "Pour 3L -> 4L"))

    for new_state, action in next_states:
        if new_state not in visited:
            if dfs(new_state, visited, path + [action + " -> " + str(new_state)]):
                return True

    return False


visited = []
start_state = (0, 0)
dfs(start_state, visited, ["Start at (0, 0)"])
