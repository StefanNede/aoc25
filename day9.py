DAY = 9

def read_input():
    inputs = []

    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            line = [int(x) for x in line.split(",")]
            inputs.append(line)

    return inputs

def parta():
    # largest rectangle
    coors = read_input()
    largest_area = 0

    for i,coor1 in enumerate(coors):
        for coor2 in coors[i+1:]:
            a,b = coor1
            c,d = coor2
            area = (abs(a-c)+1)*(abs(b-d)+1)
            largest_area = max(largest_area, area)

    return largest_area

# check if walls of region cut into sub_rectangle
def cross_edges(sub_rectangle, walls):
    coor1,coor2 = sub_rectangle
    x1,y1 = coor1
    x2,y2 = coor2

    min_x, max_x = min(x1,x2), max(x1,x2)
    min_y, max_y = min(y1,y2), max(y1,y2)

    for wall in walls:
        (wall_x1, wall_y1), (wall_x2, wall_y2) = wall

        if wall_x1 == wall_x2:
            # VERTICAL EDGE    
            # check x coordinate lies in rectangle range
            if min_x < wall_x1 < max_x:
                overlap_start = max(min_y, min(wall_y1, wall_y2))
                overlap_end = min(max_y, max(wall_y1, wall_y2))
                if overlap_start < overlap_end:
                    return True
        
        elif wall_y1 == wall_y2:
            # HORIZONTAL EDGE
            # check y coordinate lies in rectangle range
            if min_y < wall_y1 < max_y:
                overlap_start = max(min_x, min(wall_x1, wall_x2))
                overlap_end = min(max_x, max(wall_x1, wall_x2))
                if overlap_start < overlap_end:
                    return True

    return False

# check if sub_rectangle is actually inside a proper defined region using raycasting
def is_inside(sub_rectangle, walls):
    # check if sub_rectangle is just a line in which case it must be inside
    coor1,coor2 = sub_rectangle
    x1,y1 = coor1
    x2,y2 = coor2
    if x1 == x2 or y1 == y2:
        return True

    # raycast from center of sub_rectangle to the right
    crossings = 0 # want an odd number of these
    cx = (x1+x2) // 2
    cy = (y1+y2) // 2

    for wall in walls:
        (wall_x1, wall_y1), (wall_x2, wall_y2) = wall
        # only want to check for crossings of vertical walls
        if wall_x1 == wall_x2:
            min_wall_y = min(wall_y1, wall_y2)
            max_wall_y = max(wall_y1, wall_y2)

            if wall_x1 > cx: # wall to the right
                if min_wall_y <= cy <= max_wall_y:
                    crossings += 1

    return (crossings % 2 == 1)

def partb():
    # generate all edges for main shape and then check if each possible sub-rectangle is included 
    # in parent shape by running 2 point check:
    # 1. do edges of main shape cross sub-rectangle
    # 2. is sub-rectangle actually in the main shape interior (or is it in the empty space of a U-shape for example) - use raycasting

    coors = read_input()
    largest_area = 0

    walls = [] # (coor1, coor2) represents edge between these coors
    prevCoor = coors[0]

    for coor in coors[1:]:
        walls.append((prevCoor, coor))
        prevCoor = coor
    
    # the last coor goes back to the first
    walls.append((coors[-1], coors[0]))

    # generate all sub-rectangles
    for i,coor1 in enumerate(coors):
        for coor2 in coors[i+1:]:
            a,b = coor1
            c,d = coor2
            area = (abs(a-c)+1)*(abs(b-d)+1)
            # run the checks 
            if not cross_edges((coor1,coor2), walls) and is_inside((coor1,coor2), walls):
                largest_area = max(largest_area, area)

    return largest_area

# print(parta())
print(partb()) 