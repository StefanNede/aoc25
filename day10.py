import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from collections import defaultdict, deque
DAY = 10

def read_input():
    inputs = []

    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            line = line.split()
            inputs.append(line)

    return inputs

def generate_config_cost(starting_config, target_config, schematics):
    # do a BFS search
    queue = deque() # store (config, num_presses)
    visited = defaultdict(lambda: False)

    queue.append((tuple(starting_config), 0))
    visited[tuple(starting_config)] = True

    while queue:
        config, presses = queue.popleft()

        for schematic in schematics:
            new_config = list(config)
            for change in schematic:
                new_config[change] = "." if new_config[change] == "#" else "#"
            
            if new_config == target_config:
                # print(config, schematic, new_config)
                return presses + 1
            elif visited[tuple(new_config)]: 
                continue
            else:
                queue.append((tuple(new_config),presses+1))
                visited[tuple(new_config)] = True

    return -1

def parta():
    machines = read_input()
    presses = 0

    for machine in machines:
        target_config = list(machine[0][1:-1])
        starting_config = ["."]*len(target_config)

        schematics = [[int(y) for y in x[1:-1].split(",")] for x in machine[1:-1]]
        joltage_reqs = machine[-1] # irrelevant for now
        
        cost = generate_config_cost(starting_config, target_config, schematics)
        presses += cost

    return presses

# TOO SLOW
def generate_joltage_cost_bfs(starting_config, target_config, schematics):
    # do a BFS search - this is WAY too slow
    queue = deque() # store (config, num_presses)
    visited = defaultdict(lambda: False)

    queue.append((tuple(starting_config), 0))
    visited[tuple(starting_config)] = True

    while queue:
        config, presses = queue.popleft()

        for schematic in schematics:
            new_config = list(config)
            for change in schematic:
                new_config[change] += 1
            
            # prune if any joltage exceeds requirement
            prune_this = False
            for i,val in enumerate(new_config):
                if val > target_config[i]:
                    prune_this = True
                
            if prune_this:
                continue

            # continue as normal
            if new_config == target_config:
                # print(config, schematic, new_config)
                return presses + 1
            elif visited[tuple(new_config)]: 
                continue
            else:
                queue.append((tuple(new_config),presses+1))
                visited[tuple(new_config)] = True

    return -1

# unfortunately a greedy solution doesn't work however we can write this as a
# constrained optimisation problem, constraints being that Ax = b and x_i are positive integers
# and ojective function being to minimise the sum of x_i which can be framed as c_T * x where c = 1
# -> A is formed from configurations s.t. each column represents a configuration with A_ij = 1 iff config j contains value i 
#       and 0s elsewhere - it is clear this will generate a sparse matrix so scipy optimisations should help with speed :)  
# -> x is just the amount of presses required for each schematic (has dimension num_schematics)
# -> b is the joltage requirements 
# we therefore have a linear program constrainted to integer values so we can use scipy's milp (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html#scipy.optimize.milp)
def generate_joltage_cost(starting_config, target_config, schematics):
    # create A 
    variables = len(target_config)
    num_schematics = len(schematics)
    A = [[0] * num_schematics for _ in range(variables)]

    # populate A
    for j, schematic in enumerate(schematics):
        for i in schematic:
            A[i][j] = 1
    
    # convert to numpy arrays
    A = np.array(A)
    b = np.array(target_config)
    c = np.array([1 for _ in range(num_schematics)])

    # define constraints
    constraints = LinearConstraint(A,b,b) # Ax = b
    bounds = Bounds(lb=0, ub=np.inf) # keep them positive (or 0) -> you actually don't even need this but included for clarity

    # perform linear program -> integrality of 1 ensures integer results
    res = milp(c=c, integrality=1, bounds=bounds, constraints=constraints)

    if res.success:
        x = res.x
        # print(x)
        return int(np.sum(x))

    print("NO SOLUTION FOUND")
    return -1

def partb():
    machines = read_input()
    presses = 0

    for machine in machines:
        target_config = list(machine[0][1:-1]) # now irrelevant

        schematics = [[int(y) for y in x[1:-1].split(",")] for x in machine[1:-1]]
        joltage_reqs = [int(x) for x in machine[-1][1:-1].split(",")]
        starting_joltages = [0] * len(joltage_reqs)
        
        cost = generate_joltage_cost(starting_joltages, joltage_reqs, schematics)
        presses += cost

    return presses

print(parta())
print(partb())