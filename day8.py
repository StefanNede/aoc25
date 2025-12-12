import math
from collections import defaultdict
DAY = 8

def read_input():
    inputs = []

    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            line = [int(x) for x in line.split(",")]
            inputs.append(line)

    return inputs

def parta():
    # union set find
    boxes = read_input()
    num_connections = 1000

    # first calculate all possible connections 
    distances = []
    for i, box1 in enumerate(boxes):
        for j in range(i+1, len(boxes)):
            box2 = boxes[j]
            a,b,c = box1
            d,e,f = box2

            distance = ((a-d)**2 + (b-e)**2 + (c-f)**2)**0.5
            distances.append((distance, (i,j)))
    
    distances.sort(key = lambda x : x[0])
    shortest_distances = distances[:num_connections]

    par = [i for i in range(len(boxes))]
    rank = [1] * len(boxes)

    def find(n1):
        res = n1

        while res != par[res]:
            par[res] = par[par[res]]
            res = par[res]
        
        return res
    
    def union(n1, n2):
        p1, p2 = find(n1), find(n2)

        if p1 == p2: 
            return 0 # already joined
        
        if rank[p2] > rank[p1]:
            par[p1] = p2
            rank[p2] += rank[p1]
        else:
            par[p2] = p1
            rank[p1] += rank[p2]

        return 1 # new join

    for distance, pair in shortest_distances:
    # for distance, pair in distances:
        i,j = pair
        # merge i and j 
        union(i,j)

    circuit_sizes = defaultdict(lambda: 0)
    for i in range(len(boxes)):
        # as we have already calculated rank we could also just matain a set of (root, rank)'s 
        # and then pick the 3 biggest :)
        root = find(i)
        circuit_sizes[root] += 1
    
    sizes = sorted(list(circuit_sizes.values()))[-3:]
    print(sizes)
    return math.prod(sizes)

def partb():
    # same as part (a) but just go until connected all boxes
    boxes = read_input()

    # first calculate all possible connections 
    distances = []
    for i, box1 in enumerate(boxes):
        for j in range(i+1, len(boxes)):
            box2 = boxes[j]
            a,b,c = box1
            d,e,f = box2

            distance = ((a-d)**2 + (b-e)**2 + (c-f)**2)**0.5
            distances.append((distance, (i,j)))
    
    distances.sort(key = lambda x : x[0])

    par = [i for i in range(len(boxes))]
    rank = [1] * len(boxes)

    def find(n1):
        res = n1

        while res != par[res]:
            par[res] = par[par[res]]
            res = par[res]
        
        return res
    
    def union(n1, n2):
        p1, p2 = find(n1), find(n2)

        if p1 == p2: 
            return 0 # already joined
        
        if rank[p2] > rank[p1]:
            par[p1] = p2
            rank[p2] += rank[p1]
        else:
            par[p2] = p1
            rank[p1] += rank[p2]

        return 1 # new join

    num_joins = 0 
    for distance, pair in distances:
        i,j = pair
        # merge i and j 
        num_joins += union(i,j)
        if num_joins == len(boxes)-1:
            print(i,j)
            print(boxes[i])
            print(boxes[j])
            return boxes[i][0] * boxes[j][0]

    return -1

print(parta())
print(partb())