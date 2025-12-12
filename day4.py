DAY = 4

def read_input():
    inputs = []
    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            inputs.append(list(line))
    return inputs

def count_adjacents(graph,x,y):
    directions = [
        (0,1),
        (0,-1),
        (1,0),
        (-1,0),
        (1,1),
        (-1,1),
        (1,-1),
        (-1,-1),
    ]

    count = 0
    for change_x, change_y in directions:
        new_x, new_y = change_x+x, change_y+y

        if min(new_x, new_y) < 0 or new_x >= len(graph) or new_y >= len(graph[0]):
            continue
            
        elif graph[new_x][new_y] == "@":
            count += 1
    
    return count 

def parta():
    graph = read_input()
    count = 0

    for x in range(len(graph)):
        for y in range(len(graph[0])):
            if graph[x][y] == "@" and count_adjacents(graph, x, y) < 4:
                count += 1

    return count

def partb():
    graph = read_input()
    count = 0
    updated = True

    while updated:
        updated = False
        changed = []
        for x in range(len(graph)):
            for y in range(len(graph[0])):
                if graph[x][y] == "@" and count_adjacents(graph, x, y) < 4:
                    count += 1
                    changed.append((x,y))
                    updated = True
        
        for x,y in changed:
            graph[x][y] = "."

    return count

print(parta())
print(partb())