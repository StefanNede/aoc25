from functools import lru_cache
DAY = 11

def read_input():
    inputs = []

    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            line = line.split()
            line[0] = line[0][:-1] # remove colon
            inputs.append(line)

    return inputs

def dfs(node, graph, visited):
    if node == "out":
        return 1
    
    res = 0
    for neighbour in graph[node]:
        if neighbour not in visited:
            visited.add(neighbour)
            res += dfs(neighbour, graph, visited)
            visited.remove(neighbour)
    
    return res
    
def parta():
    # simple graph search count - use DFS or BFS
    inputs = read_input()
    # construct graph - adjacency matrix 
    adj_list = {}
    for selection in inputs:
        start = selection[0]
        adj_list[start] = selection[1:]
    
    visited = set()
    visited.add("you")
    return dfs("you", adj_list, visited)



def partb():
    inputs = read_input()
    # construct graph - adjacency matrix 
    adj_list = {}
    for selection in inputs:
        start = selection[0]
        adj_list[start] = selection[1:]
    
    graph = adj_list
    # regular dfs is now too slow and as we are only intersted in number of paths
    # we memoise it and split the total path down into its components (svr -> fft -> dac -> out)
    # Note: no paths from dac -> fft so we can ignore these in this case but extension to include them is trivial

    visited = set()

    # cba to build up dp array so just using lru_cache
    @lru_cache(maxsize = None)
    def dfs2(node, target):
        nonlocal graph,visited
        if node == target:
            return 1
        
        res = 0
        if node in graph:
            for neighbour in graph[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    res += dfs2(neighbour, target)
                    visited.remove(neighbour)
        
        return res
    
    visited = set()
    visited.add("dac")
    # return dfs2("dac", "out")

    # "svr" -> "fft" 10304
    # "fft" -> "dac" 7921556
    # "dac" -> "out" 3875
    return 10304*7921556*3875 # multiply together num paths between each component

print(parta())
print(partb())