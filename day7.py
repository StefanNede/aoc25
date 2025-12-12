from collections import defaultdict
DAY = 7

def read_input():
    inputs = []

    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            inputs.append(line)

    return inputs

def parta():
    # splits 
    graph = read_input()
    splits = 0 

    start_index = list(graph[0]).index("S")
    current_locations = [start_index]

    for i in range(len(graph[1:])):
        new_locations = set()
        current_layer = graph[i]
        for location in current_locations:
            if current_layer[location] == "^":
                splits += 1
                if location == 0:
                    new_locations.add(location+1)
                elif location == len(current_layer)-1:
                    new_locations.add(location-1)
                else:
                    new_locations.add(location+1)
                    new_locations.add(location-1)
            else:
                new_locations.add(location)
            

        current_locations = list(new_locations)

    return splits

def partb():
    # count number of distinct paths
    graph = read_input()

    start_index = list(graph[0]).index("S")
    current_locations = [start_index]
    path_count = defaultdict(lambda: 0)
    path_count[start_index] = 1

    for i in range(len(graph[1:])):
        new_locations = set()
        new_path_count = defaultdict(lambda: 0)
        current_layer = graph[i]
        # print(current_layer, dict(path_count), sum(dict(path_count).values()))
        for location in current_locations:
            count = path_count[location]
            if current_layer[location] == "^":
                if location == 0:
                    new_locations.add(location+1)
                    new_path_count[location+1] += count
                elif location == len(current_layer)-1:
                    new_locations.add(location-1)
                    new_path_count[location-1] += count
                else:
                    new_locations.add(location+1)
                    new_path_count[location+1] += count
                    new_locations.add(location-1)
                    new_path_count[location-1] += count
            else:
                new_locations.add(location)
                new_path_count[location] += count
            

        current_locations = list(new_locations)
        path_count = new_path_count

    return sum(dict(path_count).values())

# this also gives u the acc distinct paths but TLEs on big input
def bad_partb():
    graph = read_input()

    start_index = list(graph[0]).index("S")
    current_paths = [(start_index,)]
    visited = defaultdict(lambda: False)
    visited[(start_index)] = True

    for i in range(len(graph[1:])):
        new_paths = []
        current_layer = graph[i]
        for path in current_paths:
            path = list(path)
            location = path[-1]
            path1 = path.copy()
            path2 = path.copy()
            path2Used = False

            if current_layer[location] == "^":
                if location == 0:
                    path1.append(location+1)
                elif location == len(current_layer)-1:
                    path1.append(location-1)
                else:
                    path1.append(location+1)
                    path2.append(location-1)
                    path2Used = True
            else:
                path1.append(location)
            
            path1 = tuple(path1)
            path2 = tuple(path2)

            # deal with path 1
            if not visited[path1]:
                new_paths.append(path1)
                visited[path1] = True

            # potentially deal with path 2
            if path2Used:
                if not visited[path2]:
                    new_paths.append(path2)
                    visited[path2] = True

        current_paths = new_paths

    return len(current_paths)

print(parta())
print(partb())