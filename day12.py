from collections import defaultdict, deque
import copy
DAY = 12

def read_input():
    shapes = []
    boxes = [] # [(n,m), 0, 1, 1, ...] for nxm box

    with open(f"day{DAY}.txt", "r") as file:
        shape = []
        for line in file:
            line = line.strip()
            if "x" in line: # one of the boxes
                line = line.split(" ")
                line[0] = line[0][:-1] # remove the colon
                size = tuple([int(i) for i in line[0].split("x")])
                requirements = [int(i) for i in line[1:]]
                box = [size] + requirements
                boxes.append(box)

            elif ":" in line: # new shape
                shape = []
            
            elif line == "": # empty line
                shapes.append(shape[:])
        
            else: # contents of shape
                shape_content = [i for i in line]
                shape.append(shape_content)

    return shapes, boxes


# returns all rotations and flips of a shape
def get_rotflips(shape):
    unique_shapes = []

    # perform a 90-degree clockwise rotation
    def rotate_90(s):
        # -> flip order of rows and then get columns top to bottom
        return [list(row) for row in zip(*s[::-1])]

    # add rotations of original shape
    current = shape
    for _ in range(4):
        if current not in unique_shapes:
            unique_shapes.append(current)
        current = rotate_90(current)

    # add rotations of flipped shape
    flipped_shape = shape[::-1]
    
    current = flipped_shape
    for _ in range(4):
        if current not in unique_shapes:
            unique_shapes.append(current)
        current = rotate_90(current)

    return unique_shapes

# check if shape can fit in box at position (r,c)
def can_place(box, shape, r, c):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            # Only check if the shape actually has a block here
            if shape[i][j] == '#':
                # If grid is also occupied, it's a collision
                if box[r + i][c + j] == '#':
                    return False
    return True

# add shape to box at (r,c)
def place_shape(box, shape, r, c):
    # Deep copy to ensure we don't modify the original grid
    new_box = copy.deepcopy(box)
    
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] == '#':
                new_box[r + i][c + j] = '#'
                
    return new_box

# returns all possible fillings of box with shape
def add_shape_to_box(box, shape):
    possible_boxes = []
    possible_shapes = get_rotflips(shape)

    box_h = len(box)
    box_w = len(box[0])

    for variant in possible_shapes:
        shape_h = len(variant)
        shape_w = len(variant[0])

        # slide shape across grid
        for r in range(box_h - shape_h + 1):
            for c in range(box_w - shape_w + 1):
                if can_place(box, variant, r, c):
                    new_box = place_shape(box, variant, r, c)
                    possible_boxes.append(new_box)

    return possible_boxes

# regular DFS - for each shape to add try it in all possible positions
def dfs(box, requirements, shapes):
    stack = []
    visited = defaultdict(lambda: False)

    stack.append([box,requirements])
    visited[(tuple([tuple(b) for b in box]), tuple(requirements))] = True

    while stack:
        cur_box, cur_req = stack.pop()
        # print(cur_req, cur_box)

        finished = True
        for idx, req in enumerate(cur_req):
            if req > 0:
                finished = False
                shape_to_add = shapes[idx]
                possible_boxes = add_shape_to_box(cur_box, shape_to_add)
                next_req = cur_req[:]
                next_req[idx] -= 1

                for possible_box in possible_boxes:
                    if visited[(tuple([tuple(b) for b in possible_box]), tuple(next_req))]:
                        continue
                    stack.append([possible_box, next_req])
                    visited[(tuple([tuple(b) for b in possible_box]), tuple(next_req))] = True
                
        if finished:
            return 1

    return 0

def get_shape_sizes(shapes):
    sizes = []

    for shape in shapes:
        size = 0
        for row in shape:
            for el in row:
                size += 1 if el == "#" else 0
        sizes.append(size)
    
    return sizes

def parta():
    # IDEA 1: - too slow
    # simple DFS of shapes and their possible rotations (BFS was too slow - DFS is also too slow for ones with no solution)
    # return False down a path when not enough space -> have helper functions to return possible locations given shape and grid
    # NOTE: for search optimisation could store boxes and shapes as integers and use bitmasks for putting shapes inside boxes
    # IDEA 2 - heuristic based and works kind of via luck 
    shapes, boxes = read_input()
    shape_sizes = get_shape_sizes(shapes)
    count = 0

    for box in boxes:
        width, length = box[0]
        actual_box = [["."] * width for _ in range(length)]
        requirements = box[1:]
        # any search I can think of is going to be too slow
        # count += dfs(actual_box,requirements,shapes)

        # trying a more heuristic approach based on areas
        # looking at the shapes we have to fit in boxes we can assume some interlocking
        # so with this lower the average to 8 places per box (instead of the defined 9)
        # and compare this average*num_shapes with the box_size to see if it would fit in
        # LUCKILY THIS WORKS :0
        box_size = width*length
        total_shape_area = sum(map(lambda x : x[0]*x[1], zip(requirements, shape_sizes)))
        # print(box_size, total_shape_area, sum(requirements)*8)

        if box_size < total_shape_area:
            continue
        elif box_size > sum(requirements)*8:
            count += 1
        else: # nothing gets printed here
            print(box_size, total_shape_area)

    return count

def partb():
    # no actual part b -_-
    pass

print(parta())
# print(partb())